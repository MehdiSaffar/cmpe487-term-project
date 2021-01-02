import asyncio as aio
from json.decoder import JSONDecodeError
import time
# import pygame
import socket
# from pygame.locals import *
from aioconsole import ainput
import json
import sys
import concurrent.futures
from simple_term_menu import TerminalMenu


TCP_PORT = 5000
UDP_PORT = 5000


async def tcp_sock_read_all(sock: socket.socket):
    loop = aio.get_running_loop()
    line = bytearray()
    while True:
        buffer = await loop.sock_recv(sock, 1024)
        if not buffer:
            return line
        line += buffer


def sock_recvfrom(loop, sock, n_bytes, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_reader(fd)

    try:
        data, addr = sock.recvfrom(n_bytes)
    except (BlockingIOError, InterruptedError):
        loop.add_reader(fd, sock_recvfrom, loop, sock, n_bytes, fut, True)
    else:
        fut.set_result((data, addr))
    return fut


def sock_sendto(loop, sock, data, addr, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_writer(fd)
    if not data:
        return

    try:
        n = sock.sendto(data, addr)
    except (BlockingIOError, InterruptedError):
        loop.add_writer(fd, sock_sendto, loop, sock, data, addr, fut, True)
    else:
        fut.set_result(n)
    return fut


# def handle_message(message):
#     if message.type == '':
#         1
#     if message.type == '':
#         2
#     if message.type == '':
#         2

# def start_udp_listen_forever():
#     while True:
#         line = get_line()
#         handle_message(line)

class Game:
    def __init__(self, name: str, ip: str) -> None:
        super().__init__()
        self.ip = ip
        self.name = name
        self.player_accepted = aio.Event()
        # self.players = dict()
        self.players = {
            'buse': 'kababakakabak',
            'mehdi': 'safsar'
        }

    async def handle_udp_message(self, line: str):
        packet = json.loads(line)
        if packet["TYPE"] == "DISCOVER":
            self.players[packet['NAME']] = {"IP": packet["SRC_IP"], 'NAME': packet['NAME']}
            await self.respond(packet["SRC_IP"])

        elif packet["TYPE"] == "RESPOND":
            self.players[packet['NAME']] = {"IP": packet['SRC_IP'], 'NAME': packet['NAME']}

    async def handle_tcp_message(self, line: str):
        packet = json.loads(line)
        if packet["TYPE"] == "PLAY_REQUEST":
            is_accepted = self.choose_yes_no(packet) # 2s, 10s, 
            if is_accepted:
                self.player_accepted.set()
            else:
                self.player_refused.set()

            await self.send_play_response(packet['SRC_IP'], is_accepted)

    async def send_udp_message(self, packet: dict, ip: str):
        loop = aio.get_running_loop()

        packet['SRC_IP'] = self.ip
        packet['DST_IP'] = '<broadcast>'
        packet['NAME'] = self.name

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # sock.bind(('',0))
            sock.setblocking(False)
            if ip == '<broadcast>':
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            await sock_sendto(loop, sock, json.dumps(packet).encode('utf-8'), (ip, UDP_PORT))

    async def send_tcp_message(self, packet: dict, ip: str):
        loop = aio.get_running_loop()

        packet['SRC_IP'] = self.ip
        packet['DST_IP'] = ip
        packet['NAME'] = self.name

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)

            await loop.sock_connect(sock, (ip, TCP_PORT))

            packet = json.dumps(packet) + '\n'
            packet = packet.encode('utf-8')

            await loop.sock_sendall(sock, packet)

    async def send_respond(self, dst_ip):
        respond_packet = {"TYPE": "RESPOND", "PAYLOAD": ""}
        await self.send_udp_message(respond_packet, dst_ip)

    async def send_discover(self):
        discover_packet = {"TYPE": "DISCOVER", "PAYLOAD": ""}
        await self.send_udp_message(discover_packet, '<broadcast>')

    async def send_play_response(self, dst_ip, answer):
        play_response_packet = {"TYPE": "PLAY_RESPONSE", "PAYLOAD": answer}
        await self.send_tcp_message(play_response_packet, dst_ip)

    async def send_play_request(self, dst_ip):
        play_request_packet = {"TYPE": "PLAY_REQUEST", "PAYLOAD": ""}
        await self.send_tcp_message(play_request_packet, dst_ip)

    async def udp_listen(self):
        loop = aio.get_running_loop()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setblocking(False)
            sock.bind(('', UDP_PORT))

            while True:
                line, _ = await sock_recvfrom(loop, sock, 1000)
                line = line.decode('utf-8').strip()
                await self.handle_udp_message(line)

    async def tcp_listen(self):
        loop = aio.get_running_loop()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            sock.bind((self.ip, TCP_PORT))
            sock.listen()

            while True:
                client, _ = await loop.sock_accept(sock)
                with client:
                    line = await tcp_sock_read_all(client)
                    line = line.decode('utf-8').strip()
                    await self.handle_tcp_message(line)

    def list_players(self):
        for player_name, player in self.players.items():
            print(f"{player_name}: {json.dumps(player)}")

    def choose_player(self):
        choices = list(self.players.keys())

        player_menu = TerminalMenu(choices, title='Choose player')
        chosen_player_ix = player_menu.show()
        chosen_player = self.players[choices[chosen_player_ix]]
        return chosen_player

    def choose_yes_no(self, player: dict):
        choices = ['yes', 'no']

        choice_menu = TerminalMenu(choices, title=f'Would you like to play with {player["NAME"]}?')
        return choices[choice_menu.show()] == 'yes'

    async def blabla(self):
        i = 0
        while True:
            await aio.sleep(0.1)
            i += 1
            print(i)

    async def main(self):
        aio.create_task(self.udp_listen())
        aio.create_task(self.tcp_listen())
        # aio.create_task(self.blabla())

        for _ in range(3):
            await self.discover()

        # loop = aio.get_running_loop()
        # executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        while True:
            command = await ainput('>>> ')
            if command == 'list':
                self.list_players()
            if command == 'play':
                player = self.choose_player()  # becareful, blocking
                await self.send_play_request(player["IP"])

                await aio.wait([self.player_accepted.wait(), self.player_refused.wait()], return_when=aio.FIRST_COMPLETED)
                is_accepted = self.player_accepted.is_set()
                self.player_accepted.clear()
                self.player_refused.clear()

                if not is_accepted:
                    print('go melih bulu yourself')
                else:
                    print('all right lets play')

        # at this point we have sent the discovers
        # but it is not guaranteed that we received all responds


async def main():
    game = Game(name='mehdi', ip='127.0.0.1')
    await game.main()

if __name__ == '__main__':
    aio.run(main())

# pygame.init()
# surface = pygame.display.set_mode((500, 500))

# FPS = pygame.time.Clock()


# while True:
#     # Process all events
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()

#     # Do all the drawings here
#     surface.fill((255, 255, 255))

#     # Update the actual screen
#     pygame.display.update()
#     FPS.tick(60)

    # start_udp_listen_forever()
    # start_tcp_listen_forever()

    # discover_peers()

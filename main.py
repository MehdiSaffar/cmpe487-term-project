import concurrent.futures
import io as aio
import json
import queue
import socket
import sys
import threading
import numpy as np
import time
from json.decoder import JSONDecodeError

import pygame
from aioconsole import ainput
from pygame.locals import *
from simple_term_menu import TerminalMenu

TCP_PORT = 5000
UDP_PORT = 5000


# def tcp_sock_read_all(sock: socket.socket):
#     loop = aio.get_running_loop()
#     line = bytearray()
#      while True:
#           buffer = loop.sock_recv(sock, 1024)
#            if not buffer:
#                 return line
#             line += buffer


# def sock_recvfrom(loop, sock, n_bytes, fut=None, registed=False):
#     """
#     CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-io.html#simple-io-udp-echo-server
#     """
#     fd = sock.fileno()
#     if fut is None:
#         fut = loop.create_future()
#     if registed:
#         loop.remove_reader(fd)

#     try:
#         data, addr = sock.recvfrom(n_bytes)
#     except (BlockingIOError, InterruptedError):
#         loop.add_reader(fd, sock_recvfrom, loop, sock, n_bytes, fut, True)
#     else:
#         fut.set_result((data, addr))
#     return fut


# def sock_sendto(loop, sock, data, addr, fut=None, registed=False):
#     """
#     CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-io.html#simple-io-udp-echo-server
#     """
#     fd = sock.fileno()
#     if fut is None:
#         fut = loop.create_future()
#     if registed:
#         loop.remove_writer(fd)
#     if not data:
#         return

#     try:
#         n = sock.sendto(data, addr)
#     except (BlockingIOError, InterruptedError):
#         loop.add_writer(fd, sock_sendto, loop, sock, data, addr, fut, True)
#     else:
#         fut.set_result(n)
#     return fut


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

class Board:
    EMPTY_CELL = ' '
    P1_CELL = 'R'
    P2_CELL = 'Y'

    def __init__(self) -> None:
        super().__init__()
        self.grid = np.full((6, 7), Board.EMPTY_CELL)


class Game:
    def init_game(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.turn = player1

    def __init__(self, name: str, ip: str) -> None:
        super().__init__()
        self.ip = ip
        self.name = name
        self.players = {
            'buse': {'NAME': 'buse', 'IP': other_ip},
            'mehdi': 'safsar'
        }

    def handle_udp_message(self, line: str):
        print(repr(line))
        packet = json.loads(line)
        if packet["TYPE"] == "DISCOVER":
            self.players[packet['NAME']] = {"IP": packet["SRC_IP"], 'NAME': packet['NAME']}
            self.send_respond(packet["SRC_IP"])

        elif packet["TYPE"] == "RESPOND":
            self.players[packet['NAME']] = {"IP": packet['SRC_IP'], 'NAME': packet['NAME']}

    def handle_tcp_message(self, line: str):
        print(repr(line))
        packet = json.loads(line)
        if packet["TYPE"] == "PLAY_REQUEST":
            is_accepted = self.choose_yes_no(packet)  # 2s, 10s,
            self.send_play_response(packet['SRC_IP'], is_accepted)
            if is_accepted:
                player1 = packet['NAME']
                player2 = self.name
                self.init_game(player1=player1, player2=player2)

        if packet["TYPE"] == "PLAY_RESPONSE":
            if packet["PAYLOAD"]:
                player1 = self.name
                player2 = packet['NAME']
                self.init_game(player1=player1, player2=player2)

    def send_udp_message(self, packet: dict, ip: str):
        packet['SRC_IP'] = self.ip
        packet['DST_IP'] = '<broadcast>'
        packet['NAME'] = self.name

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # sock.bind(('',0))

            if ip == '<broadcast>':
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            packet = json.dumps(packet).encode('utf-8')
            sock.sendto(packet, (ip, UDP_PORT))

    def send_tcp_message(self, packet: dict, ip: str):
        packet['SRC_IP'] = self.ip
        packet['DST_IP'] = ip
        packet['NAME'] = self.name

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, TCP_PORT))

            packet = json.dumps(packet) + '\n'
            packet = packet.encode('utf-8')

            sock.sendall(packet)

    def send_respond(self, dst_ip):
        respond_packet = {"TYPE": "RESPOND", "PAYLOAD": ""}
        self.send_udp_message(respond_packet, dst_ip)

    def send_discover(self):
        discover_packet = {"TYPE": "DISCOVER", "PAYLOAD": ""}
        self.send_udp_message(discover_packet, '<broadcast>')

    def send_play_response(self, dst_ip, answer):
        play_response_packet = {"TYPE": "PLAY_RESPONSE", "PAYLOAD": answer}
        self.send_tcp_message(play_response_packet, dst_ip)

    def send_play_request(self, dst_ip):
        play_request_packet = {"TYPE": "PLAY_REQUEST", "PAYLOAD": ""}
        self.send_tcp_message(play_request_packet, dst_ip)

    def list_players(self):
        for player_name, player in self.players.items():
            print(f"{player_name}: {json.dumps(player)}")

    def choose_player(self):
        choices = list(self.players.keys())

        player_menu = TerminalMenu(choices, title='Choose player')
        chosen_player_ix = player_menu.show()
        chosen_player = self.players[choices[chosen_player_ix]]
        print('chosen player', chosen_player)
        return chosen_player

    def choose_yes_no(self, player: dict):
        choices = ['yes', 'no']

        choice_menu = TerminalMenu(choices, title=f'Would you like to play with {player["NAME"]}?')
        return choices[choice_menu.show()] == 'yes'

    def handle_command(self, command):
        if command == 'list':
            self.list_players()
        elif command == 'play':
            player = self.choose_player() 
            self.send_play_request(player["IP"])

    def main(self):
        for _ in range(3):
            self.send_discover()

        while True:
            # input
            while not input_q.empty():
                command = input_q.get()
                self.handle_command(command)
                input_q.task_done()

            # tcp
            while not tcp_q.empty():
                tcp_msg = tcp_q.get()
                self.handle_tcp_message(tcp_msg)
                tcp_q.task_done()

            # udp
            while not udp_q.empty():
                udp_msg = udp_q.get()
                self.handle_udp_message(udp_msg)
                udp_q.task_done()


# ip = '127.0.0.1'
ip = f'127.0.0.{sys.argv[1]}'
other_ip = f'127.0.0.{sys.argv[2]}'
name = sys.argv[3]

input_q = queue.Queue()
tcp_q = queue.Queue()
udp_q = queue.Queue()


def game_thread():
    game = Game(name=name, ip=ip)
    game.main()


def udp_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, UDP_PORT))

        while True:
            line, addr = sock.recvfrom(1024)
            line = line.decode('utf-8').strip()
            udp_q.put(line)


def tcp_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((ip, TCP_PORT))
        sock.listen()

        while True:
            client, _ = sock.accept()
            with client:
                line = b''
                while True:
                    chunk = client.recv(1024)
                    if not chunk:
                        break
                    line += chunk

                line = line.decode('utf-8').strip()
                tcp_q.put(line)


def input_thread():
    while True:
        command = input('>>> ')
        input_q.put(command)
        input_q.join()


if __name__ == '__main__':
    tcp_th = threading.Thread(target=tcp_thread)
    udp_th = threading.Thread(target=udp_thread)
    game_th = threading.Thread(target=game_thread)
    tcp_th.start()
    udp_th.start()
    game_th.start()

    input_thread()

    tcp_th.join()
    udp_th.join()
    game_th.join()

# pygame.init()tcp_q = queue.Queue()
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

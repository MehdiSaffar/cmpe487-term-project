import asyncio as aio
import socket
import janus

from .constants import *
from .utils import sock_recvfrom, sock_sendto

class Network():
    def __init__(self):
        self.is_ready = False
        # Cannot initialize queues here since they depend on asyncio loop to be running
        self.recv_q = None
        self.tcp_send_q = None
        self.udp_send_q = None

        self.udp_port = UDP_PORT
        self.tcp_port = TCP_PORT

    async def _udp_recv_loop(self, addr):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setblocking(False)
            sock.bind(addr)

            while True:
                line, addr = await sock_recvfrom(self.loop, sock, 1000)
                line = line.decode('utf-8').strip()
                await self.recv_q.async_q.put(('udp', (addr[0], self.udp_port), line))

    async def _tcp_recv_loop(self, addr):
        async def read_all(sock: socket.socket):
            line = bytearray()
            while True:
                buffer = await self.loop.sock_recv(sock, 1024)
                if not buffer:
                    return line
                line += buffer

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            sock.bind(addr)
            sock.listen()

            while True:
                client, addr = await self.loop.sock_accept(sock)
                with client:
                    line = await read_all(client)
                    line = line.decode('utf-8').strip()
                    await self.recv_q.async_q.put(('tcp', (addr[0], self.tcp_port), line))
    
    async def _tcp_send_loop(self):
        addr, data = await self.tcp_send_q.async_q.get()
        print('tcp_send', addr, data)
        await self._tcp_send(addr, data)
        self.tcp_send_q.async_q.task_done()

    async def _udp_send_loop(self):
        addr, data = await self.udp_send_q.async_q.get()
        print('udp_send', addr, data)
        await self._udp_send(addr, data)
        self.udp_send_q.async_q.task_done()

    async def _tcp_send(self, addr, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)

            await self.loop.sock_connect(sock, addr)
            await self.loop.sock_sendall(sock, data)

    async def _udp_send(self, addr, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setblocking(False)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(('', 0))

            await sock_sendto(self.loop, sock, data, addr)
    
    def send(self, packet):
        type, ip, data = packet
        if type == 'udp':
            self.udp_send_q.sync_q.put(((ip, self.udp_port), data))
        elif type == 'tcp':
            self.tcp_send_q.sync_q.put(((ip, self.tcp_port), data))
        else:
            raise Exception(f'Unknown type {type}')

    async def main(self):
        self.recv_q = janus.Queue()
        self.udp_send_q = janus.Queue()
        self.tcp_send_q = janus.Queue()

        self.loop = aio.get_running_loop()

        udp_listen_loop_task = aio.create_task(self._udp_recv_loop(('', self.udp_port)))
        tcp_listen_loop_task = aio.create_task(self._tcp_recv_loop(('', self.tcp_port)))

        tcp_send_loop_task = aio.create_task(self._tcp_send_loop())
        udp_send_loop_task = aio.create_task(self._udp_send_loop())

        self.is_ready = True

        await aio.wait([udp_listen_loop_task, tcp_listen_loop_task, tcp_send_loop_task, udp_send_loop_task])
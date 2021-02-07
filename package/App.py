from package.scenes.PlayScene import PlayScene
from package.scenes.SendRequestScene import SendRequestScene
from package.scenes.LobbyScene import LobbyScene
from package.scenes.MenuScene import MenuScene
from package.Packet import discover_packet, discover_reply_packet

import pygame
import pygame_gui as pygui
import asyncio as aio
import time
import threading
import queue
import json

from .scenes import LobbyScene
from .constants import Color, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from .Network import Network
from .NetEvent import NetEvent


class App:
    def __init__(self):
        self.init_network()
        self.init_pygame()
        self.scene = MenuScene(self)

        self.players = {}

        # DO NOT HANDLE MESSAGES IN APP
        # HANDLE THEM IN CHAT COMPONENT
        # I HAVE MESSAGES HERE ONLY TO PERSIST THEM
        self.messages = [] 

        while not self.network.is_ready:
            time.sleep(0.01)

    def init_network(self):
        self.network = Network()

        def network_main(network):
            aio.run(network.main())

        self.network_thread = threading.Thread(
            target=network_main, args=(self.network,), daemon=True)
        self.network_thread.start()

    def discover_players(self):
        self.network.send(
            ('udp', '<broadcast>', discover_packet(self.my_name, self.network.ip)))

    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()  # For sound

        self.player_name = ''
        self.my_name = ''

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.scene = MenuScene(self)

        pygame.display.set_caption("Connect4")
        self.clock = pygame.time.Clock()  # For syncing the FPS
        self.is_running = True

        self.ui = pygui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    def get_events(self):
        for event in pygame.event.get():
            yield event
        while True:
            try:
                type, addr, data = self.network.recv_q.sync_q.get_nowait()
                yield NetEvent(type, addr, json.loads(data))
            except queue.Empty:
                break

    def get_other_player_ip(self):
        return self.players[self.player_name]['ip']

    def main(self):
        while self.is_running:
            # will make the loop run at the same speed all the time
            time_delta = self.clock.tick(FPS) / 1000.0

            # 1 Process input/events
            for event in self.get_events():
                if event.type == pygame.USEREVENT:
                    print('main', event)
                    # if event.user_type == 'ui_text_entry_finished':
                    #     print('main', event)

                if event.type == 'udp':
                    if not isinstance(self.scene, MenuScene):
                        if event.data['type'] == 'discover':
                            if event.data['name'] not in self.players:
                                self.players[event.data['name']] = {
                                    'ip': event.data['ip']}
                                self.network.send(
                                    ('udp', event.data['ip'], discover_reply_packet(self.my_name, self.network.ip)))
                        elif event.data['type'] == 'discover_reply':
                            self.players[event.data['name']] = {
                                'ip': event.data['ip']}

                if event.type == pygame.QUIT:
                    self.is_running = False

                self.scene.handle_event(event)
                self.ui.process_events(event)

            # 2 Update
            self.ui.update(time_delta)
            self.scene.update()

            # 3 Render
            self.screen.fill(Color.LIGHT_BLUE)
            self.scene.draw()
            self.ui.draw_ui(self.screen)

            # Done after drawing everything to the screen
            pygame.display.flip()

        pygame.quit()

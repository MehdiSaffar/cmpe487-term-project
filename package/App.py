from package.scenes.PlayScene import PlayScene
from package.scenes.SendRequestScene import SendRequestScene
from package.scenes.LobbyScene import LobbyScene
from package.scenes.MenuScene import MenuScene
from package.scenes.PopupScene import PopupScene
from package.Packet import discover_packet, discover_reply_packet, goodbye_packet

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

        self.my_all_scores = {}

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
        self.network.send(('udp', '<broadcast>', discover_packet(
            self.my_name, self.network.ip, self.my_score)))

    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()  # For sound

        self.player_name = ''
        self.my_name = ''
        self.my_score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.scene = MenuScene(self)

        pygame.display.set_caption("Connect4")
        self.clock = pygame.time.Clock()  # For syncing the FPS
        self.is_running = True

    def get_my_score_from_file(self):
        with open('my_scores.txt') as file:
            for line in file:
                key, val = line.split(': ')
                self.my_all_scores[key] = int(val)

        print(self.my_all_scores)

        if self.my_name in self.my_all_scores:
            self.my_score = int(self.my_all_scores[self.my_name])
            print("my score: ", self.my_score)
        else:
            self.my_all_scores[self.my_name] = self.my_score

    def write_my_score_into_file(self):
        with open("my_scores.txt", "w") as file:
            for key, val in self.my_all_scores.items():
                file.write(f"{key}: {val}\n")

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
            self.time_delta = self.clock.tick(FPS) / 1000.0

            # 1 Process input/events
            for event in self.get_events():
                if event.type == pygame.WINDOWCLOSE:
                    print("Quiting")
                    self.network.send(('udp', '<broadcast>', goodbye_packet(self.my_name, self.network.ip)))
                    self.is_running = False
                    break

                if event.type == 'tcp':
                    if event.data['type'] == 'chat_message':
                        name, message = event.data['name'], event.data['message']
                        self.app.messages.append(('regular', name, message))
                        self.prepare_chatbox()

                if event.type == 'udp':
                    if event.data['type'] == 'goodbye':
                        name = event.data['name']
                        self.app.messages.append(
                            ('event', None, f'{name} left the lobby'))
                        self.prepare_chatbox()

                        if event.data['name'] in self.players:
                            del self.players[event.data['name']]

                    if event.data['type'] in ['discover']:
                        name = event.data['name']
                        self.app.messages.append(
                            ('event', None, f'{name} joined the lobby'))
                        self.prepare_chatbox()

                    if not isinstance(self.scene, MenuScene):
                        if event.data['type'] == 'discover':
                            if event.data['name'] not in self.players:
                                self.players[event.data['name']] = {
                                    'ip': event.data['ip'], 'score': event.data['score']}
                                self.network.send(('udp', event.data['ip'], discover_reply_packet(
                                    self.my_name, self.network.ip, self.my_score)))
                        elif event.data['type'] == 'discover_reply':
                            self.players[event.data['name']] = {
                                'ip': event.data['ip'], 'score': event.data['score']}

                self.scene.handle_event(event)

            # 2 Update
            self.scene.update()

            # 3 Render
            self.screen.fill(Color.LIGHT_BLUE)
            self.scene.draw()

            # Done after drawing everything to the screen
            pygame.display.flip()

        pygame.quit()

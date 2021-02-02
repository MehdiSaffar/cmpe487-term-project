from package.scenes.PlayScene import PlayScene
import pygame
import asyncio as aio
import time
import threading
import queue

from .scenes import LobbyScene
from .constants import Color, WIDTH, HEIGHT, FPS
from .Network import Network
from .NetEvent import NetEvent


class App:
    def __init__(self):
        self.scene = LobbyScene(self)
        # self.scene = PlayScene(self)

        self.init_network()
        self.init_pygame()

        while not self.network.is_ready:
            time.sleep(0.01)
    
    def init_network(self):
        self.network = Network()

        def network_main(network):
            aio.run(network.main())

        self.network_thread = threading.Thread(target=network_main, args=(self.network,), daemon=True)
        self.network_thread.start()
    
    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()  # For sound

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect4")
        self.clock = pygame.time.Clock()  # For syncing the FPS
        self.is_running = True
    
    def get_events(self):
        for event in pygame.event.get():
            yield event
        while True:
            try:
                type, addr, data = self.network.recv_q.sync_q.get_nowait()
                yield NetEvent(type, addr, data)
            except queue.Empty:
                break


    def main(self):
        while self.is_running:
            # 1 Process input/events
            for event in self.get_events():
                if event.type == 'tcp':
                    print(event)
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.scene.handle_event(event)

            # 2 Update
            self.scene.update()

            # 3 Render
            self.screen.fill(Color.WHITE)
            self.scene.draw()

            # Done after drawing everything to the screen
            pygame.display.flip()
            self.clock.tick(FPS)  # will make the loop run at the same speed all the time

        pygame.quit()

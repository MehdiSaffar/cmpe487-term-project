import pygame

from .scenes import LobbyScene
from .constants import *

class App:
    def __init__(self):
        self.scene = LobbyScene(self)

        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()  # For sound

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect4")
        self.clock = pygame.time.Clock()  # For syncing the FPS
        self.is_running = True

    def main(self):
        while self.is_running:
            # 1 Process input/events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.scene.handle_event(event)

            # 2 Update
            self.scene.update()

            # 3 Render
            self.screen.fill(WHITE)
            self.scene.draw()

            # Done after drawing everything to the screen
            pygame.display.flip()
            self.clock.tick(FPS)  # will make the loop run at the same speed all the time

        pygame.quit()

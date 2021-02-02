from package.scenes.PlayScene import PlayScene
from package.scenes.SendRequestScene import SendRequestScene
from package.scenes.LobbyScene import LobbyScene
from package.scenes.MenuScene import MenuScene

import pygame

from .constants import Color, SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # For sound

        self.player_name = ''
        self.my_name = ''

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.scene = MenuScene(self)
        
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
            self.screen.fill(Color.LIGHT_BLUE)
            self.scene.draw()

            # Done after drawing everything to the screen
            pygame.display.flip()
            self.clock.tick(FPS)  # will make the loop run at the same speed all the time

        pygame.quit()

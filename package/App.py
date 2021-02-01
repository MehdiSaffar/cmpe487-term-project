from package.scenes.PlayScene import PlayScene
from package.scenes.SendRequestScene import SendRequestScene
from package.scenes.LobbyScene import LobbyScene


import pygame
import pygame_menu

from .constants import Color, SCREEN_WIDTH, SCREEN_HEIGHT, FPS




class App:
    def __init__(self):
        
        pygame.init()
        self.player_name = None
        self.my_name = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #self.scenes = {'Lobby': LobbyScene(self), 'Play': PlayScene(self), 'SendRequest': SendRequestScene(self)} 
        #self.scene = self.scenes['Lobby']
        self.scene = LobbyScene(self)
        # self.scene = LobbyScene(self)
        #self.scene = PlayScene(self)

        # initialize pygame and create window
        
        #pygame.mixer.init()  # For sound

        
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

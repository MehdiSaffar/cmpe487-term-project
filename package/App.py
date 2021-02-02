from package.scenes.PlayScene import PlayScene
from package.scenes.SendRequestScene import SendRequestScene
from package.scenes.LobbyScene import LobbyScene


import pygame
import pygame_menu

from .constants import Color, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import ctypes
import os


class App:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.player_name = None
        self.my_name = None
        user32 = ctypes.windll.user32
        #self.max_width, self.max_heigth =  user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        #1280, 720
        #print(self.max_width, self.max_heigth)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
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

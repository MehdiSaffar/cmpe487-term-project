
from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
from ..scenes.LobbyScene import LobbyScene
import pygame
import pygame_menu

class MenuScene:
    def __init__(self, app):
        self.app = app

        menu_theme = pygame_menu.themes.Theme(
            background_color=Color.LIGHT_BLUE, # transparent background
            title_shadow=True,
            title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=menu_theme)
        self.menu.add_text_input('Username : ', default=self.app.my_name, onchange=self.handle_username_change)
        self.menu.add_button('Play', self.handle_play)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def handle_username_change(self, name):
        self.app.my_name = name

    def handle_event(self, event):
        self.menu.update([event])

    def handle_play(self):
        print("app player name: ",self.app.player_name)
        self.app.scene = LobbyScene(self.app)

    def update(self):
        pass

    def draw(self):
        self.menu.draw(self.app.screen)
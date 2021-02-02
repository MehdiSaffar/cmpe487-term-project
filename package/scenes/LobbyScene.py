from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
import pygame
import pygame_menu

class LobbyScene:
    def __init__(self, app):
        self.app = app
        self.players = [("buse",0), ("mehdi", 1)]
        self.app.player_name = self.players[0][0]

        menu_theme = pygame_menu.themes.Theme(
            background_color=Color.LIGHT_BLUE, # transparent background
            title_shadow=True,
            title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=menu_theme)
        self.menu.add_text_input('Username : ', default=self.app.my_name, onchange=self.handle_username_change)
        self.menu.add_selector('Choose Player :', self.players, onchange=self.handle_choose_player)
        self.menu.add_button('Play', self.handle_play)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def handle_username_change(self, name):
        self.app.my_name = name

    def handle_event(self, event):
        self.menu.update([event])
        

    def handle_choose_player(self, player_name, player_number):
        self.app.player_name = player_name[0][0]
        print("player name = ",player_name[0][0])
        

    def handle_play(self):
        if not self.app.player_name:
            return

        print("app player name: ",self.app.player_name)
        print("sending game request...")
        self.app.scene = SendRequestScene(self.app)

    def update(self):
        pass

    def draw(self):
        self.menu.draw(self.app.screen)
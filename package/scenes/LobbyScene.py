from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
import pygame
import pygame_menu

class LobbyScene:
    def __init__(self, app):
        self.app = app
        self.players = []

        self.menu = None

        self.discover_players()

    
    def prepare_menu(self):
        menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=menu_theme)

        for player in self.players:
            self.menu.add_button(player[0], lambda: self.handle_choose_player(player[0]))

    def discover_players(self):
        # self.app.network.send(('tcp', '<broadcast>' )
        pass


    def handle_event(self, event):
        if self.menu:
            self.menu.update([event])

    def handle_choose_player(self, player_name):
        # istek gondermemiz lazim
        print("player name = ", player_name)
        self.app.player_name = player_name
        self.app.scene = SendRequestScene(self.app)
        
    def update(self):
        pass

    def draw(self):
        if self.menu:
            self.menu.draw(self.app.screen)
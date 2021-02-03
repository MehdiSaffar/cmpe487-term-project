from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
import pygame
import pygame_menu

from ..Packet import discover_packet

class LobbyScene:
    def __init__(self, app):
        self.app = app
        self.menu = None
        self.prepare_menu()
    
    def prepare_menu(self):
        menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=menu_theme)

        for player in self.app.players.keys():
            #print("playerss: ",self.app.players)
            if(player!=''):
                self.menu.add_button(player, lambda: self.handle_choose_player(player))

    #def discover_players(self):
    #    self.app.players = []
    #    self.app.network.send(('udp', '<broadcast>', discover_packet(self.app.my_name, self.app.network.ip)))


    def handle_event(self, event):
        if self.menu:
            self.menu.update([event])

    def handle_choose_player(self, player_name):
        # istek gondermemiz lazim
        print("player name = ", player_name)
        self.app.player_name = player_name
        self.app.scene = SendRequestScene(self.app)
        
    def update(self):
        self.prepare_menu()

    def draw(self):
        if self.menu:
            self.menu.draw(self.app.screen)
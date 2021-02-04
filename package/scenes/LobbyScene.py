from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
from ..scenes.PlayScene import PlayScene

import pygame
import pygame_menu

from ..Packet import discover_packet

class LobbyScene:
    def __init__(self, app):
        self.app = app
        self.players = []

        self.state = 'normal'
        self.discover_players()

        self.menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.prepare_player_list_menu()

    def prepare_player_list_menu(self):
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=self.menu_theme)

        for player in self.app.players.keys():
            #print("playerss: ",self.app.players)
            if(player!=''):
                self.menu.add_button(player, lambda: self.handle_choose_player(player))

    def prepare_invite_menu(self):
        self.invite_menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Game request', theme=self.menu_theme)

        player_name = self.state['packet']['name']

        self.menu.add_label(f"{player_name} would like to play with you")
        self.menu.add_button('Accept', self.handle_accept_invite)
        self.menu.add_button('Decline', self.handle_reject_invite)
    
    def handle_accept_invite(self):
        self.app.player_name = self.state['packet']['name']
        self.app.scene = PlayScene(self.app)

    def handle_reject_invite(self):
        self.state = {'type': 'normal'}

    def discover_players(self):
        self.app.network.send(('udp', '<broadcast>', discover_packet(self.app.my_name, self.app.network.ip)))


    def handle_event(self, event):
        if event.type == 'tcp':
            if event.data['type'] == 'game_request':
                self.state = {'type': 'invited', 'packet': event.data }
                self.prepare_invite_menu()

        if self.state['type'] == 'normal':
            self.menu.update([event])
        elif self.state['type'] == 'invited':
            self.invite_menu.update([event])

    def handle_choose_player(self, player_name):
        print("player name = ", player_name)
        self.app.player_name = player_name
        self.app.scene = SendRequestScene(self.app)
        
    def update(self):
        self.prepare_menu()

    def draw(self):
        if self.state['type'] == 'normal':
            self.menu.draw(self.app.screen)
        elif self.state['type'] == 'invited':
            self.invite_menu.draw(self.app.screen)
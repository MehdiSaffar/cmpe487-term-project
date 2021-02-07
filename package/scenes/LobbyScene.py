from ..constants import *
from .. import scenes

import pygame
import pygame_menu

from ..Packet import discover_packet, game_reply_packet

class LobbyScene:
    def __init__(self, app):
        self.app = app

        self.state = {'type': 'normal'}

        self.menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.prepare_player_list_menu()
    
    def prepare_player_list_menu(self):
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=self.menu_theme)
        for player in self.app.players.keys():
            self.menu.add_button('{}: {}'.format(player,self.app.players[player]['score']), lambda: self.handle_choose_player(player))

    def prepare_invite_menu(self):
        self.invite_menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Game request', theme=self.menu_theme)

        player_name = self.state['packet']['name']

        self.invite_menu.add_label(f"{player_name} would like to play with you")
        self.invite_menu.add_button('Accept', self.handle_accept_invite)
        self.invite_menu.add_button('Decline', self.handle_reject_invite)
    
    def handle_accept_invite(self):
        self.app.player_name = self.state['packet']['name']
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(self.app.my_name, self.app.network.ip, True)))
        self.app.scene = scenes.PlayScene(self.app, is_my_turn=True, my_player_number=PLAYER1)

    def handle_reject_invite(self):
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(self.app.my_name, self.app.network.ip, False)))
        self.state = {'type': 'normal'}

    def handle_event(self, event):
        if event.type == 'tcp':
            if event.data['type'] == 'game_request':
                self.state = {'type': 'invited', 'packet': event.data }
                print("preparing invite menu")
                self.prepare_invite_menu()

        if self.state['type'] == 'normal':
            self.menu.update([event])
        elif self.state['type'] == 'invited':
            self.invite_menu.update([event])

    def handle_choose_player(self, player_name):
        print("player name = ", player_name)
        self.app.player_name = player_name
        self.app.scene = scenes.SendRequestScene(self.app)
        
    def update(self):
        if self.state['type'] == 'normal': 
            self.prepare_player_list_menu()

    def draw(self):
        if self.state['type'] == 'normal':
            self.menu.draw(self.app.screen)
        elif self.state['type'] == 'invited':
            self.invite_menu.draw(self.app.screen)
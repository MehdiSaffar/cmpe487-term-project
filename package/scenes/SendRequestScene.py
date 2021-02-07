from package.Packet import game_request_packet, game_cancel_request_packet
from .. import scenes
import pygame
import pygame_menu
from ..constants import *


class SendRequestScene:
    def __init__(self, app):
        self.app = app
        menu_theme = pygame_menu.themes.Theme(
            background_color=Color.LIGHT_BLUE,  # transparent background
            title_shadow=True,
            title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.menu = pygame_menu.Menu(
            SCREEN_HEIGHT, SCREEN_WIDTH, 'Waiting...', theme=menu_theme)
        self.menu.add_label(f'Sending request to {self.app.player_name}...')
        self.menu.add_button('Cancel Request', self.cancel_game_request)
        self.send_game_request()

    def send_game_request(self):
        ip = self.app.get_other_player_ip()
        packet = game_request_packet(self.app.my_name, self.app.network.ip)
        self.app.network.send(('tcp', ip, packet))

    def handle_game_reply(self, event):
        if event.data['has_accepted']:  # accepts
            self.app.scene = scenes.PlayScene(
                self.app, is_my_turn=False, my_player_number=PLAYER2)
        else:
            self.app.scene = scenes.PopupScene(self.app, 'request_declined', self.app.player_name)

    def handle_event(self, event):
        self.menu.update([event])
        if(event.type == 'tcp'):
            if event.data['type'] == 'game_reply':
                if event.data['name'] == self.app.player_name:
                    self.handle_game_reply(event)
        elif event.type == 'udp':
            if event.data['type'] == 'goodbye':
                if event.data['name'] == self.app.player_name:
                    self.handle_goodbye_from_other_player()


    def handle_goodbye_from_other_player(self):
        self.app.scene = scenes.PopupScene(
            self.app, 'request_declined', self.app.player_name)

    def handle_cancel_game_request(self, event):
        self.app.scene = scenes.PopupScene(
            self.app, 'request_declined', self.app.player_name)

    def cancel_game_request(self):
        ip = self.app.get_other_player_ip()
        packet = game_cancel_request_packet(
            self.app.my_name, self.app.network.ip)
        self.app.network.send(('tcp', ip, packet))
        self.app.scene = scenes.LobbyScene(self.app)

    def update(self):
        pass

    def draw(self):
        self.menu.draw(self.app.screen)

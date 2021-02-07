from package.Packet import game_request_packet,discover_packet, game_reply_packet
from .. import scenes
import pygame
import pygame_menu
from ..constants import *

class PopupScene:
    def __init__(self, app, player_won):
        self.app = app
        self.player_won = player_won
        self.text = None
        self.text_rect = None
        self.menu = None
        self.lobby = scenes.LobbyScene(self.app)
        self.menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)
        print("Game ended: ",player_won)
        pygame.display.set_caption('Game ended')
        if player_won == 1:
            self.show_result_popup(True)
        elif player_won == 2:
            self.show_result_popup(False)
        else:
            self.show_result_popup(None)

    def show_result_popup(self, i_won):
        if i_won == None:
            self.increase_my_score()
            menu_theme = pygame_menu.themes.Theme(
                background_color=Color.LIGHT_SLATE_GRAY,
                title_font_size=18,
                title_background_color=Color.DARK_GRAY_2,
                widget_font_color=Color.WHITE,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)
            self.menu = pygame_menu.Menu(SCREEN_HEIGHT//2, SCREEN_WIDTH//2, 'It\'s a Tie!!', theme=menu_theme)
        else:
            if i_won:
                self.increase_my_score()
                menu_theme = pygame_menu.themes.Theme(
                    background_color=Color.PALE_GREEN,
                    title_font_size=18,
                    title_background_color=Color.DARK_GREEN,
                    widget_font_color=Color.WHITE,
                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)
                self.menu = pygame_menu.Menu(SCREEN_HEIGHT//2, SCREEN_WIDTH//2, f'Congratulations you won!!!', theme=menu_theme)
            else:
                self.increase_my_score()
                menu_theme = pygame_menu.themes.Theme(
                            title_font_size=18,
                            background_color=Color.INDIAN_RED,
                            title_background_color=Color.DARK_RED,
                            widget_font_color=Color.WHITE,
                            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)
                self.menu = pygame_menu.Menu(SCREEN_HEIGHT//2, SCREEN_WIDTH//2, f'Sorry, game over...', theme=menu_theme)
        self.menu.add_button('Rematch', self.handle_rematch)
        self.menu.add_button('Return to Lobby', self.handle_return_to_lobby)

    def handle_return_to_lobby(self):
        self.app.scene = scenes.LobbyScene(self.app)

    def handle_rematch(self):
        self.app.scene = scenes.SendRequestScene(self.app)

    def increase_my_score(self):
        self.app.my_all_scores[self.app.my_name] +=10
        self.app.players[self.app.player_name]['score'] -= 10
        self.app.write_my_score_into_file()
        print("my score: ", self.app.my_all_scores[self.app.my_name])

    def decrease_my_score(self):
        self.app.my_all_scores[self.app.my_name] -= 10
        self.app.players[self.app.player_name]['score'] += 10
        self.app.write_my_score_into_file()
        print("my score: ", self.app.my_all_scores[self.app.my_name])

    def handle_event(self, event):
        if event.type == 'tcp':
            if event.data['type'] == 'game_request':
                self.state = {'type': 'invited', 'packet': event.data }
                print("preparing invite menu")
                self.prepare_rematch_invite_menu()
        self.menu.update([event])

    def prepare_rematch_invite_menu(self):
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Game request', theme=self.menu_theme)
        player_name = self.state['packet']['name']
        self.menu.add_label(f"{player_name} wants a rematch")
        self.menu.add_button('Accept', self.handle_accept_invite)
        self.menu.add_button('Decline', self.handle_reject_invite)

    def handle_accept_invite(self):
        self.app.player_name = self.state['packet']['name']
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(self.app.my_name, self.app.network.ip, True)))
        self.app.scene = scenes.PlayScene(self.app, is_my_turn=True, my_player_number=PLAYER1)

    def handle_reject_invite(self):
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(self.app.my_name, self.app.network.ip, False)))
        self.state = {'type': 'normal'}

    def update(self):
        pass

    def draw(self):
        self.menu.draw(self.app.screen)
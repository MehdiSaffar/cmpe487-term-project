from ..constants import *
from .. import scenes
from ..Board import *
from ..scenes.PopupScene import PopupScene
from ..Packet import game_move_packet


class PlayScene:
    def __init__(self, app, is_my_turn, my_player_number):
        self.app = app
        self.app.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = Board(self)
        self.is_my_turn = is_my_turn
        self.my_player_number = my_player_number
        self.is_game_finished = False
        self.is_draw = False
        self.winning_player_number = None

    @property
    def current_player(self):
        return 1 if self.is_my_turn else 2

    def handle_event(self, event):
        if event.type == 'tcp':
            if event.data['type'] == 'game_move':
                self.handle_other_player_game_move(event.data)
        elif event.type == 'udp':
            if event.data['type'] == 'goodbye':
                if event.data['name'] == self.app.player_name:
                    self.handle_goodbye_from_other_player()
        self.board.handle_event(event)

    def handle_goodbye_from_other_player(self):
        self.app.scene = scenes.PopupScene(self.app, 'game_aborted', self.app.player_name)

    def handle_other_player_game_move(self, packet):
        col = packet['col']
        self.board.try_put_piece(col)
        self.toggle_current_player()

    def handle_piece_placed(self, col):
        ip = self.app.get_other_player_ip()
        packet = game_move_packet(self.app.my_name, self.app.network.ip, col)
        self.app.network.send(('tcp', ip, packet))
        # if not self.is_game_finished:
        self.toggle_current_player()

    def toggle_current_player(self):
        self.is_my_turn = not self.is_my_turn

    def update(self):
        self.board.update()
        if self.is_game_finished:
            time.sleep(1)
            win_state = 'win' if self.winning_player_number == 1 else 'lose' if self.winning_player_number == 2 else 'draw'
            self.app.scene = scenes.PopupScene(self.app, win_state, self.app.player_name)

    def draw(self):
        self.board.draw(self.app.screen)
        self.add_text()

    def add_text(self):
        font = pygame.font.SysFont('Courier', 18, bold=True)

        # create a text surface object,
        # on which text is drawn on it.
        if(self.is_my_turn):
            my_name = font.render(
                'player 1: '+self.app.my_name, True, Color.YELLOW)
            player_name = font.render(
                'player 2: '+self.app.player_name, True, Color.WHITE)
        else:
            my_name = font.render(
                'player 1: '+self.app.my_name, True, Color.WHITE)
            player_name = font.render(
                'player 2: '+self.app.player_name, True, Color.YELLOW)

        # create a rectangular object for the
        # text surface object
        my_name_text_rect = my_name.get_rect()
        player_name_text_rect = player_name.get_rect()

        # set the center of the rectangular object.
        my_name_text_rect.center = (SCREEN_WIDTH - 150, 50)
        player_name_text_rect.center = (SCREEN_WIDTH - 150, 100)

        self.app.screen.blit(my_name, my_name_text_rect)
        self.app.screen.blit(player_name, player_name_text_rect)

from ..constants import *
import . as scenes
from ..Board import *


class PlayScene:
    def __init__(self, app):
        self.app = app
        self.app.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT),pygame.RESIZABLE)
        self.board = Board(self)
        self.current_player = 1

    def handle_event(self, event):
        self.board.handle_event(event)

    def toggle_current_player(self):
        self.current_player = 1 if self.current_player == 2 else 2

    def update(self):
        self.board.update()

    def draw(self):
        self.board.draw(self.app.screen)
        self.add_text()

    def add_text(self):
        font = pygame.font.SysFont('Courier', 18,bold=True)
        
        # create a text suface object,
        # on which text is drawn on it.
        if(self.current_player == 1):
            my_name = font.render('player 1: '+self.app.my_name, True, Color.YELLOW)
            player_name = font.render('player 2: '+self.app.player_name, True, Color.WHITE)
        else:
            my_name = font.render('player 1: '+self.app.my_name, True, Color.WHITE)
            player_name = font.render('player 2: '+self.app.player_name, True, Color.YELLOW)
        # create a rectangular object for the
        # text surface object
        my_name_text_rect = my_name.get_rect()
        player_name_text_rect = player_name.get_rect()
        # set the center of the rectangular object.
        my_name_text_rect.center = (SCREEN_WIDTH - 150, 50)
        player_name_text_rect.center = (SCREEN_WIDTH - 150, 100)
        self.app.screen.blit(my_name, my_name_text_rect)
        self.app.screen.blit(player_name, player_name_text_rect)
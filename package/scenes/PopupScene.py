from package.Packet import game_request_packet
from .. import scenes
import pygame
from ..constants import *

class PopupScene:
    def __init__(self, app, i_won):
        self.app = app
        self.player_won = i_won
        self.text = None
        self.text_rect = None
        print("Game ended: ",i_won)
        pygame.display.set_caption('Game ended')
        if i_won:
            self.show_winning_popup()
        else:
            self.show_losing_popup()
      

    def show_winning_popup(self):
        font = pygame.font.SysFont('Courier', 18, bold=True)
        self.text = font.render(f'Congratulations you won!!!', True, Color.WHITE, Color.LIGHT_BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def show_losing_popup(self):
        font = pygame.font.SysFont('Courier', 18, bold=True)
        self.text = font.render(f'Player {self.app.player_name} has won, game over...', True, Color.WHITE, Color.LIGHT_BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def handle_event(self, event):
        pass
                
        
    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.text, self.text_rect)
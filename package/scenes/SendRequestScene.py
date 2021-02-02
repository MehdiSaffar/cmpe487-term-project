from ..scenes.PlayScene import PlayScene
import pygame
from ..constants import *

class SendRequestScene:
    def __init__(self, app):
        self.app = app
        pygame.display.set_caption('Waiting...')
        font = pygame.font.SysFont('Courier', 18,bold=True)
        
        # create a text suface object,
        # on which text is drawn on it.
        self.text = font.render('Sending request to {}...'.format(self.app.player_name), True, Color.WHITE, Color.LIGHT_BLUE)
        
        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        
        # set the center of the rectangular object.
        self.textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
    def handle_event(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            self.app.scene = PlayScene(self.app)
        
    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.text, self.textRect)
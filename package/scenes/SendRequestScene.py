from package.Packet import game_request_packet
from .. import scenes
import pygame
from ..constants import *

class SendRequestScene:
    def __init__(self, app):
        self.app = app

        pygame.display.set_caption('Waiting...')
        font = pygame.font.SysFont('Courier', 18, bold=True)
        
        # create a text suface object,
        # on which text is drawn on it.
        self.text = font.render(f'Sending request to {self.app.player_name}...', True, Color.WHITE, Color.LIGHT_BLUE)
        
        # create a rectangular object for the
        # text surface object
        self.text_rect = self.text.get_rect()
        
        # set the center of the rectangular object.
        self.text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.send_game_request()

    
    def send_game_request(self):
        ip = self.app.get_other_player_ip()
        packet = game_request_packet(self.app.my_name, self.app.network.ip)
        self.app.network.send(('tcp', ip, packet)) 
    
    
    def handle_game_reply(self, event):
        if event.data['has_accepted']: # accepts
            self.app.scene = scenes.PlayScene(self.app, is_my_turn=False, my_player_number=PLAYER2)
        else:
            self.app.scene = scenes.LobbyScene(self.app)

    def handle_event(self, event):
        if(event.type == 'tcp'):
            if (event.data['type'] == 'game_reply'):
                self.handle_game_reply(event)
        
    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.text, self.text_rect)
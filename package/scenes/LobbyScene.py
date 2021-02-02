from ..constants import *
from ..scenes.SendRequestScene import SendRequestScene
import pygame
import pygame_menu

class LobbyScene:
   

    def __init__(self, app):
        self.app = app
        self.players = []
        self.is_player_chosen = False
        players = [("buse",1), ("mehdi",2)]
        mytheme = pygame_menu.themes.Theme(background_color=Color.LIGHT_BLUE, # transparent background
                title_shadow=True,
                title_background_color=(4, 47, 126),widget_font_color=Color.WHITE)
        self.menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Connect 4', theme=mytheme)
        self.menu.add_text_input('Username : ', default='',onchange=self.get_my_user_name)
        self.menu.add_selector('Choose Player :', players, onchange=self.choose_player)
        self.menu.add_button('Play', self.start_the_game)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def get_my_user_name(self,name):
        self.app.my_name = name

    def handle_event(self, event):
        if(not self.is_player_chosen):
            self.menu.update([event])
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print("in play")
            #self.app.scene = self.app.scenes['Play']
        
    def update(self):
        pass

    def draw(self):
        if(not self.is_player_chosen):
            self.menu.draw(self.app.screen)
        

    def choose_player(self, player_name, player_number):
        self.app.player_name = player_name[0][0]
        print("player name = ",player_name[0][0])
        

    def start_the_game(self):
        pygame_menu.events.EXIT
        self.is_player_chosen = True
        print("app player name: ",self.app.player_name)
        print("sending game request...")
        self.app.scene = SendRequestScene(self.app)
        pygame.display.update()
        pygame.display.flip()
        

    #def addText(self,text):
    #    self.font = pygame.font.SysFont('Arial', 25)
    #    self.surface.blit(self.font.render(str(text), True, (255,0,0)), (200, 100))
    #    pygame.display.flip()
        

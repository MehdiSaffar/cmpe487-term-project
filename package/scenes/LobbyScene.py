from ..constants import *
import pygame
import pygame_menu

class LobbyScene:
   

    def __init__(self, app):
        self.app = app
        self.players = []
        self.is_player_chosen = False
        #font = pygame.font.SysFont('Arial', 25)
        players = [("buse",1), ("mehdi",2)]
        self.menu = pygame_menu.Menu(300, 300, 'Welcome', theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add_text_input('Username : ', default='')
        self.menu.add_selector('Choose Player :', players, onchange=self.choose_player)
        self.menu.add_button('Play', self.start_the_game)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def handle_event(self, event):
        global is_player_chosen
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print("in play")
            #self.app.scene = self.app.scenes['Play']
            

    def update(self):
        pass

    def draw(self):
        print("mainloop")
        if(self.is_player_chosen==False):
            self.menu.mainloop(self.app.screen,bgfun=self.draw,disable_loop=True)
        else:
            return

    def choose_player(self, player_name, player_number):
        self.is_player_chosen = True
        print(player_name)
        

    #def addText(self,player_name):
    #    self.surface.blit(self.font.render(str(player_name), True, (255,0,0)), (200, 100))
    #    pygame.display.update()

    def start_the_game(self):
        pygame_menu.events.EXIT
        self.is_player_chosen = True
        print("sending game request...")
        self.app.scene = self.app.scenes['Play']
        pygame.display.update()
        pygame.display.flip()
        

    #def addText(self,text):
    #    self.font = pygame.font.SysFont('Arial', 25)
    #    self.surface.blit(self.font.render(str(text), True, (255,0,0)), (200, 100))
    #    pygame.display.flip()

    def show_players(self):
        self.menu.draw(self.app.screen)
        

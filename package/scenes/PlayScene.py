from ..constants import *

from ..Board import *


class PlayScene:
    def __init__(self, app):
        print("in play")
        self.app = app
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
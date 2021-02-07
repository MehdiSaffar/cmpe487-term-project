import numpy as np
import pygame
import time

from .constants import Color, root_path, SCREEN_HEIGHT,SCREEN_WIDTH,PLAYER1 ,PLAYER2
from .Piece import Piece


class Board:
    ROWS = 6
    COLS = 7
    

    def __init__(self, scene):
        self.grid = np.zeros((self.ROWS, self.COLS), np.int8)
        self.board_img = pygame.image.load(str(root_path / 'assets' / 'Connect4Board.png'))
        self.scene = scene
        self.board_img = pygame.transform.scale(self.board_img, (SCREEN_WIDTH - 300, SCREEN_HEIGHT))

    def get_empty_row(self, col):
        """
        Gets first empty row
        Return -1 if full
        """
        row = 0
        while row < self.ROWS and self.grid[row][col] == 0:
            row += 1
        return row - 1

    def put_piece(self, pos, player):
        row, col = pos
        self.grid[row][col] = player
        winning_pieces = self.check_winning_condition(pos, player)
        #print("Grid: \n", self.grid)
        return winning_pieces

    def check_winning_condition(self, pos, player):
        _col = self.check_col_is_winning(pos, player)
        _row = self.check_row_is_winning(pos, player)
        _rdi = self.check_right_diag_is_winning(pos, player)
        _ldi = self.check_left_diag_is_winning(pos, player)

        #print(f"{_col=} {_row=} {_rdi=} {_ldi=}")

        indexes = [
            *_col,
            *_row,
            *_rdi,
            *_ldi,
        ]

        indexes = map(tuple, indexes)
        indexes = set(indexes)
        return list(map(np.array, indexes))

    def is_board_full(self):
        if 0 in self.grid[0]:
            return False
        return True
        
    def try_put_piece(self, col):
        empty_row = self.get_empty_row(col)
        if empty_row == -1:  # Do nothing
            return []

        pos = np.array((empty_row, col))
        #print(f'{pos=}')
        self.winning_indexes = self.put_piece(pos, self.scene.current_player)
        if len(self.winning_indexes) > 0:
                print("game finished is winner me: ",self.scene.current_player)
                self.scene.winning_player_number = self.scene.current_player
                if self.is_board_full():
                    self.scene.is_game_finished = True
        return self.winning_indexes

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scene.is_my_turn:
                col, row = np.array(pygame.mouse.get_pos()) // Piece.DIAMETER
                self.winning_indexes = self.try_put_piece(col)
                print(self.winning_indexes)
                self.scene.handle_piece_placed(int(col))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(Color.DARK_GRAY)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                pos = np.array((row, col))
                screen_pos = np.array((col, row))
                screen_pos = screen_pos * Piece.DIAMETER + Piece.RADIUS

                # color =
                if self.at(pos) == 1:
                    if tuple(pos) in list(map(tuple, self.winning_indexes)):
                        pygame.draw.circle(screen, Color.GREEN, screen_pos, Piece.RADIUS)
                        self.scene.is_game_finished = True
                    else:
                        pygame.draw.circle(screen, Color.RED, screen_pos, Piece.RADIUS)
                elif self.at(pos) == 2:
                    if tuple(pos) in list(map(tuple, self.winning_indexes)):
                        pygame.draw.circle(screen, Color.GREEN, screen_pos, Piece.RADIUS)
                        self.scene.is_game_finished = True
                    else:
                        pygame.draw.circle(screen, Color.YELLOW, screen_pos, Piece.RADIUS)

        screen.blit(self.board_img, (0, 0))


    def is_within_bounds(self, pos):
        """
        Returns True if pos within bounds of the board
        """
        row, col = pos
        return (0 <= row and row < self.ROWS) and (0 <= col and col < self.COLS)

    def at(self, pos):
        """
        Returns element found at pos = (row, col)
        """
        row, col = pos
        return self.grid[row][col]

    def check_right_diag_is_winning(self, pos, player):
        row, col = pos
        min_diff = min(row, self.COLS - col - 1)

        row = row - min_diff
        col = col + min_diff

        while self.is_within_bounds((row, col)):
            winning_indexes = []
            while self.is_within_bounds((row, col)) and self.at((row, col)) == player:
                winning_indexes.append(np.array((row, col)))
                row += 1
                col -= 1

            if len(winning_indexes) >= 4:
                return winning_indexes

            row += 1
            col -= 1

        return []

    def check_left_diag_is_winning(self, pos, player):
        row, col = pos
        min_diff = min(row, col)
        row, col = np.array((row - min_diff, col - min_diff))

        while self.is_within_bounds((row, col)):
            winning_indexes = []
            while self.is_within_bounds((row, col)) and self.at((row, col)) == player:
                winning_indexes.append(np.array((row, col)))
                row += 1
                col += 1

            if len(winning_indexes) >= 4:
                return winning_indexes

            row += 1
            col += 1
        return []

    def check_col_is_winning(self, pos, player):
        row, col = pos
        for row in range(self.ROWS):
            winning_indexes = []
            while row < self.ROWS and self.at((row, col)) == player:
                winning_indexes.append(np.array((row, col)))
                row += 1

            if len(winning_indexes) >= 4:
                return winning_indexes

        return []

    def check_row_is_winning(self, pos, player):
        row, col = pos
        for col in range(self.COLS):
            winning_indexes = []
            while col < self.COLS and self.at((row, col)) == player:
                winning_indexes.append(np.array((row, col)))
                col += 1

            if len(winning_indexes) >= 4:
                return winning_indexes

        return []

import numpy
import pygame, sys
from pygame.locals import *

class Color:
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = ((255,255,0))
    DARK_GRAY = ((50,50,50))

class Piece:
    DIAMETER = 23
    def __init__(self, color):
        self.color = color

    def draw(self, DISPLAYSURF, x, y):
        pygame.draw.circle(DISPLAYSURF, self.color, (y*50+25,x*50+25), self.DIAMETER)  

class Board:
    ROWS = 6
    COLS = 7
    PLAYER1 = 1
    PLAYER2 = 2
    

    def __init__(self):
        self.grid = numpy.zeros((self.ROWS, self.COLS), numpy.int8)

    def canPutPiece(self,col):
        i = 0
        if self.grid[i][col] == 0:
            while i < self.ROWS and self.grid[i][col] == 0:
                i += 1
            return i - 1
        else:
            return -1

    def checkWinningCondition(self,row,col,player):
        winning_indexes = []
        winning_indexes = self.checkColIsWinning(col,player)
        if len(winning_indexes)>0:
            return winning_indexes

        winning_indexes = self.checkRowIsWinning(row,player)
        if len(winning_indexes)>0:
            return winning_indexes

        winning_indexes = self.checkRightDiagonalIsWinning(row,col,player)
        if len(winning_indexes)>0:
            return winning_indexes

        winning_indexes = self.checkLeftDiagonalIsWinning(row,col,player)
        if len(winning_indexes)>0:
            return winning_indexes

        return winning_indexes

    def putPiece(self,col, player):
        row = self.canPutPiece(col)
        if row != -1:
            self.grid[row][col] = player
        winning = self.checkWinningCondition(row,col,player)
        print("Grid: \n", self.grid)
        return row, col, winning

    def draw(self):
        # Initialize program
        image = pygame.image.load(r'C:\Users\busekabakoglu\Cmpe487Final\CMPE487_term_project\Connect4Board.png')
        image = pygame.transform.scale(image, (350, 300))
        pygame.init()
        player = 1
        # Assign FPS a value
        FPS = 60
        FramePerSec = pygame.time.Clock()
        # Setup a 300x300 pixel display with caption
        DISPLAYSURF = pygame.display.set_mode((350,300))
        DISPLAYSURF.fill(Color.DARK_GRAY)
        DISPLAYSURF.blit(image, (0, 0)) 
        pygame.display.set_caption("Example")
        # Main Loop
        while True:
            # Listen to events part
            for event in pygame.event.get():
                self.drawAllBoard(DISPLAYSURF)
                if event.type == QUIT:
                    # Handle event part
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[1] // 50
                    y = pos[0] // 50
                    x, y, winning_indexes = self.putPiece(y,player)
                    if len(winning_indexes)>0:
                        print("player ",player," wins!!")
                    if(x == -1):
                        print("You cannot put here!!")
                    else:
                        #DISPLAYSURF.fill(WHITE)
                        new_piece = None
                        if(player == self.PLAYER1):
                            new_piece = Piece(Color.RED)
                            player = self.PLAYER2
                        else:
                            new_piece = Piece(Color.YELLOW)
                            player = self.PLAYER1
                        new_piece.draw(DISPLAYSURF, x, y)

            # Draw part
            #pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (130,170))
            #pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (170,170))
            #pygame.draw.line(DISPLAYSURF, GREEN, (130,170), (170,170))
            #x += 1
            #x %= 300
            DISPLAYSURF.blit(image, (0, 0)) 
            #pygame.draw.circle(DISPLAYSURF, BLACK, (x,y), 30)
            #pygame.draw.circle(DISPLAYSURF, BLACK, (200,50), 30)
            #pygame.draw.rect(DISPLAYSURF, RED, (100, 200, 100, 50), 2)
            #pygame.draw.rect(DISPLAYSURF, BLACK, (110, 260, 80, 5))
            pygame.display.update()
            FramePerSec.tick(FPS)

    def drawAllBoard(self, DISPLAYSURF):
        for i in range(0, self.ROWS-1):
            for j in range(0,self.COLS-1):
                if self.grid[i][j] == 1:
                    pygame.draw.circle(DISPLAYSURF, Color.RED, (j*50+25,i*50+25), 22)

    def checkRightDiagonalIsWinning(self,row, col, player):
        winning_indexes = []
        minDiff = min(row,self.COLS-col-1)
        row = row - minDiff
        col = col + minDiff
        while row < self.ROWS and col < self.COLS and row >= 0 and col >= 0:
            winning_indexes = []
            if self.grid[row][col] == player:
                while row < self.ROWS and col < self.COLS and row >= 0 and col >= 0 and self.grid[row][col] == player:
                    winning_indexes.append([row, col])
                    row += 1
                    col -= 1
                    if len(winning_indexes) == 4:
                        return winning_indexes
            else:
                winning_indexes = []
                row += 1
                col -= 1
        return []


    def checkLeftDiagonalIsWinning(self,row, col, player):
        winning_indexes = []
        minDiff = min(row,col)
        row = row - minDiff
        col = col - minDiff
        while row < self.ROWS and col < self.COLS and row >= 0 and col >= 0:
            winning_indexes = []
            if self.grid[row][col] == player:
                while row < self.ROWS and col < self.COLS and row >= 0 and col >= 0 and self.grid[row][col] == player:
                    winning_indexes.append([row, col])
                    row += 1
                    col += 1
                    if len(winning_indexes) == 4:
                        return winning_indexes
            else:
                winning_indexes = []
                row += 1
                col += 1
        return []


    def checkColIsWinning(self, col, player):
        winning_indexes = []
        for row in range(0, self.ROWS):
            if self.grid[row][col] == player:
                while row < self.ROWS and self.grid[row][col] == player:
                    winning_indexes.append([row, col])
                    row += 1
                if len(winning_indexes) < 4:
                    winning_indexes = []
        return winning_indexes

    def checkRowIsWinning(self, row, player):
        winning_indexes = []
        for col in range(self.COLS):
            if self.grid[row][col] == player:
                while col < self.COLS and self.grid[row][col] == player:
                    winning_indexes.append([row, col])
                    col += 1
                if len(winning_indexes) < 4:
                    winning_indexes = []
        return winning_indexes

def main():
    board = Board()
    board.draw()

main()
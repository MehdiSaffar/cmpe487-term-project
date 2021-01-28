import numpy
import pygame, sys
from pygame.locals import *

ROWS = 6
COLS = 7
PLAYER1 = 1
PLAYER2 = 2
grid = numpy.zeros((ROWS,COLS))

def canPutPiece(col):
    i = 0
    if grid[i][col] == 0:
        while i < ROWS and grid[i][col] == 0:
            i += 1
        return i - 1
    else:
        return -1


def putPiece(col, player):
    row = canPutPiece(col)
    grid[row][col] = player
    return row, col

def draw():
    # Initialize program
    image = pygame.image.load(r'C:\Users\busekabakoglu\Cmpe487Final\CMPE487_term_project\Connect4Board.png')
    image = pygame.transform.scale(image, (350, 300))
    pygame.init()
    
    # Assign FPS a value
    FPS = 60
    FramePerSec = pygame.time.Clock()
    
    # Setting up color objects
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Setup a 300x300 pixel display with caption
    DISPLAYSURF = pygame.display.set_mode((350,300))
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(image, (0, 0)) 
    pygame.display.set_caption("Example")
    
    x = 0
    y = 0
    # Main Loop
    while True:
        # Listen to events part
        for event in pygame.event.get():
            if event.type == QUIT:
                # Handle event part
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[1] // 50
                y = pos[0] // 50
                x, y = putPiece(y,PLAYER1)
                if(x == -1):
                    print("You cannot put here!!")
                else:
                    DISPLAYSURF.fill(WHITE)
                    for i in (0, ROWS-1):
                        for j in (0,COLS-1):
                            if(grid[i][j] != 0):
                                pygame.draw.circle(DISPLAYSURF, RED, (i*50+25,j*50+25), 22)
                print (x, y)
                            

    
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


def checkDiagonalIsWinning(row, col, player):
    winning_indexes = []
    minDiff = min(row,col)
    row = row - minDiff
    col = col - minDiff
    while row < ROWS and col < COLS:
        if grid[row][col] == player:
            winning_indexes.append([row, col])
            while row < ROWS and col < COLS and grid[row][col] == player:
                winning_indexes.append([row, col])
                row += 1
                col += 1
            if len(winning_indexes) < 4:
                winning_indexes = []
    return winning_indexes


def checkColIsWinning(col, player):
    winning_indexes = []
    for row in range(ROWS):
        if grid[row][col] == player:
            winning_indexes.append([row, col])
            while grid[row][col] == player:
                winning_indexes.append([row, col])
            if len(winning_indexes) < 4:
                winning_indexes = []
    return winning_indexes

def checkRowIsWinning(row, player):
    winning_indexes = []
    for col in range(COLS):
        if grid[row][col] == player:
            winning_indexes.append([row, col])
            while grid[row][col] == player:
                winning_indexes.append([row, col])
            if len(winning_indexes) < 4:
                winning_indexes = []
    return winning_indexes

draw()
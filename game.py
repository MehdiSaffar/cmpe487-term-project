import pygame, sys
from pygame.locals import *
 
# Initialize program
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
DISPLAYSURF = pygame.display.set_mode((300,300))
DISPLAYSURF.fill(WHITE)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y += 1 
            elif event.key == pygame.K_UP:
                y -= 1             

   
    # Draw part
    #pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (130,170))
    #pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (170,170))
    #pygame.draw.line(DISPLAYSURF, GREEN, (130,170), (170,170))
    x += 1
    x %= 300
    DISPLAYSURF.fill(WHITE)
    pygame.draw.circle(DISPLAYSURF, BLACK, (x,y), 30)
    #pygame.draw.circle(DISPLAYSURF, BLACK, (200,50), 30)
    #pygame.draw.rect(DISPLAYSURF, RED, (100, 200, 100, 50), 2)
    #pygame.draw.rect(DISPLAYSURF, BLACK, (110, 260, 80, 5))
    pygame.display.update()

    FramePerSec.tick(FPS)
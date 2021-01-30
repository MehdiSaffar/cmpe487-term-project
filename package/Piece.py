import pygame


class Piece:
    RADIUS = 25
    DIAMETER = RADIUS * 2

    def __init__(self, color):
        self.color = color

    def draw(self, screen, pos):
        screen_pos = pos * Piece.DIAMETER + Piece.RADIUS,
        pygame.draw.circle(screen, self.color, screen_pos, self.RADIUS)

import pygame

pygame.init()


class CircleGUI:
    def __init__(self, coordinate, radius, color):
        self.coordinate = coordinate
        self.radius = radius
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.coordinate, self.radius)

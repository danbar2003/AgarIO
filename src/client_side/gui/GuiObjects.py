import pygame

pygame.init()


class CircleGUI:
    def __init__(self, coordinate, radius, color):
        self.coordinate = coordinate
        self.radius = radius
        self.color = color

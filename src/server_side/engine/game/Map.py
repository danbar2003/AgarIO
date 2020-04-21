from random import randrange
from math import sqrt

from server_side.engine.game import Constants
from server_side.engine.game.Player import Player


def create_random_points():
    center = Point(0, 0)
    points = []
    for x in range(Constants.MAP_RADIOS):
        for y in range(Constants.MAP_RADIOS):
            point = Point(x, y)
            if point.distance(center) < Constants.MAP_RADIOS:
                if randrange(100) < Constants.POINTS_DENSITY * 100:
                    points.append(point)
    return points


class Map:
    def __init__(self, radios=Constants):
        self.points = create_random_points()
        self.radios = radios
        self.players = []


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

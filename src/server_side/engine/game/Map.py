from random import randrange

from server_side.engine.game import Constants
from server_side.engine.game.Point import Point
from server_side.engine.game.Player import Player

HYPOTHESIS_SPAWN_POINTS = []


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


def create_hypothesis_spawn_points():
    for y in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        HYPOTHESIS_SPAWN_POINTS.append(Point(0, y))
    for x in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        HYPOTHESIS_SPAWN_POINTS.append(Point(x, 0))


def exec_instructions(player, player_instructions):
    dup, move_vector = player_instructions  # TODO - make mouse loc a point object
    if dup:
        player.duplicate(move_vector)
    else:
        player.move(move_vector)


class Map:

    def create_id(self):
        return len(self.players)

    def someone_contains(self, point):
        for player in self.players:
            for circle in player.circles:
                if circle.contains(point):
                    return True

    def create_spawn_point(self):
        for point in HYPOTHESIS_SPAWN_POINTS:
            if not self.someone_contains(point):  # no one contains the point
                return point

    def __init__(self, radios=Constants.MAP_RADIOS):
        create_hypothesis_spawn_points()
        self.points = create_random_points()
        self.radios = radios
        self.players = []

    def create_new_player(self):
        player = Player(spawn_point=self.create_spawn_point(), player_id=self.create_id(), color=0)  # TODO - color
        self.players.append(player)
        return player

    def player_interactions(self):
        pass

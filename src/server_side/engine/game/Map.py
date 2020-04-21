from random import randrange

from server_side.engine.game import Constants
from server_side.engine.game.Point import Point
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


def create_hypothesis_spawn_points():
    hypothesis_spawn_points = []
    for y in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        hypothesis_spawn_points.append(Point(0, y))
    for x in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        hypothesis_spawn_points.append(Point(x, 0))
    return hypothesis_spawn_points


class Map:

    def create_id(self):
        return len(self.players)

    def someone_contains(self, point):
        for player in self.players:
            for circle in player.circles:
                if circle.contains(point):
                    return True

    def create_spawn_point(self):
        for point in create_hypothesis_spawn_points():
            if not self.someone_contains(point):  # no one contains the point
                return point

    def __init__(self, radios=Constants.MAP_RADIOS):
        self.points = create_random_points()
        self.radios = radios
        self.players = []

    def create_new_player(self):
        player = Player(spawn_point=self.create_spawn_point(), player_id=self.create_id(), color=0)  # TODO - color
        self.players.append(player)
        return player

    def exec_instructions(self, player, player_instructions):
        dup, mouse_vector = player_instructions
        if dup:
            player.duplicate(mouse_vector, self.radios)
        else:
            player.move(mouse_vector, self.radios)

    def player_interactions(self):
        pass

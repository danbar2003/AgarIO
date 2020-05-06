import random
import threading
import math

from engine.game import Constants
from engine.game.Point import Point
from engine.game.Player import Player


def create_random_points():
    list_of_points = []
    for i in range(Constants.NUM_OF_POINTS):
        x = random.randint(-Constants.MAP_RADIOS, Constants.MAP_RADIOS)
        height = int(math.sqrt((Constants.MAP_RADIOS ** 2) - (x ** 2)))
        y = random.randint(-height, height)
        list_of_points.append(Point(x, y))

    return list_of_points


def create_hypothesis_spawn_points():
    hypothesis_spawn_points = []
    for y in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        hypothesis_spawn_points.append(Point(0, y))
    for x in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS, 100):
        hypothesis_spawn_points.append(Point(x, 0))
    return hypothesis_spawn_points


class Map:
    colors = {0: (0, 255, 0),
              1: (0, 0, 255),
              2: (60, 181, 255),
              3: (60, 20, 101),
              4: (50, 50, 50),
              5: (60, 60, 60),
              6: (70, 70, 70),
              7: (80, 80, 80),
              8: (90, 90, 90),
              9: (100, 100, 100),
              10: (110, 110, 110),
              11: (120, 120, 120),
              12: (130, 130, 130),
              13: (140, 140, 140),
              14: (150, 150, 150),
              15: (160, 160, 160),
              16: (170, 170, 170),
              17: (180, 180, 180),
              18: (190, 190, 190),
              19: (200, 200, 200),
              20: (210, 210, 210)}

    def __init__(self, radios=Constants.MAP_RADIOS):
        self.points = create_random_points()
        self.radios = radios
        self.players = []
        threading.Thread(target=self.player_interactions, args=()).start()

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

    def create_new_player(self, res):
        player = Player(spawn_point=Point(0, 0), player_id=self.create_id(),
                        color=Map.colors.get(len(self.players)),
                        resolution=res)  # TODO - color
        self.players.append(player)
        return player

    def exec_instructions(self, player, player_instructions):
        dup, mouse_vector = player_instructions
        if dup:
            player.duplicate(mouse_vector, self.radios)
        else:
            player.move(mouse_vector, self.radios)

    def player_interactions(self):
        while True:
            # player v player
            for player in self.players:
                for circle in player.circles:
                    for enemy_player in self.players:
                        if enemy_player == player:
                            continue
                        for enemy_circle in enemy_player.circles:
                            if circle.contains(enemy_circle.point_coordinate):
                                print(type(enemy_circle))
                                circle.circle_radius = math.sqrt(
                                    circle.circle_radius ** 2 + enemy_circle.circle_radius ** 2)
                                enemy_player.circles.remove(enemy_circle)
            # player v world
            for player in self.players:
                for circle in player.circles:
                    for point in self.points:
                        if circle.contains(point):
                            circle.circle_radius += 1
                            self.points.remove(point)

            # update players speed
            for player in self.players:
                player.minimize_big_circles()

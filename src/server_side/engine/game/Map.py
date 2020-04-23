import random
import threading

from server_side.engine.game import Constants
from server_side.engine.game.Point import Point
from server_side.engine.game.Player import Player


def create_random_points():
    list_of_points = []
    for i in range(-Constants.MAP_RADIOS, Constants.MAP_RADIOS):
        x = random.randint(-Constants.MAP_RADIOS, Constants.MAP_RADIOS)
        y = random.randint(-Constants.MAP_RADIOS, Constants.MAP_RADIOS)
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

    def create_new_player(self):
        player = Player(spawn_point=Point(0, 0), player_id=self.create_id(), color=0)  # TODO - color
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
                            if circle.contains(enemy_circle):
                                circle.circle_radios += enemy_circle.radios
                                enemy_player.circles.remove(enemy_circle)
            # player v world
            for player in self.players:
                for circle in player.circles:
                    for point in self.points:
                        if circle.contains(point):
                            circle.circle_radios += 1
                            self.points.remove(point)

            # update players speed
            for player in self.players:
                # TODO - more work here!!!
                pass

    def to_string(self):
        for player in self.players:
            player.to_string()

from server_side.engine.game.Circle import Circle
from server_side.engine.game.Point import Point


def create_vector(size, vector):  # vector = Point
    pass


class Player:

    def __init__(self, spawn_point, player_id, color):  # etc
        self.player_id = player_id  # id
        self.color = color  # color
        self.speed = 1
        self.circles = []
        self.circles.append(Circle(point_coordinate=spawn_point, circle_id=0))

    def duplicate(self, move_vector):
        self.move(move_vector)
        for circle in self.circles:
            circle.duplicate_circle(move_vector)

    def move(self, move_vector):
        for circle in self.circles:
            next_circles_positions = []
        for circle in self.circles:
            circle.move_circle(self.speed, move_vector)

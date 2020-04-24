from server_side.engine.game.Circle import Circle
from server_side.engine.game.Point import Point
import math

CENTER = Point(0, 0)


class Player:

    def __init__(self, spawn_point, player_id, color):  # etc
        self.player_id = player_id  # id
        self.color = color  # color
        self.speed = 10
        self.circles = []
        self.circles.append(Circle(point_coordinate=spawn_point, circle_id=0))

    def hypothesis_circles_locations(self, vector):
        locations = []
        for circle in self.circles:
            locations.append(circle.hypothesis_location(vector))
        return locations

    def create_vector(self, mouse_vector):  # vector = Point
        base_point = self.circles[0].point_coordinate
        vector = Point(mouse_vector.x - base_point.x, mouse_vector.y - base_point.y)
        size = vector.distance(Point(0, 0))
        vector.x, vector.y = (self.speed / size) * vector.x, (self.speed / size) * vector.y
        return vector

    def duplicate(self, mouse_vector, map_radios):
        self.move(mouse_vector, map_radios)
        # TODO - think about mechanics

    def move(self, mouse_vector, map_radios):
        vector = self.create_vector(mouse_vector=mouse_vector)
        hypothesis_circle_locations = self.hypothesis_circles_locations(vector)
        for point in hypothesis_circle_locations:
            if point.distance(CENTER) > map_radios:
                break
        else:
            for circle in self.circles:
                circle.move_circle(vector)

    def to_string(self):
        print('player_id', self.player_id)
        for circle in self.circles:
            circle.to_string()

    def info_str(self):
        circles = []
        for circle in self.circles:
            circles.append(circle.info_str())
        return f"Player(player_id={self.player_id}, color={self.color}, speed={self.speed}, circles={circles})"

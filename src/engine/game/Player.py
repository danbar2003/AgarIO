from engine.game.Circle import Circle
from engine.game.Point import Point
from engine.game.Constants import *

CENTER = Point(0, 0)


class Player:

    def __init__(self, spawn_point, player_id, color, resolution):  # etc
        self.player_id = player_id  # id
        self.color = color  # color
        self.speed = 4
        self.circles = []
        self.resolution = resolution
        self.circles.append(Circle(point_coordinate=spawn_point, circle_id=0))

    def hypothesis_circles_locations(self, vector):
        locations = []
        for circle in self.circles:
            locations.append(circle.hypothesis_location(vector))
        return locations

    def create_vector(self, mouse_vector):  # vector = Point
        base_point = Point(self.resolution[0] / 2, self.resolution[1] / 2)
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

    def minimize_big_circles(self):
        for circle in self.circles:
            if circle.circle_radius > BIG_CIRCLE_LIMIT:
                circle.circle_radius -= MINIMIZE_SIZE

    def info_str(self):
        """
        :return:color#lst of circles
        """
        circles = []
        for circle in self.circles:
            circles.append(circle.info_str())
        return f"{self.color}#{circles}"

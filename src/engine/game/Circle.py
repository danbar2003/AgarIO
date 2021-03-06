from engine.game.Point import Point


class Circle:
    def __init__(self, point_coordinate, circle_id):
        self.point_coordinate = point_coordinate  # Point(x,y)
        self.circle_id = circle_id
        self.circle_radius = 30

    def duplicate_circle(self, vector_point):
        pass

    def hypothesis_location(self, vector):
        point = Point(self.point_coordinate.x, self.point_coordinate.y)
        point.shift(vector)
        return point

    def move_circle(self, vector):
        self.point_coordinate.shift(vector)

    def contains(self, point):
        return point.distance(self.point_coordinate) < self.circle_radius

    def to_string(self):
        print('    circle_id', self.circle_id)
        print('        circle coordinate', self.point_coordinate.x, self.point_coordinate.y)
        print('        circle radios', self.circle_radius)

    def info_str(self):
        """
        :return:location!radios
        """
        return f"({self.point_coordinate.x}:{self.point_coordinate.y})!{self.circle_radius})"

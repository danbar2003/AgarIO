class Circle:
    def __init__(self, point_coordinate, circle_id):
        self.point_coordinate = point_coordinate  # Point(x,y)
        self.circle_id = circle_id
        self.circle_radios = 1

    def duplicate_circle(self, vector_point):
        pass

    def move_circle(self, speed, vector_point):
        pass

    def contains(self, point):
        return point.distance(self.point_coordinate) < self.circle_radios



class Player:

    def __init__(self, player_id, color):  # etc
        self.player_id = player_id  # id
        self.color = color  # color
        self.speed = 1
        self.circles = []

    def duplicate(self):
        for circle in self.circles:
            circle.duplicate()  # mouse_loc

    def move(self, mouse_location):
        for circle in self.circles:
            circle.move(mouse_location)
        pass

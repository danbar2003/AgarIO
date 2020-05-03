import pygame
import pyautogui
import threading

from engine.game.Point import Point
from client_side.gui.GuiObjects import CircleGUI

FOV_CONSTANT = 300


def remove_chars(str_data, str_lst):
    for str_part in str_lst:
        str_data = str_data.replace(str_part, "")
    return str_data


def convert_str_to_data(frame):
    main_player_circles = []
    enemy_circles = []
    points_as_circles = []

    main_player, enemy_players, points = frame.split('|')

    # enemy_players
    for player in enemy_players.split('", "'):
        if '#' in player:
            player_info = remove_chars(player, ["[", "]", '"', "'"])
            color, circles = player_info.split('#')

            # color
            r, g, b = (remove_chars(color, ["(", ")", " "])).split(",")
            color = (int(r), int(g), int(b))

            # circles
            for circle in (remove_chars(circles, [" "])).split(","):
                circle_info = remove_chars(circles, ["(", ")"])
                coordinate, radius = circle_info.split('!')
                x, y = coordinate.split(':')
                enemy_circles.append(CircleGUI(coordinate=Point(float(x), float(y)), radius=float(radius), color=color))

    # main_player
    main_player = main_player[1:]
    color, circles = main_player.split('#')

    # main_player_color
    r, g, b = (remove_chars(color, ["(", ")", " "])).split(",")
    color = (int(r), int(g), int(b))

    # main_player_circles
    for circle in (remove_chars(circles, ["[", "]", "'", " "])).split(','):
        circle_info = remove_chars(circle, ["(", ")"])
        coordinate, radius = circle_info.split('!')
        x, y = coordinate.split(':')
        main_player_circles.append(CircleGUI(coordinate=Point(float(x), float(y)), radius=float(radius), color=color))

    # points
    for point in remove_chars(points, ["[", "]", "'", " "]).split(','):
        point_info = remove_chars(point, ["(", ")"])
        x, y = point_info.split('X')
        points_as_circles.append(CircleGUI(coordinate=Point(float(x), float(y)), radius=2, color=(60, 90, 120)))

    return main_player_circles, enemy_circles, points_as_circles


def calculate_fov(main_player_circles, enemy_circles, points_as_circles):
    pass


class WindowGui:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.circles = []
        threading.Thread(target=self.gui, args=()).start()

    def gui(self):
        pygame.init()

        win = pygame.display.set_mode(pyautogui.size())
        pygame.display.set_caption("Agar-IO")

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            win.fill((255, 255, 255))  # Fills the screen with white
            """
            FUCK
            """
            pygame.display.update()
        pygame.quit()

    def print_data(self, frame):
        main_player_circles, enemy_circles, points_as_circles = convert_str_to_data(frame)

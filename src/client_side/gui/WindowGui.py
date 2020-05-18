import time

import pygame
import pyautogui
import threading
import math
import os

from engine.game.Constants import MAP_RADIOS
from engine.game.Point import Point
from client_side.gui.GuiObjects import CircleGUI

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
win = pygame.display.set_mode(pyautogui.size())
pygame.display.set_caption("Agar-IO")
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
        try:
            player_info = remove_chars(player, ["[", "]", '"', "'"])
            color, circles = player_info.split('#')

            # color
            r, g, b = (remove_chars(color, ["(", ")", " "])).split(",")
            color = (int(r), int(g), int(b))

            # circles
            for circle in (remove_chars(circles, [" "])).split(","):
                if circle != "":
                    circle_info = remove_chars(circles, ["(", ")"])
                    coordinate, radius = circle_info.split('!')
                    x, y = coordinate.split(':')
                    enemy_circles.append(
                        CircleGUI(coordinate=Point(float(x), float(y)), radius=float(radius), color=color))
        except ValueError:
            pass
    # main_player
    main_player = main_player[1:]
    color, circles = main_player.split('#')

    # main_player_color
    r, g, b = (remove_chars(color, ["(", ")", " "])).split(",")
    color = (int(r), int(g), int(b))

    # main_player_circles
    for circle in (remove_chars(circles, ["[", "]", "'", " "])).split(','):
        try:
            circle_info = remove_chars(circle, ["(", ")"])
            coordinate, radius = circle_info.split('!')
            x, y = coordinate.split(':')
            main_player_circles.append(
                CircleGUI(coordinate=Point(float(x), float(y)), radius=float(radius), color=color))
        except ValueError:
            pass

    # points
    for point in remove_chars(points, ["[", "]", "'", " "]).split(','):
        try:
            point_info = remove_chars(point, ["(", ")"])
            x, y = point_info.split('X')
            points_as_circles.append(CircleGUI(coordinate=Point(float(x), float(y)), radius=5, color=(60, 90, 120)))
        except ValueError:
            pass
    return main_player_circles, enemy_circles, points_as_circles


class WindowGui:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def gui(self, frame):
        circles = self.calculate_fov(frame)
        run = True
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((255, 0, 0))  # Fills the screen with white
        for circle in circles:
            pygame.draw.circle(win, circle.color, (int(circle.coordinate.x), int(circle.coordinate.y)),
                               int(circle.radius))
        pygame.display.update()
        print(time.time() - start_time)
        if not run:
            pygame.quit()

    def calculate_fov(self, frame):
        main_player_circles, enemy_circles, points_as_circles = convert_str_to_data(frame)
        final_circles = []
        try:
            big_radius = 0
            center = Point(0, 0)
            for circle in main_player_circles:
                center.x += circle.coordinate.x
                center.y += circle.coordinate.y
                big_radius += circle.radius ** 2
            center.x, center.y = center.x / len(main_player_circles), center.y / len(main_player_circles)
            big_radius = math.sqrt(big_radius)
            y_fov = big_radius + FOV_CONSTANT
            x_fov = (16 / 9) * y_fov
            top_left_point = Point(center.x - x_fov, center.y - y_fov)
            proportion = (self.width / 2) / x_fov
            main_player_circles += enemy_circles
            for circle in main_player_circles:
                final_circles.append(CircleGUI(
                    coordinate=Point(proportion * (circle.coordinate.x - top_left_point.x),
                                     proportion * (circle.coordinate.y - top_left_point.y)),
                    radius=proportion * circle.radius, color=circle.color))
            for point in points_as_circles:
                final_circles.append((CircleGUI(coordinate=Point(proportion * (point.coordinate.x - top_left_point.x),
                                                                 proportion * (point.coordinate.y - top_left_point.y)),
                                                radius=point.radius, color=point.color)))
            m = [CircleGUI(coordinate=Point(proportion * (-top_left_point.x), proportion * (-top_left_point.y)),
                           radius=proportion * MAP_RADIOS, color=(255, 255, 255))]
            final_circles = m + final_circles
        except Exception:
            pass
        return final_circles

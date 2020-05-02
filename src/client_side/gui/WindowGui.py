import pygame
import pyautogui
import threading
import math

FOV_CONSTANT = 300


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
            for circle in self.circles.copy():
                """
                print those circles
                """
                pass
            pygame.draw.circle(win, (60, 123, 32), (-32, -32), 1000)
            pygame.display.update()

        pygame.quit()

    def calculate_fov(self, main_player, enemy_players, points):
        """
        This function calculates the field of view the client can see
        :param main_player: (color, [((x,y),radios), (x,y),radios), (x,y),radios),...])
        :param enemy_players: [(color,[((x,y),radios),..]), (color,[((x,y),radios),..]),...]
        :param points:[(x,y), (x,y), (x,y),...]
        :raises Gui function with list of circles to print
        """

        circles_info_gui = []
        mid_screen = [0, 0]
        radios_sum = 0
        for circle in main_player[1]:
            radios_sum += circle[1] ** 2
            mid_screen[0], mid_screen[1] = mid_screen[0] + circle[0][0], mid_screen[1] + circle[0][1]

        all_players = enemy_players.copy()
        all_players.append(main_player)
        mid_screen[0], mid_screen[1] = mid_screen[0] / len(main_player[1]), mid_screen[1] / len(main_player[1])
        y_fov = math.sqrt(radios_sum) + FOV_CONSTANT
        x_fov = (16 / 9) * y_fov
        proportion = self.height / y_fov
        top_left_screen = (mid_screen[0] - x_fov, mid_screen[1] - y_fov)

        for player in all_players:
            for circle in player[1]:
                circles_info_gui.append(
                    (player[0], (circle[0][0], circle[0][1]), (circle[1] * self.height) / (2 * y_fov)))
        self.circles = circles_info_gui

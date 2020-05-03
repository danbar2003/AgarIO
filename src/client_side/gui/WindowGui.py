import pygame
import pyautogui
import threading
import math
import time
from engine.game.Circle import Circle
from engine.game.Point import Point

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
            """
            FUCK
            """
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
        pass

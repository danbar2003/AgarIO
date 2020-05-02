import pygame
import pyautogui
import threading


class WindowGui:
    def __init__(self):
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
            for circle in self.circles.copy():
                """
                print those circles
                """
                pass
            win.fill((255, 255, 255))  # Fills the screen with white
            pygame.display.update()

        pygame.quit()

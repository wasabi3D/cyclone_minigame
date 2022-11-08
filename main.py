from GameManager.MainLoopManager import GameRoot
from GameExtensions.UI import TextLabel, BaseUIObject
import os
import pygame
from pygame import Vector2
from objects import *
from GameManager.resources import load_img


def main():
    root = GameRoot((1200, 800), (40, 25, 150), "Cyclone.", os.path.dirname(__file__), Vector2(600, 0))

    root.add_gameObject(BaseUIObject(Vector2(600, 400), 0, load_img("sea_bg.png", (1200, 800)), "sea_bg"))
    root.add_gameObject(Cyclone())
    root.add_gameObject(TextLabel(Vector2(115, 50), 0, pygame.font.SysFont("Arial", 35, bold=True), "==Score==",
                                  (10, 15, 10), "score_name"))
    root.add_gameObject(TextLabel(Vector2(115, 85), 0, pygame.font.SysFont("Arial", 35), "0",
                                  (10, 15, 10), "score"))
    root.add_gameObject(ItemSpawner())


    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

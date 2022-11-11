from GameManager.MainLoopManager import GameRoot
from GameExtensions.UI import TextLabel, BaseUIObject
import os
import pygame
from pygame import Vector2
from objects import *
from GameManager.resources import load_img


def main():
    # Initialisation
    root = GameRoot((1200, 800), (40, 25, 150), "Cyclone.", os.path.dirname(__file__), Vector2(600, 0))
    
    # Fond d'écran
    root.add_gameObject(BaseUIObject(Vector2(600, 400), 0, load_img("sea_bg.png", (1200, 800)), "sea_bg"))
    
    # Cyclone controllé par le joueur
    root.add_gameObject(Cyclone())
    
    # Le texte "score" affiché sur l'écran
    root.add_gameObject(TextLabel(Vector2(115, 50), 0, pygame.font.SysFont("Arial", 35, bold=True), "==Score==",
                                  (10, 15, 10), "score_name"))
    
    # Le score
    root.add_gameObject(TextLabel(Vector2(115, 85), 0, pygame.font.SysFont("Arial", 35), "0",
                                  (10, 15, 10), "score"))
    
    # Celui qui s'occupe de la création des soleils et des flocons
    root.add_gameObject(ItemSpawner())

    root.mainloop()


if __name__ == '__main__':
    main()

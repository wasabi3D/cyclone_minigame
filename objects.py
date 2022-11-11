from GameManager.util import GameObject
from GameManager.resources import *
import pygame as pg
from pygame.locals import *
import GameManager.singleton as sing
import random
from GameManager.funcs import resize_surface
from GameExtensions.UI import TextLabel


# La classe qui définit le cyclone
class Cyclone(GameObject):
    def __init__(self):
        super().__init__(pg.Vector2(600, 250), 0, load_img("cyclone1.png", (100, 100)), "cyclone")
        self.mov = 250
        self.rot_spd = 0.4  # C'est en radian/sec
        self.scale = 1
        
        # Il faut garder l'original car l'image se déforme petit à petit à cause des rotations, etc..
        self.backup_img = self.image.copy()

    def update(self) -> None:
        super().update()

        pressed = pg.key.get_pressed()

        # Key input et mouvement
        if pressed[K_LEFT] or pressed[K_a]:
            self.translate(-1 * pg.Vector2(self.mov, 0) * sing.ROOT.delta)
        if pressed[K_RIGHT] or pressed[K_d]:
            self.translate(pg.Vector2(self.mov, 0) * sing.ROOT.delta)
        if pressed[K_UP] or pressed[K_w]:
            self.translate(pg.Vector2(0, -self.mov) * sing.ROOT.delta)
        if pressed[K_DOWN] or pressed[K_s]:
            self.translate(pg.Vector2(0, self.mov) * sing.ROOT.delta)
            
        # évite que le cyclone sort de l'écran
        self.pos.x = max(min(self.pos.x, 1200), 0)
        self.pos.y = max(min(self.pos.y, 800), 0)

        self.rotate(self.rot_spd * sing.ROOT.delta)

        # Détection des collisions avec les soleils/flocons
        col = sing.ROOT.is_colliding(self.get_collision_rect())
        if col != -1:
            obj = sing.ROOT.collidable_objects[col]
            lb: TextLabel = sing.ROOT.game_objects["score"]
            if isinstance(obj, Humid):
                self.rot_spd += 0.35
                self.scale += 0.1
                lb.set_text(f"{int(lb.text) + 50}")
                print("Humid")
            elif isinstance(obj, Cold):
                self.rot_spd -= 0.2
                self.scale -= 0.1
                self.rot_spd = max(0.0, self.rot_spd)
                self.scale = max(0, self.scale)
                lb.set_text(f"{int(lb.text) - 50}")
                print("Cold")
                
            self.image = resize_surface(self.backup_img, self.scale)
            self.copy_img = self.image.copy()
            sing.ROOT.remove_object(obj)


# La classe qui s'occupe de la création des soleils/flocons
class ItemSpawner(GameObject):
    def __init__(self):
        super().__init__(pg.Vector2(), 0, pg.Surface((0, 0)), "spawner")
        self.timer = 0
        self.cnt = 0
        self.spawn_interval = 3
        
        # Si on est en train de générer les items ou pas
        sing.ROOT.parameters["gen"] = True

    def update(self) -> None:
        self.timer += sing.ROOT.delta
        if self.timer > self.spawn_interval and sing.ROOT.parameters["gen"]:
            self.timer = 0
            self.cnt += 1
            
            #spawn
            if random.randint(1, 2) == 2:
                sing.ROOT.add_gameObject(Cold(pg.Vector2(random.randint(100, 1100), -400), self.cnt))
            else:
                sing.ROOT.add_gameObject(Humid(pg.Vector2(random.randint(100, 1100), -400), self.cnt))


# Flocon
class Cold(GameObject):
    def __init__(self, spawn_pos: pg.Vector2, sn_id: int):
        super().__init__(spawn_pos, 0, load_img("snowflake.png", (80, 80)), f"snowfl{sn_id}")
        self.mov = pg.Vector2(0, 120)
        sing.ROOT.add_collidable_object(self)

    def update(self) -> None:
        self.translate(self.mov * sing.ROOT.delta)
        self.rotate(0.2 * sing.ROOT.delta)

        if self.pos.y > 500:
            sing.ROOT.remove_object(self)


# Soleil (Humidité)
class Humid(GameObject):
    def __init__(self, spawn_pos: pg.Vector2, sn_id: int):
        super().__init__(spawn_pos, 0, load_img("humid.png", (100, 100)), f"humid{sn_id}")
        self.mov = pg.Vector2(0, 165)
        sing.ROOT.add_collidable_object(self)

    def update(self) -> None:
        self.translate(self.mov * sing.ROOT.delta)

        if self.pos.y > 500:
            sing.ROOT.remove_object(self)


# Cette classe n'est pas utilisée car le joueur ne peut pas mourir pour l'instant
class GameOver(GameObject):
    def __init__(self):
        super().__init__(pg.Vector2(), 0, pg.Surface((0, 0)), "gameovermng")

        sing.ROOT.add_gameObject(TextLabel(pg.Vector2(600, 400), 0, pg.font.SysFont("Arial", 25), "Game Over", (30, 30,30), "gameover_label"))
        sing.ROOT.add_gameObject(
            TextLabel(pg.Vector2(600, 400), 0, pg.font.SysFont("Arial", 15), "Press space to restart", (30, 30, 30),
                      "restart_label"))
        sing.ROOT.remove_object(sing.ROOT.game_objects["cyclone"])
        sing.ROOT.parameters["gen"] = False

    def update(self) -> None:
        # Redémarrer le jeu
        if pg.key.get_pressed()[K_SPACE]:
            sing.ROOT.remove_object(sing.ROOT.game_objects["restart_label"])
            sing.ROOT.remove_object(sing.ROOT.game_objects["gameover_label"])
            sing.ROOT.add_gameObject(Cyclone())
            sing.ROOT.parameters["gen"] = True
            lb: TextLabel = sing.ROOT.game_objects["score"]



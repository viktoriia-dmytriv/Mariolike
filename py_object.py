import pygame
from globals import *


class PyObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.center += self.speed * clock.get_time() / 1000

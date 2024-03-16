import pygame

from obstacle import Obstacle
from platform import Platform
from py_object import PyObject
import globals
from globals import *
from settings import GRAVITY


class Player(PyObject):
    JUMP_SPEED = 1200
    SPEED = 400
    PLAYER_HEIGHT = 50
    PLAYER_WIDTH = 50

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
        self.win = False
        self.lose = False
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.math.Vector2(pos)
        self.jumps_left = 0

    def update(self):
        super().update()
        self.speed.y += GRAVITY * clock.get_time() / 1000

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > globals.WIDTH:
            self.rect.right = globals.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > globals.HEIGHT:
            self.lose = True

        for platform in globals.level:
            if self.rect.colliderect(platform.rect):
                if isinstance(platform, Platform) and self.rect.bottom - self.speed.y * clock.get_time() / 1000 <= platform.rect.top:
                    self.jumps_left = 1
                    self.rect.bottom = platform.rect.top
                    self.speed.y = 0
                    if platform.is_win:
                        self.win = True

        for platform in globals.level:
            if self.rect.colliderect(platform.rect):
                if isinstance(platform, Obstacle):
                    self.lose = True

    def jump(self):
        if self.jumps_left > 0:
            self.speed.y = -self.JUMP_SPEED
            self.jumps_left -= 1

    def move_left(self):
        self.speed.x = -self.SPEED

    def move_right(self):
        self.speed.x = self.SPEED

    def stop(self):
        self.speed.x = 0

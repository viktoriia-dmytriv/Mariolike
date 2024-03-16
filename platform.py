# create platform class, player can jump on it

from py_object import *


class Platform(PyObject):
    def __init__(self, x, y, width, height, is_win=False):
        super().__init__()
        self.is_win = is_win
        self.image = pygame.Surface((width, height))
        if is_win:
            self.image.fill((0, 255, 0))
        else:
            self.image.fill((64, 64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

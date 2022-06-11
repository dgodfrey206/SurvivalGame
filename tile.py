import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, number) -> None:
        super().__init__()
        self.image = tiles[number - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surf: pygame.Surface) -> None:
        surf.blit(self.image, self.rect)
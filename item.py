import pygame
from settings import *
from tile import Tile

class Item(Tile):
    def __init__(self, x, y, number):
        super().__init__(x, y, number)
        self.image = items[number - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = item_values[number - 1]
        #type food or water
        if number <= 5:
            self.type = 0
        else:
            self.type = 1

    def on_screen(self) -> bool:
        """
        checks if the item is still on screen
            > removes it if not
        """
        if self.rect.x > 0:
            return True
        return False
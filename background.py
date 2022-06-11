import pygame

from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        #load images
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        # current time
        self.time = 0
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def day_night_cycle(self) -> None:
        """
        change background based on current time
        """
        self.time += 1
        if self.time > 1800:
            self.image = night
        elif self.time > 2600:
            self.image = bg
            self.time = 0

    def command(self, command: str) -> None:
        """
        adjust background based on command
        """
        if command == "/night":
            self.set_daytime("night")
        elif command == "/day":
            self.set_daytime("day")

    def get_daytime(self) -> str:
        if self.time < 1800:
            return "day"
        return "night"

    def set_daytime(self, daytime) -> None:
        if daytime == "night":
            self.image = night
            self.time = 1800
        elif daytime == "day":
            self.image = bg
            self.time = 0
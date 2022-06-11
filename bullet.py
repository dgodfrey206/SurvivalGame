import pygame
from settings import *

class Bullet:
    def __init__(self, x: int, y: int, direction: int, damage: int) -> None:
        self.x = x
        self.y = y
        self.vel = 30
        self.damage = damage
        self.img = BULLET

        self.direction = direction

        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def draw(self, surf: pygame.Surface) -> None:
        surf.blit(self.img, (self.x, self.y))

    def move(self, obstacles: list, targets: list) -> bool:
        """
        moving the bullets
        obstacles, targets: checking for collision
        """
        self.x += self.vel * self.direction
        self.rect.x = self.x
        if self.off_screen():
            return True, False
        for target in targets:
            if self.rect.colliderect(target.rect):
                target.health -= self.damage
                return True
        for row in obstacles:
            for obstacle in row:
                if self.rect.colliderect(obstacle.rect):
                    return True

        return False

    def off_screen(self) -> bool:
        """
        check if bullet went off screen
        """
        if self.x > WIDTH or self.x < 0:
            return True
        return False

    def camera(self, scroll: int) -> None:
        """
        adjusting bullet according to camera
        """
        self.x += scroll
        self.rect.x += scroll
import pygame

from player import Player
from settings import *

class Zombie(Player):
    def __init__(self, x, y) -> None:
        """
        cannot be inherited from Player
        """
        self.x = x
        self.ix = x
        self.y = y
        self.vel = 1
        self.vel_up = 0

        self.time = 0
        self.bullet_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.scale = 2.3

        self.direction = -1
        self.damage = ZOMBIE_DAMAGE
        self.seeing_distance = 300
        self.offset = 200

        #loading in images
        self.imgs = []
        self.deaths = []

        self.score_added = False

        for i in range(1, 4):
            img = pygame.image.load(f"images/enemy/walk left{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.imgs.append(img)

        for i in range(1, 5):
            img = pygame.image.load(f"images/player/death/death{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
            self.deaths.append(img)

        self.img = self.imgs[0]

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.flip = False

        self.resetted = False

    def draw(self, surf: pygame.Surface) -> None:
        """
        only draw if enemy is alive else death animation > then remove enemy
        """
        if self.alive():
            max_health, health = self.healthbar()
            pygame.draw.rect(surf, BLUE, max_health)
            pygame.draw.rect(surf, PINK, health)
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))

    def move(self, targets: list, target, daytime: str) -> None:
        """
        depending on whether or not zombie sees player
            > seeing distance
        """
        if self.direction == -1:
            self.flip = True
        else:
            self.flip = False

        dx = dy = 0
        saw, in_range, direction = self.see(target, daytime)
        if saw:
            self.direction = direction
            self.vel = 3
            if in_range:
                self.vel = 0
                self.attack(target)
        else:
            if self.vel == 3:
                self.ix = self.x
            self.vel = 1
            if self.check_offset() or self.off_screen():
                self.direction *= -1

        dx = self.vel
        dy = self.vel_up

        dx, dy, obs = self.collision(targets, dx, dy)
        if obs:
            self.jump()

        self.x += dx * self.direction
        self.y += dy

        self.cooldown()
        self.animate()
        self.gravity()
        self.update_rect()

    def collision(self, targets: list, dx: int, dy: int) -> tuple:
        """
        edited player collision function
        """
        obs = False
        for chunk in targets:
            for tile in chunk:
                if tile.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                    obs = True
                if tile.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    if self.vel_up < 0:
                        self.vel_up = 0
                        dy = tile.rect.y + TILE_SIZE  - self.y
                    elif self.vel_up >= 0:
                        self.vel_up = 0
                        self.jumping = False
                        dy = tile.rect.y - (self.y + self.height)

        return dx, dy, obs

    def update_rect(self) -> None:
        """
        no inheritation possible
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def attack(self, target: tuple) -> None:
        """
        attack the player if cooldown allows it
        """
        if self.bullet_cooldown == 0:
            target.health -= self.damage
            self.bullet_cooldown = 1

    def see(self, target: Player, time) -> tuple:
        """
        check if zombie can see the player -> returning: seeing: bool, touching: bool, direction: int
        """
        if time == "day":
            self.seeing_distance = 300
        else:
            self.seeing_distance = 100
        if self.x - self.seeing_distance < target.rect.x and self.x > target.rect.x and abs(self.y - target.rect.y) < 100:
            if self.rect.colliderect(target.rect):
                return True, True, -1
            return True, False, -1
        elif self.x + self.width + self.seeing_distance > target.rect.x and self.x < target.rect.x and abs(self.y - target.rect.y) < 100:
            if self.rect.colliderect(target.rect):
                return True, True, 1
            return True, False, 1

        return False, False, self.direction

    def animate(self) -> None:
        """
        animation function (cannot be inherited from Player)
        """
        self.time += 1
        if self.time < 8:
            self.img = self.imgs[0]
        elif self.time < 16:
            self.img = self.imgs[1]
        elif self.time < 24:
            self.img = self.imgs[2]
        else:
            self.time = 0

    def check_offset(self) -> bool:
        """
        check if zombie has to turn around (when on patrol)
        """
        if abs(self.x - self.ix) > self.offset:
            return True
        return False

    def death_animation(self, targets):
        """ 
        death animation based on time (not possible to inherit from player)
        """
        if not self.resetted:
            self.rect.x = -100
            self.rect.y = -100
            self.time = 0
            self.resetted = True

        self.time += 1

        if self.time < 5:
            self.img = self.deaths[0]
        elif self.time < 10:
            self.y += 2 * self.scale
            self.img = self.deaths[1]
        elif self.time < 15:
            self.y += 2 * self.scale
            self.img = self.deaths[2]
        elif self.time < 20:
            if self.time == 15:
                self.y += 5 * self.scale
                self.x -= 3 * self.scale
            self.img = self.deaths[3]
        elif self.time > 120:
            return True

    def alive(self) -> bool:
        """
        check if player is alive
        """
        if self.health > 0:
            return True
        return False

    def camera(self, scroll: int) -> None:
        """
        add camera effect to object
        """
        self.x += scroll
        self.ix += scroll
        self.rect.x += scroll

    def healthbar(self) -> tuple:
        """
        get healthbar and return according rect
        """
        rel_health = (self.health / self.max_health) * 100
        max_health = pygame.Rect(self.x + self.width / 2 - self.max_health / 2, self.y - 20, self.max_health, 10)
        health = pygame.Rect(self.x + self.width / 2 - self.max_health / 2, self.y - 20, rel_health, 10)

        return max_health, health

    def jump(self) -> None:
        """
        jump up > change up value > gravitiy pulls object down
        """
        self.vel_up = -15

    def off_screen(self) -> bool:
        if self.x < 0 or self.x > WIDTH - self.width:
            return True
        return False


        
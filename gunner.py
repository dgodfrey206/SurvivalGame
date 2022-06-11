import pygame
from settings import *
from bullet import Bullet
from player import Player

class Gunner(Player):
    SHOOT_COOL = GUNNER_COOLDOWN

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.vel = 2
        self.ix = x
        self.patrol_offset = 400
        self.scale = 2.2

        self.imgs = []
        self.deaths = []
        self.current = 0
        animations = ["run", "death"]
        for animation in animations:
            l = []
            for i in range(1,5):
                img = pygame.image.load(f"images/enemy/{animation}/{animation}{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                l.append(img)
            if animation == "death":
                self.deaths += l
            self.imgs.append(l)

        # gunner standing
        img = pygame.image.load(f"images/enemy/stand/standing.png")
        img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.imgs.append([])
        for i in range(4):
            self.imgs[2].append(img)

    def move(self, targets: list, target: Player, daytime: int) -> None:
        """
        adjusted player move function > not inherited
        """
        dx = 0
        dy = 0

        if abs(self.x - self.ix) > self.patrol_offset:
            self.direction *= -1

        dx += self.vel * self.direction

        self.flip = False if self.direction == 1 else True
        
        self.gravity()

        dy += self.vel_up

        dx, dy, obs = self.collision(targets, dx, dy)

        if obs:
            self.direction *= -1

        saw, dir = self.see(target, daytime)
        if saw:
            self.direction = dir
            self.ix = self.x
            self.shoot()
            self.current = 2
            dx = 0
        else:
            self.current = 0
            

        self.x += dx
        self.y += dy

        self.time += 1

        self.animate()
        self.update_rect()
        self.move_bullets(targets, [target])

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

    def animate(self) -> None:
        """
        animate the player every frame
        """
        if self.time < 10:
            self.img = self.imgs[self.current][0]
        elif self.time < 20:
            self.img = self.imgs[self.current][1]
        elif self.time < 30:
            self.img = self.imgs[self.current][2]
        elif self.time < 40:
            self.img = self.imgs[self.current][3]
        else:
            self.time = 0

    def see(self, target: Player, time) -> tuple:
        """
        check if gunner can see the player -> returning: seeing: bool, direction: int
        """
        if time == "day":
            self.seeing_distance = 500
        else:
            self.seeing_distance = 100
        if self.x - self.seeing_distance < target.rect.x and self.x > target.rect.x and abs(self.y - target.rect.y) < 75:
            return True, -1
        elif self.x + self.width + self.seeing_distance > target.rect.x and self.x < target.rect.x and abs(self.y - target.rect.y) < 75:
            return True, 1

        return False, self.direction

    def shoot(self) -> None:
        """
        adjusted
        """
        if self.bullet_cooldown == 0:
            if self.direction == -1:
                bullet = Bullet(self.x + 14 * self.scale, self.y + 13 * self.scale, self.direction, GUNNER_DAMAGE)
            else:
                bullet = Bullet(self.x - 4 * self.scale, self.y + 13 * self.scale, self.direction, GUNNER_DAMAGE)
            self.bullets.append(bullet)
            self.bullet_cooldown = 1

    def camera(self, scroll):
        self.x += scroll
        self.ix += scroll

    def draw(self, surf: pygame.Surface) -> None:
        """
        only draw if gunner is alive else death animation > then remove gunner
        """
        if self.alive():
            max_health, health = self.healthbar()
            pygame.draw.rect(surf, BLUE, max_health)
            pygame.draw.rect(surf, PINK, health)
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(surf)


    def healthbar(self) -> tuple:
        """
        returns Rects to draw health bar
        """
        rel_health = (self.health / self.max_health) * 100
        max_health = pygame.Rect(self.x + self.width / 2 - self.max_health / 2, self.y - 20, self.max_health, 10)
        health = pygame.Rect(self.x + self.width / 2 - self.max_health / 2, self.y - 20, rel_health, 10)

        return max_health, health

    def death_animation(self, targets):
        """
        death animation:
            > stops every other activity (in main.py)
        """
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel_up += 20

        if not self.resetted:
            self.time = 0
            self.resetted = True

        dy = 20
        dx = 0
        obs = None

        dx, dy, obs = self.collision(targets, dx, dy)

        self.y += dy

        self.time += 1

        if self.time < 5:
            self.img = self.deaths[0]
        elif self.time < 10:
            self.y += 0.2 * self.scale
            self.img = self.deaths[1]
        elif self.time < 15:
            self.y += 0.2 * self.scale
            self.img = self.deaths[2]
        elif self.time < 20:
            if self.time == 15:
                self.y += 2 * self.scale
                self.x -= 5 * self.scale
            self.img = self.deaths[3]
        else:
            return True

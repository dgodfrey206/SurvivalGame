import pygame

from tile import Tile
from settings import *
from bullet import Bullet

class Player:
    # CONSTANTS
    COOLDOWN = 60
    GRAVITY = 1
    SHOOT_COOL = 30
    ATTACK_COOL = 60

    def __init__(self, x: int, y: int,) -> None:
        self.x = x
        self.y = y
        self.vel = 10
        self.vel_up = 0
        self.time = 0
        self.bullet_cooldown = 0
        self.attack_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.food = 100
        self.max_food = self.food
        self.water = 100
        self.max_water = self.water
        self.desire = 0
        
        self.second_jump = False
        self.hit_enemy = False

        self.scale = 5
        self.direction = 1
        self.current = 0
        self.current_item = 0
        self.items = 3
        self.imgs = []
        self.deaths = []

        # standart sprite sheets
        items = ["normal", "pistol", "sword"]
        animations = ["idle", "walk", "swim", "attack"]
        for item in items:
            items = []
            for animation in animations:
                l = []
                for i in range(1, 5):
                    img = pygame.image.load(f"images/player/{item}/{animation}/{animation} left{i}.png")
                    img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                    l.append(img)
                items.append(l)
            self.imgs.append(items)
        self.img = self.imgs[self.current_item][self.current][0]

        # death animation
        for i in range(1, 5):
            img = pygame.image.load(f"images/player/death/death{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
            self.deaths.append(img)


        self.width = self.img.get_width()
        self.height = self.img.get_height() - 2 * self.scale
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.flip = False
        self.jumping = False

        self.resetted = False
        # list where all shot bullets are stored
        self.bullets = []

    def draw(self, surf: pygame.Surface) -> None:
        """
        drawing the player with every additional element
        """
        # checking for iamge flip and drawing image
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))
        # getting bar rects
        max_health, health = self.healthbar()
        max_food, food, max_water, water = self.get_food()
        # drawign bar rects
        pygame.draw.rect(surf, BLUE, max_health)
        pygame.draw.rect(surf, PINK, health)

        pygame.draw.rect(surf, BLUE, max_food)
        pygame.draw.rect(surf, PINK, food)
        
        pygame.draw.rect(surf, BLUE, max_water)
        pygame.draw.rect(surf, PINK, water)
        # drawing bullets
        for bullet in self.bullets:
            bullet.draw(surf)

    def move(self, left: bool, right: bool, targets: list, items: list, camera_lim: int) -> int:
        """ 
        updating the player movement
        handling most of the events related or affected by player movement
        """
        scroll = 0
        dx = dy = 0
        if left and self.current != 3 or right and self.current != 3:
            self.current = 1
        if left:
            dx += self.vel
            self.flip = True
            self.direction = -1
        elif right:
            dx -= self.vel
            self.flip = False
            self.direction = 1
        else:
            if self.current != 3:
                self.current = 0

        self.time += 1

        self.gravity()

        dy += self.vel_up

        dx, dy = self.collision(targets, dx, dy)

        self.x += dx
        self.y += dy

        if self.x > WIDTH - camera_lim - self.width and self.direction == -1:
            self.x -= dx
            scroll = -dx

        self.animate()
        self.update_rect()
        self.att_cooldown()
        self.item_collision(items)

        #updating every bullet to camera
        for bullet in self.bullets:
            bullet.camera(scroll)

        #returning camera value
        return scroll

    def update_rect(self) -> None:
        """
        update the player rect every frame
        """
        self.width = self.img.get_width()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def animate(self) -> None:
        """
        animate the player every frame
        """
        if self.time < 10:
            self.img = self.imgs[self.current_item][self.current][0]
        elif self.time < 20:
            self.img = self.imgs[self.current_item][self.current][1]
        elif self.time < 30:
            self.img = self.imgs[self.current_item][self.current][2]
        elif self.time < 40:
            self.img = self.imgs[self.current_item][self.current][3]
        else:
            if self.current == 3:
                if self.current_item == 2:
                    self.attack_adjustmend()
                self.current = 0
            self.time = 0
        if self.current == 3:
            if self.current_item == 1:
                self.shoot_adjustmend()
            elif self.current_item == 2:
                self.attack_adjustmend()

    def alive(self) -> bool:
        """
        check if player is still alive
        """
        if self.health > 0:
            return True
        return False

    def gravity(self) -> None:
        """
        constantly add gravity to players movement
        """
        self.vel_up += self.GRAVITY
        if self.vel_up > 20:
            self.vel_up = 20

    def collision(self, targets: list, dx: int, dy: int) -> tuple:
        """
        check for player collisions
        """
        for chunk in targets:
            for tile in chunk:
                if tile.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                if tile.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    if self.vel_up < 0:
                        self.vel_up = 0
                        dy = tile.rect.y + TILE_SIZE  - self.y
                    elif self.vel_up >= 0:
                        self.vel_up = 0
                        self.jumping = self.second_jump = False
                        dy = tile.rect.y - (self.y + self.height)

        if self.x + dx < 0:
            dx = 0

        return dx, dy

    def item_collision(self, items: list) -> list:
        b = False
        for item in items:
            if item.rect.colliderect(self.rect):
                if item.type == 0:
                    self.food += item.value
                    items.remove(item)
                    if self.food > 100:
                        self.food = 100
                    break
                else:
                    self.water += item.value
                    if self.water > 100:
                        self.water = 100
                    items.remove(item)
                    break
        return items
                    

    def shoot(self) -> None:
        """
        add bullet to self.bullets
        """
        if self.bullet_cooldown == 0:
            self.current = 3
            self.time = 0
            if self.direction == -1:
                bullet = Bullet(self.x + 12 * self.scale, self.y + 8 * self.scale, -self.direction, PISTOL_DAMAGE)
            else:
                bullet = Bullet(self.x - 2 * self.scale, self.y + 8 * self.scale, -self.direction, PISTOL_DAMAGE)
            self.bullets.append(bullet)
            self.bullet_cooldown = 1
    
    def attack(self) -> None:
        """
        attack with sword and shield
        """
        if self.attack_cooldown == 0:
            self.current = 3
            self.time = 0
            self.attack_cooldown = 1

    def attack_hit(self, targets: list) -> None:
        """
        check if sword hitted target when swinging
        """
        if self.time == 1:
            self.hit_enemy = False
        if not self.hit_enemy:
            if self.time < 20 and self.current == 3:
                if self.direction == -1:
                    for target in targets:
                        offset = self.x - target.rect.x
                        offsety = self.y - target.rect.y
                        if abs(offset) <= self.width and abs(offsety) < 15 * self.scale:
                            target.health -= SWORD_DAMAGE
                            self.hit_enemy = True
                            break
                else:
                    for target in targets:
                        offsety = self.y - target.rect.y
                        if self.x < (target.rect.x + target.width) and self.x > (target.rect.x - 9 * self.scale) and abs(offsety) < 15 * self.scale:
                            target.health -= SWORD_DAMAGE
                            self.hit_enemy = True
                            break

    def move_bullets(self, obstacles: list, targets: list) -> None:
        """
        move the bullets after shooting
        """
        self.cooldown()
        for bullet in self.bullets:
            v1 = bullet.move(obstacles, targets)
            if v1:
                self.bullets.remove(bullet)

    def cooldown(self) -> None:
        """
        shooting cooldown
        """
        if self.bullet_cooldown > 0:
            self.bullet_cooldown += 1
            if self.bullet_cooldown >= self.SHOOT_COOL:
                self.bullet_cooldown = 0

    def att_cooldown(self) -> None:
        """
        sword cooldown
        """
        if self.attack_cooldown > 0:
            self.attack_cooldown += 1
            if self.attack_cooldown >= self.ATTACK_COOL:
                self.attack_cooldown = 0


    def next_item(self) -> None:
        """
        get the next item after rolling the mouse wheel
        """
        self.current_item += 1
        if self.current_item > self.items - 1:
            self.current_item = 0

        # changing the speed if player takes gun or sword
        if self.current_item == 1:
            self.vel = 7
        elif self.current_item == 2:
            self.vel = 5
        else:
            self.vel = 10

    def shoot_adjustmend(self) -> None:
        """
        image topleft changes because of the gun tip when firing -> adjustment
        """
        if self.direction == 1:
            if self.time == 1:
                self.x -= 4 * self.scale
            elif self.time == 10:
                self.x += 5 * self.scale
            elif self.time == 20:
                self.x -= 1 * self.scale

    def attack_adjustmend(self) -> None:
        """
        image topleft changes because of the sword tip when attacking -> adjustment
        """
        if self.direction == -1:
            if self.time == 1:
                self.x -= 3 * self.scale
            elif self.time == 10:
                self.x += 4 * self.scale
            elif self.time == 20:
                self.x -= 5 * self.scale
            elif self.time == 40:
                self.x += 4 * self.scale
        elif self.direction == 1:
            if self.time == 1:
                self.x -= 10 * self.scale
            #elif self.time == 10:
                #self.x += 4 * self.scale
            elif self.time == 20:
                self.x += 10 * self.scale
            #elif self.time == 40:
                #self.x += 4 * self.scale

    def check_shoot(self) -> None:
        """
        getting all keys that are held down:
            > this is done, so the player can shoot/attack continously
            > when holding down the mouse button
        """
        if pygame.mouse.get_pressed()[0]:
            if self.current_item == 1:
                self.shoot()
            elif self.current_item == 2:
                self.attack()

    def death_animation(self, targets):
        """
        death animation:
            > stops every other activity (in main.py)
        """
        self.height = self.deaths[3].get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel_up = 20
        if not self.resetted:
            self.time = 0
            self.resetted = True

        dy = self.vel_up
        dx = 0

        dx, dy = self.collision(targets, dx, dy)

        self.y += dy

        self.time += 1

        if self.time < 5:
            self.img = self.deaths[0]
        elif self.time < 10:
            self.img = self.deaths[1]
        elif self.time < 15:
            self.img = self.deaths[2]
        elif self.time < 20:
            if self.time == 15:
                self.x -= 5 * self.scale
            self.img = self.deaths[3]
        else:
            return True

    def healthbar(self) -> tuple:
        """
        returns Rects to draw health bar
        """
        rel_health = (self.health / self.max_health) * 100
        max_health = pygame.Rect(5, 5, self.max_health * 2, 20)
        health = pygame.Rect(5, 5, rel_health * 2, 20)

        return max_health, health

    def get_food(self):
        """
        returns Rects to draw for bars
        """
        max_food = pygame.Rect(5, 30, self.max_food * 2, 20)
        max_water = pygame.Rect(5, 55, self.max_water * 2, 20)

        food = pygame.Rect(5, 30, self.food * 2, 20)
        water = pygame.Rect(5, 55, self.water * 2, 20)

        return max_food, food, max_water, water

    def get_desire(self) -> None:
        """
        food and water bar decreases every time this funcion is called
        """
        self.desire += 1
        if self.desire >= 60:
            self.food -= FOOD_DECREASE
            self.water -= FOOD_DECREASE
            self.desire = 0

    def use_item(self, targets: list) -> None:
        """
        pick up food or water and add points to according bar
        """
        for target in targets:
            if self.rect.colliderect(target.rect):
                if target.type == 0:
                    self.water += 20
                    if self.water > 100:
                        self.water = 100

                else:
                    self.food += 20
                    if self.food > 100:
                        self.food = 100
                break

    def food_shortage(self) -> None:
        """
        check if food or water is less than 0 > health decreases
        """
        if self.food < 0 or self.water < 0:
            self.health -= 1

    def jump(self) -> None:
        if not self.second_jump:
            self.vel_up = -20
            if self.jumping:
                self.second_jump = True
            else:
                self.jumping = True
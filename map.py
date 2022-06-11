import pygame
import random
import noise

from settings import *
from tile import Tile
from item import Item
from zombie import Zombie
from gunner import Gunner

class Map:
    def __init__(self) -> None:
        self.map = []
        self.obstacles = []
        self.items = []
        self.deco = []
        self.enemies = []
        self.load_map()

    def generate_chunk(self, x: float, y: float, noise_x: int): #! improve
        """
        generates chunk with x and y value
        noise_x: x value for 1d noise map gen
        """
        chunk = []
        items = []
        chunk_deco = []
        n_x = noise_x
        max_height = 8
        for y_pos in range(CHUNK_SIZE):
            n_x = noise_x
            for x_pos in range(CHUNK_SIZE):
                target_x = x * CHUNK_SIZE + x_pos
                target_y = y * CHUNK_SIZE + y_pos
                height = int(noise.pnoise1(n_x * 0.1, repeat=999999) * 4)
                max_height = min(7 - height, max_height)
                n_x += 1
                if target_y > 7 - height:
                    chunk_deco.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE , 2))
                elif target_y == 7 - height:
                    chunk.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE, 1))
                elif target_y == 5 - height:
                    r = random.randint(1, 20)
                    if r <= 3:
                        chunk_deco.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE + TILE_SIZE * 1.5, random.randint(12, 14)))
                    elif r == 5:
                        chunk_deco.append(Tile(target_x * TILE_SIZE, (target_y) * TILE_SIZE, 17))
                    elif r == 6:
                        chunk_deco.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE + TILE_SIZE, 18))
                    elif r == 7:
                        pass
                        #enemies.append(Zombie())
                elif target_y == 6 - height:
                    r = random.randint(1, 3)
                    if r <= 2:
                        chunk_deco.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE + TILE_SIZE * 0.76, random.randint(9, 11)))
                elif target_y == 4 - height:
                    if x_pos == CHUNK_SIZE - 1:
                        r = random.randint(1, 2)
                        if r == 1:
                            y_r = random.randint(2, 4)
                            r_size = random.randint(0, 4)
                            p = target_x - CHUNK_SIZE + random.randint(0, CHUNK_SIZE - r_size - 2)

                            chunk.append(Tile(p * TILE_SIZE + 5, max_height * TILE_SIZE - (TILE_SIZE * y_r), 3))
                            i = 0
                            for i in range(r_size):
                                chunk.append(Tile(p * TILE_SIZE + (TILE_SIZE * (i + 1)), max_height * TILE_SIZE - (TILE_SIZE * y_r), 1))
                            chunk.append(Tile(p * TILE_SIZE + (TILE_SIZE * (i + 1)), max_height * TILE_SIZE - (TILE_SIZE * y_r), 4))
                            items.append(Item(p * TILE_SIZE + (TILE_SIZE * (i)), max_height * TILE_SIZE - (TILE_SIZE * (y_r + 0.5)), random.randint(1, ITEMS)))


        return chunk, chunk_deco, items

    def generate_enemy(self, x: float, daytime: str) -> list:
        """
        generate enemies in new chunk
        """
        enemies = []
        # get daytime > for how many enemies can spawn in one chunk
        if daytime == "night":
            r = random.randint(0, 5)
        else:
            r = random.randint(0, 2)
        # spawn every enemy at random pos in chunk based on daytime
        for _i in range(r):
            if daytime == "night":
                enemies.append(Zombie(x * CHUNK_SIZE * TILE_SIZE + random.randint(0, CHUNK_SIZE * TILE_SIZE), TILE_SIZE * 2))
            else:
                enemies.append(Gunner(x * CHUNK_SIZE * TILE_SIZE + random.randint(0, CHUNK_SIZE * TILE_SIZE), TILE_SIZE * 2))
        return enemies

    
    def load_map(self) -> None:
        """
        loding the first chunks and generating map
        """
        for x in range(4):
            for y in range(2):
                chunk_obs, chunk_deco, items = self.generate_chunk(x, y, x * CHUNK_SIZE)
                if x != 0:
                    self.enemies += self.generate_enemy(x, y)
                self.obstacles.append(chunk_obs)
                self.deco.append(chunk_deco)
                if items:
                    self.items += items

    def draw(self, surf: pygame.Surface) -> None:
        """
        drawing all tiles
        """
        for chunk in self.obstacles:
                for tile in chunk:
                    tile.draw(surf)

    def draw_deco(self, surf: pygame.Surface) -> None:
        """
        drawing all decoration
        """
        for chunk in self.deco:
                for tile in chunk:
                    tile.draw(surf)

    def draw_items(self, surf: pygame.Surface) -> None:
        """
        drawing all items
        """
        for tile in self.items:
            if tile.on_screen():
                tile.draw(surf) 
            else:
                self.items.remove(tile)
    
    def camera(self, scroll: None) -> None:
        """
        adding camera effect for every map object
        """
        for chunk in self.obstacles:
            for tile in chunk:
                tile.rect.x += scroll

        for chunk in self.deco:
            for tile in chunk:
                tile.rect.x += scroll

        for item in self.items:
            item.rect.x += scroll

    def spawn_enemy(self, spawn_range_a: int, spawn_range_b: int, i: int, t: str) -> list:
        enemies = []
        for _i in range(i):
            if t == "zombie":
                enemies.append(Zombie(random.randint(spawn_range_a, spawn_range_b), -200))
            else:
                enemies.append(Gunner(random.randint(spawn_range_a, spawn_range_b), -200))
        return enemies
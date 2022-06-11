import pygame
import sys
import random
from pygame import K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL, QUIT, K_a, K_d, mixer

from settings import *
from player import Player
from tile import Tile
from map import Map
from zombie import Zombie
from background import BG
from commands import Commands

pygame.init()
pygame.font.init()
mixer.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

def main():
    clock = pygame.time.Clock()
    FPS = 60

    right = False
    left = False
    active = False

    enemies = []

    map = Map()
    background = BG(bg)
    commands = Commands()

    player = Player(200, 200)

    scroll = 0
    
    last_tile =  CHUNK_SIZE * TILE_SIZE
    
    noise_x = CHUNK_SIZE * 4

    for i in range(10, 5, -1):
        enemy = Zombie(100 * i, 200)
        enemies.append(enemy)

    def redraw_window():
        WIN.fill(BLACK)

        WIN.blit(bg, (0, 0))

        map.draw_deco(WIN)
        map.draw_items(WIN)
        map.draw(WIN)
        
        WIN.blit(main_font.render(str(round(clock.get_fps())), 1, BLACK), (210, 0))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while 1:
        clock.tick(FPS)

        daytime = background.get_daytime()

        if not active:
            if last_tile < -CHUNK_SIZE * TILE_SIZE:
                x = round((last_tile + CHUNK_SIZE * TILE_SIZE * 3) / CHUNK_SIZE / TILE_SIZE, 1) - 0.2
                chunk, deco, items = map.generate_chunk(x, 0, noise_x)
                map.obstacles.append(chunk)
                map.deco.append(deco)
                map.items.append(items)

                chunk, deco, items = map.generate_chunk(x, 1, noise_x)
                map.obstacles.append(chunk)
                map.deco.append(deco)
                map.items.append(items)

                del map.obstacles[0]
                del map.obstacles[1]

                del map.deco[0]
                del map.deco[1]

                try:
                    del map.items[0]
                    del map.items[1]
                except:
                    pass

                last_tile = -TILE_SIZE
                noise_x += CHUNK_SIZE

            last_tile += scroll

            map.camera(scroll)
            for enemy in enemies:
                enemy.camera(scroll)

            if player.alive():
                scroll = player.move(right, left, map.obstacles, map.items)
                player.move_bullets(map.obstacles, enemies)
                player.get_desire()
                player.check_shoot()
                map.items = player.item_collision(map.items)
                if player.current_item == 2:
                    player.attack_hit(enemies)
            else:
                finished = player.death_animation()
                if finished:
                    pass

            for enemy in enemies:
                if enemy.alive():
                    enemy.move(map.obstacles, player, daytime)
                else:
                    finished = enemy.death_animation()
                    if finished:
                        enemies.remove(enemy)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_d:
                        right = True
                    elif event.key == K_a:
                        left = True
                    elif event.key == K_SPACE:
                        if not player.jumping:
                            player.jumping = True
                    elif event.key == pygame.K_ESCAPE:
                        active = True

                if event.type == KEYUP:
                    if event.key == K_d:
                        right = False
                    elif event.key == K_a:
                        left = False
                if event.type == MOUSEWHEEL:
                    player.next_item()
                
            redraw_window()
        else:
            commands.draw(WIN)
            pygame.display.update()

            commands.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        commands.r_input()
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        commands.remove_letter()
                    elif event.unicode.isalpha():
                        commands.append_letter(event.unicode)
                    
                    

main()

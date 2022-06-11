import pygame
import sys
import random
from pygame import K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL, QUIT, K_a, K_d, mixer
from argparse import ArgumentParser

from settings import *
from player import Player
from tile import Tile
from map import Map
from zombie import Zombie
from background import BG
from gunner import Gunner
from commands import Commands

pygame.init()
pygame.font.init()
mixer.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

def survival_mode(background):
    clock = pygame.time.Clock()
    FPS = 60

    right = False
    left = False
    active = False

    map = Map()
    commands = Commands()

    player = Player(200, 200)

    scroll = 0
    
    last_tile =  CHUNK_SIZE * TILE_SIZE
    
    noise_x = CHUNK_SIZE * 4

    def redraw_window():
        WIN.fill(BLACK)

        background.draw(WIN)

        map.draw_deco(WIN)
        map.draw_items(WIN)
        map.draw(WIN)
        
        WIN.blit(main_font.render(str(round(clock.get_fps())), 1, BLACK), (210, 0))
        
        for enemy in map.enemies:
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
                map.enemies += map.generate_enemy(x, daytime)
                map.obstacles.append(chunk)
                map.deco.append(deco)
                if items != []:
                    map.items += items

                chunk, deco, items = map.generate_chunk(x, 1, noise_x)
                map.obstacles.append(chunk)
                map.deco.append(deco)
                if items != []:
                    map.items += items

                del map.obstacles[0]
                del map.obstacles[1]

                del map.deco[0]
                del map.deco[1]

                last_tile = -TILE_SIZE
                noise_x += CHUNK_SIZE

            last_tile += scroll

            map.camera(scroll)
            for enemy in map.enemies:
                enemy.camera(scroll)

            if player.alive():
                scroll = player.move(right, left, map.obstacles, map.items, CAMERA_LIM)
                player.move_bullets(map.obstacles, map.enemies)
                player.get_desire()
                player.food_shortage()
                player.check_shoot()
                map.items = player.item_collision(map.items)
                if player.current_item == 2:
                    player.attack_hit(map.enemies)
            else:
                scroll = 0
                finished = player.death_animation(map.obstacles)
                if finished:
                    pass

            for enemy in map.enemies:
                if enemy.alive():
                    enemy.move(map.obstacles, player, daytime)
                else:
                    finished = enemy.death_animation(map.obstacles)
                    if finished:
                        map.enemies.remove(enemy)

            background.day_night_cycle()
            
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
                        player.jump()
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
                        t = commands.r_input()
                        background.command(t)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        commands.remove_letter()
                    elif event.unicode.isalpha():
                        commands.append_letter(event.unicode)
                    
def zombie_mode(background):
    clock = pygame.time.Clock()
    FPS = 60

    time = 0
    score = 0

    spawn_density = 120

    right = False
    left = False

    map = Map()
    map.items = []
    map.enemies = []
    map.obstacles = []
    map.deco = []

    with open("level.txt", "r") as f:
        target_y = 0
        for line in f:
            chunk = []
            target_x = 0
            for tile in range(0, len(line), 2):
                if line[tile] != "0":
                    chunk.append(Tile(target_x * TILE_SIZE, target_y * TILE_SIZE, int(line[tile])))
                target_x += 1
            map.obstacles.append(chunk)
            target_y += 1

        

    background.set_daytime("night")

    commands = Commands()

    player = Player(200, 200)

    kills = main_font.render("Kills: " + str(score), 1, BLACK)

    def redraw_window():
        background.draw(WIN)

        map.draw_deco(WIN)
        map.draw(WIN)

        WIN.blit(main_font.render(str(round(clock.get_fps())), 1, BLACK), (210, 0))
        WIN.blit(kills, (WIDTH - kills.get_width(), 0))
        
        for enemy in map.enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while 1:
        clock.tick(FPS)

        kills = main_font.render("Kills: " + str(score), 1, BLACK)

        if player.alive():
            player.move(right, left, map.obstacles, map.items, 0)
            player.move_bullets(map.obstacles, map.enemies)
            player.check_shoot()
            if player.current_item == 2:
                player.attack_hit(map.enemies)
        else:
            finished = player.death_animation(map.obstacles)
            if finished:
                pass
    
        for enemy in map.enemies:
            if enemy.alive():
                enemy.move(map.obstacles, player, "day")
            else:
                finished = enemy.death_animation(map.obstacles)
                if not enemy.score_added:
                    score += 1
                    enemy.score_added = True
                if finished:
                    map.enemies.remove(enemy)

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
                    player.jump()
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

        # generate enemies
        if time >= spawn_density:
            enem = map.spawn_enemy(0, WIDTH, 1, "zombie")
            for e in enem:
                e.seeing_distance = 900
            map.enemies += map.spawn_enemy(0, WIDTH, 1, "zombie")
            time = 0
            if spawn_density > 45:
                spawn_density -= 1

        time += 1

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--day", action="store_true", help="Set Daytime to Day")
    parser.add_argument("-n", "--night", action="store_true", help="Set Daytime to Night")
    parser.add_argument("-z", "--zombie", action="store_true", help="Set Mode to Zombie Mode")

    args, leftovers = parser.parse_known_args()

    background = BG(bg)

    if args.night:
        background.command("/night")
    if args.zombie:
        zombie_mode(background)
    else:
        survival_mode(background)

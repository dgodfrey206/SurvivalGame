import pygame
# initializing pygame
pygame.init()
pygame.display.init()

# tile size, chunk size
TILE_SIZE = 75
CHUNK_SIZE = 8
# width, height of window
WIDTH, HEIGHT = 1100, 700
# window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# caption
pygame.display.set_caption("Survival Platformer")
# main font
main_font = pygame.font.SysFont("Arial", 30)
# tile types
TILES = 18
ITEMS = 8
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (239, 62, 91)
BLUE = (63, 100, 126)
# scroll > when player gets to CAMERA_LIM before screen end > stops moving and camera starts scrolling
CAMERA_LIM = 300

# background
bg = pygame.transform.scale(pygame.image.load("images/bg/bg.png"), (WIDTH, HEIGHT)).convert()
night = pygame.transform.scale(pygame.image.load("images/bg/bg_night.png"), (WIDTH, HEIGHT)).convert()
BULLET = pygame.transform.scale(pygame.image.load("images/items/bullet.png"), (12, 6)).convert()

# settings/balancing
PISTOL_DAMAGE = 50
SWORD_DAMAGE = 100

FOOD_DECREASE = 2

ZOMBIE_DAMAGE = 10
GUNNER_DAMAGE = 10
GUNNER_COOLDOWN = 60
# all tile images
tiles = []
items = []
item_values = [10, 10, 15, 20, 30, 20, 10, 10]
for i in range(1, TILES + 1):
    if i < 9:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE, TILE_SIZE)).convert_alpha()
    elif i < 12:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE / 2, TILE_SIZE / 4)).convert_alpha()
    elif i < 14:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE, TILE_SIZE / 2)).convert_alpha()
    elif i < 15:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE, TILE_SIZE)).convert_alpha()
    elif i < 17:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE * 3, TILE_SIZE)).convert_alpha()
    elif i < 18:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE * 0.95, TILE_SIZE * 2.25)).convert_alpha()
    else:
        img = pygame.transform.scale(pygame.image.load("images/tiles/{}.png".format(i)), (TILE_SIZE * 0.85, TILE_SIZE * 1.5)).convert_alpha()

    tiles.append(img)

for i in range(1, ITEMS + 1):
    img = pygame.transform.scale(pygame.image.load("images/items/{}.png".format(i)), (TILE_SIZE / 2, TILE_SIZE / 2)).convert_alpha()

    items.append(img)
    
    

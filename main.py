import sys, random, time
from pygame.locals import *
from classes import *

#set up pygame
pygame.init()
vec = pygame.math.Vector2

#constants
HEIGHT = 900
WIDTH = 1600
FPS = 60

FramePerSec = pygame.time.Clock()

#display setup
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

import title_screen, test_screen

current_screen = get_screens()["title_screen"]

while True:
    displaysurface.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    update_info = current_screen.update()
    #print(current_screen.screen_name)

    #returns {
    # sprite_group:pygame.sprite.Group(),
    # next_screen:screen to switch to, normally None
    # }
    if update_info["next_screen"]: #switches screens if needed
        current_screen = update_info["next_screen"]
        current_screen.load()
    
    else: #blit all sprites
        for entity in update_info["sprite_group"]:
            displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

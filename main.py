import sys, random, time
from pygame.locals import *
from ui_objects import *

# set up pygame
pygame.init()

# constants
WIDTH,HEIGHT = get_screen_size()
FPS = 60

FramePerSec = pygame.time.Clock()

# display setup
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

import title_screen, game_screen, tutorial_screen, game_over_screen # runs the files and create the screen objects

def quit():
    pygame.quit()

def start():
    current_screen = get_screens()["title_screen"] # set the first screen
    current_screen.load() # load the first screen
    
    while True: # loop
        displaysurface.fill((255,255,255)) # fill bg to cover up previous frame

        for event in pygame.event.get(): # check if you quit
            if event.type == QUIT:
                quit()
        
        update_info = current_screen.update() # runs update on the current screen

        # returns {
        # sprite_group:pygame.sprite.Group(),
        # next_screen:screen to switch to, normally None
        # }

        if update_info["next_screen"]: # switches screens if needed
            current_screen = update_info["next_screen"] # sets it to the current
            current_screen.load() # loads it

        else: #blit all sprites
            for entity in update_info["sprite_group"]:
                displaysurface.blit(entity.surf, entity.rect)
        
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    start()
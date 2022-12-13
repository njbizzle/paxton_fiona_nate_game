from ui_objects import *
from datetime import datetime

WIDTH,HEIGHT = get_screen_size()

all_sprites = pygame.sprite.Group()

next_screen = None

wave = 0

def set_wave(n):
    global wave
    wave = n

def game_screen_click():
    global next_screen
    next_screen = get_screens()["game_screen"]

def title_screen_click():
    global next_screen
    next_screen = get_screens()["title_screen"]

text("GAME OVER", (WIDTH/2, HEIGHT*0.3), (255,0,0), get_font(100), group=all_sprites)
wavetext = text(f"You survived until wave {wave}", (WIDTH/2, HEIGHT*0.5), (0,0,0), get_font(50), group=all_sprites)
game_screen_button = button("play again", rect=pygame.Rect((WIDTH/2-100, HEIGHT*0.7),(200,50)), on_click=game_screen_click, group=all_sprites)
title_screen_button = button("to title screen", rect=pygame.Rect((WIDTH/2-100, HEIGHT*0.8),(200,50)), on_click=title_screen_click, group=all_sprites)

def game_over_screen_init():
    pass

def game_over_screen_load():
    global next_screen
    next_screen = None

    wavetext.update_text(f"you survived until wave {wave}")

def game_over_screen_update():
    global next_screen

    for sprite in all_sprites:
        try:
            sprite.check_click()
        except:
            pass

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_over_screen = screen("game_over_screen", game_over_screen_init, game_over_screen_load, game_over_screen_update)
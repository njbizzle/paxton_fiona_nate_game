from ui_objects import *
from datetime import datetime

all_sprites = pygame.sprite.Group()

time_init = text("0", (200,100), (0,255,0), get_font(30), all_sprites)
time_loaded = text("0", (200,200), (0,255,0), get_font(30), all_sprites)
time_update = text("0", (200,300), (0,255,0), get_font(30), all_sprites)

next_screen_button_pressed = False

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

next_screen_button = button("to game screen", rect=pygame.Rect((500,500),(100,100)), on_click=next_screen_button_click, group=all_sprites)


def update_time(text_sprite):
    text_sprite.update_text(f"{str(datetime.now())} title screen")

def title_screen_init():
    global time_init
    update_time(time_init)

def title_screen_load():
    global time_loaded, next_screen_button_pressed

    update_time(time_loaded)
    next_screen_button_pressed = False

def title_screen_update():
    global time_update

    keys_pressed = pygame.key.get_pressed()

    next_screen_button.check_click()
    if next_screen_button_pressed == True:
        next_screen = get_screens()["game_screen"]
    else:
        next_screen = None
    
    update_time(time_update)


    return {"sprite_group":all_sprites, "next_screen":next_screen}

title_screen = screen("title_screen", title_screen_init, title_screen_load, title_screen_update)
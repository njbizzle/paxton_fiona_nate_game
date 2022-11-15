from ui_objects import *
from datetime import datetime

time_init = text("0", (100,100), (0,255,0), get_font(30))
time_loaded = text("0", (100,200), (0,255,0), get_font(30))
time_update = text("0", (100,300), (0,255,0), get_font(30))

all_sprites = pygame.sprite.Group()

next_screen_button_pressed = False

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

next_screen_button = button("to game screen", rect=pygame.Rect((500,500),(100,100)), on_click=next_screen_button_click)

all_sprites.add(next_screen_button)
all_sprites.add(next_screen_button.text_sprite)

def update_time(text_sprite):
    all_sprites.remove(text_sprite)
    text_ =  text(f"{str(datetime.now())} title screen", (text_sprite.rect.center), (0,0,0), text_sprite.font)
    all_sprites.add(text_)
    return text_

def title_screen_init():
    global time_init
    time_init = update_time(time_init)

def title_screen_load():
    global time_loaded, next_screen_button_pressed

    time_loaded = update_time(time_loaded)
    next_screen_button_pressed = False

def title_screen_update():
    global time_update, button_pressed

    keys_pressed = pygame.key.get_pressed()

    next_screen_button.check_click()
    if next_screen_button_pressed == True:
        next_screen = get_screens()["game_screen"]
    else:
        next_screen = None
    
    time_update = update_time(time_update)


    return {"sprite_group":all_sprites, "next_screen":next_screen}

title_screen = screen("title_screen", title_screen_init, title_screen_load, title_screen_update)
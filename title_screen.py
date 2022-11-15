from classes import *
from datetime import datetime

print("file run title screen")

time_init = text("0", (0,255,0), (100,100), get_font(30))
time_loaded = text("0", (0,255,0), (100,200), get_font(30))
time_update = text("0", (0,255,0), (100,300), get_font(30))

all_sprites = pygame.sprite.Group()

def update_time(text_sprite):
    all_sprites.remove(text_sprite)
    text_ =  text(f"{str(datetime.now())} title screen", (0,0,0), (text_sprite.rect.center), text_sprite.font)
    all_sprites.add(text_)
    return text_

def title_screen_init():
    global time_init

    print("init title screen")
    time_init = update_time(time_init)

def title_screen_load():
    global time_loaded

    print("load title screen")
    time_loaded = update_time(time_loaded)

def title_screen_update():
    global time_update

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        next_screen = get_screens()["test_screen"]
    else:
        next_screen = None
    
    time_update = update_time(time_update)


    return {"sprite_group":all_sprites, "next_screen":next_screen}

title_screen = screen("title_screen", title_screen_init, title_screen_load, title_screen_update)
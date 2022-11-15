from classes import *
from datetime import datetime

print("file run test screen")

time_init = text("0", (0,255,0), (100,100), get_font(30))
time_loaded = text("0", (0,255,0), (100,200), get_font(30))
time_update = text("0", (0,255,0), (100,300), get_font(30))

all_sprites = pygame.sprite.Group()

def update_time(text_sprite):
    all_sprites.remove(text_sprite)
    text_ =  text(f"{str(datetime.now())} test screen", (0,0,0), (text_sprite.rect.center), text_sprite.font)
    all_sprites.add(text_)
    return text_

def test_screen_init():
    global time_init

    print("init test screen")
    time_init = update_time(time_init)

def test_screen_load():
    global time_loaded

    print("load test screen")
    time_loaded = update_time(time_loaded)

def test_screen_update():
    global time_update

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None
    
    time_update = update_time(time_update)


    return {"sprite_group":all_sprites, "next_screen":next_screen}

test_screen = screen("test_screen", test_screen_init, test_screen_load, test_screen_update)
from ui_objects import *

all_sprites = pygame.sprite.Group()

# button ui

next_screen_button_pressed = False

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

next_screen_button = button("to title screen", rect=pygame.Rect((1000,500), (100,100)), on_click=next_screen_button_click)

all_sprites.add(next_screen_button)
all_sprites.add(next_screen_button.text_sprite)



def game_screen_init():
    pass

def game_screen_load():
    global next_screen_button_pressed
    next_screen_button_pressed = False

def game_screen_update():
    global next_screen_button_pressed

    keys_pressed = pygame.key.get_pressed()

    next_screen_button.check_click()
    if next_screen_button_pressed == True:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)
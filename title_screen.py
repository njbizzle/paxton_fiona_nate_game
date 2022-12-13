from ui_objects import *
from datetime import datetime

WIDTH,HEIGHT = get_screen_size()

all_sprites = pygame.sprite.Group()

next_screen = None

def game_screen_click():
    global next_screen
    next_screen = get_screens()["game_screen"]

def tutorial_screen_click():
    global next_screen
    next_screen = get_screens()["tutorial_screen"]

def quit_click():
    from main import quit
    quit()

title = text("name of the game or something idk", (WIDTH/2, HEIGHT*0.3), (0,0,0), font=get_font(70), group=all_sprites)

game_screen_button = button("PLAY GAME", rect=pygame.Rect((WIDTH/2-200,HEIGHT*0.55),(400,100)), on_click=game_screen_click, font=50, group=all_sprites)
tutorial_screen_button = button("tutorial", rect=pygame.Rect((WIDTH/2-150,HEIGHT*0.7),(300,70)), on_click=tutorial_screen_click, font=30, group=all_sprites)
quit_button = button("quit game", rect=pygame.Rect((WIDTH/2-100,HEIGHT*0.85),(200,50)), on_click=quit_click, font=20, group=all_sprites)

def title_screen_init():
    pass

def title_screen_load():
    global next_screen
    next_screen = None

def title_screen_update():
    global next_screen

    for sprite in all_sprites:
        try:
            sprite.check_click()
        except:
            pass

    return {"sprite_group":all_sprites, "next_screen":next_screen}

title_screen = screen("title_screen", title_screen_init, title_screen_load, title_screen_update)
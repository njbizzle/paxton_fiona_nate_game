from ui_objects import *
from datetime import datetime

WIDTH,HEIGHT = get_screen_size()

all_sprites = pygame.sprite.Group()

next_screen = None

def title_screen_click():
    global next_screen
    next_screen = get_screens()["title_screen"]

text("CONTROLS", (WIDTH/2, HEIGHT*0.15), (0,0,0), font=get_font(40), group=all_sprites)
text("MOVE CONTROLS | go up = w/up arrow | go down = s/down arrow | go left = a/left arrow | go right = d/right arrow | sprint = left shift", (WIDTH/2, HEIGHT*0.25), (0,0,0), font=get_font(20), group=all_sprites)
text("SHOOTING | shoot = space | aim = points at mouse | reload = r | OTHER | zoom in = z/o | zoom out = x/p | pause = escape |", (WIDTH/2, HEIGHT*0.3), (0,0,0), font=get_font(25), group=all_sprites)

text("MECHANICS", (WIDTH/2, HEIGHT*0.5), (0,0,0), font=get_font(40), group=all_sprites)
text("Enemies spawn in a cicle arond you in waves, the number of enemies is equal to the number of the wave (exsample: wave 5 has 5 enemies).", (WIDTH/2, HEIGHT*0.6), (0,0,0), font=get_font(20), group=all_sprites)
text("Your health starts at 100, when ever an enemy thouches you your health decreases by 25 and you are launched away and given 1.5 seconds of invincibility.", (WIDTH/2, HEIGHT*0.65), (0,0,0), font=get_font(20), group=all_sprites)
text("Stamina allows you to sprint which allows you to move faster then the enemies. Sprinting costs stamina, when stamina is 0 it will not regenerate until you stop sprinting.", (WIDTH/2, HEIGHT*0.70), (0,0,0), font=get_font(17), group=all_sprites)
text("Shooting an enemy does 10 damage and costs ammo which is shown on screen, when your ammo reaches 0 you have to reload to be able to shoot. While you are reloading you can not shoot.", (WIDTH/2, HEIGHT*0.75), (0,0,0), font=get_font(17), group=all_sprites)
text("Touching water will slow you down and you will be unable to sprint. Enemies are unaffected by water. Also aim for the top right corners of the enemies. (its a feature not a bug)", (WIDTH/2, HEIGHT*0.80), (0,0,0), font=get_font(17), group=all_sprites)

title_screen_button = button("back", rect=pygame.Rect((WIDTH/2-100, HEIGHT*0.90),(200,50)), on_click=title_screen_click, group=all_sprites)

def tutorial_screen_init():
    pass

def tutorial_screen_load():
    global next_screen
    next_screen = None

def tutorial_screen_update():
    global next_screen

    for sprite in all_sprites:
        try:
            sprite.check_click()
        except:
            pass

    return {"sprite_group":all_sprites, "next_screen":next_screen}

tutorial_screen = screen("tutorial_screen", tutorial_screen_init, tutorial_screen_load, tutorial_screen_update)
from ui_objects import *
from camera import camera
from test_rect import Test_rect

vec = pygame.math.Vector2

HEIGHT = 900
WIDTH = 1600

non_camera_sprites = pygame.sprite.Group()

# button ui
next_screen_button_pressed = False

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

next_screen_button = button("to title screen", rect=pygame.Rect((1000,500), (100,100)), on_click=next_screen_button_click)

non_camera_sprites.add(next_screen_button)
non_camera_sprites.add(next_screen_button.text_sprite)

def game_screen_init():
    test_rect1 = Test_rect(pygame.Rect((0,0), (1, 1)), (255,0,0))
    test_rect1 = Test_rect(pygame.Rect((-5,5), (2, 2)), (0,255,0))
    test_rect1 = Test_rect(pygame.Rect((-5,2), (1, 1)), (0,0,255))

def game_screen_load():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale
    next_screen_button_pressed = False
    camera_x, camera_y, camera_scale = [0,0,100]

def game_screen_update():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP]:
        camera_y+=0.1
    if keys_pressed[pygame.K_DOWN]:
        camera_y-=0.1
    if keys_pressed[pygame.K_LEFT]:
        camera_x-=0.1
    if keys_pressed[pygame.K_RIGHT]:
        camera_x+=0.1

    if keys_pressed[pygame.K_q]:
        camera_scale+=3
    if keys_pressed[pygame.K_w]:
        camera_scale-=3

    next_screen_button.check_click()
    if next_screen_button_pressed == True:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None
    
    all_sprites = pygame.sprite.Group()

    for sprite in camera.get_displayed_sprites(vec(camera_x, camera_y),vec(WIDTH,HEIGHT), camera_scale, use_rect_colliders=True):
        all_sprites.add(sprite)

    for sprite in non_camera_sprites:
        all_sprites.add(sprite)

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)
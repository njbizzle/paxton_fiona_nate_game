from ui_objects import *
from camera import camera
from test_rect import Test_rect

vec = pygame.math.Vector2

HEIGHT = 900
WIDTH = 1600

non_camera_sprites = pygame.sprite.Group()

camera_pos_text = text("x: 0, y 0", (200,100), (0,0,0), get_font(30), non_camera_sprites)
camera_scale_text = text("scale: 0", (200,200), (0,0,0), get_font(30), non_camera_sprites)
objects_rendered_text = text("objects_rendered: 0", (200,300), (0,0,0), get_font(30), non_camera_sprites)

# button ui
next_screen_button_pressed = False

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

next_screen_button = button("to title screen", rect=pygame.Rect((1000,500), (100,100)), on_click=next_screen_button_click, group=non_camera_sprites)

non_camera_sprites.add(next_screen_button)
non_camera_sprites.add(next_screen_button.text_sprite)

def game_screen_init():
    test_rect1 = Test_rect(pygame.Rect((0,0), (1, 1)), (255,0,0))
    test_rect2 = Test_rect(pygame.Rect((-5,5), (1, 2)), (0,255,0))
    test_rect3 = Test_rect(pygame.Rect((-5,2), (2, 1)), (0,0,255))
    test_rect4 = Test_rect(pygame.Rect((-1,-1), (1, 1)), (0,0,0))
    test_rect4 = Test_rect(pygame.Rect((4,-4), (3, 1)), (255,0,255))

def game_screen_load():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale
    next_screen_button_pressed = False
    camera_x, camera_y, camera_scale = [0,0,100]

def game_screen_update():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale

    keys_pressed = pygame.key.get_pressed()

    camera_speed = 0.1

    if keys_pressed[pygame.K_LSHIFT]:
        camera_speed = 0.5

    if keys_pressed[pygame.K_UP]:
        camera_y+=camera_speed
    if keys_pressed[pygame.K_DOWN]:
        camera_y-=camera_speed
    if keys_pressed[pygame.K_LEFT]:
        camera_x-=camera_speed
    if keys_pressed[pygame.K_RIGHT]:
        camera_x+=camera_speed

    if keys_pressed[pygame.K_z]:
        camera_scale+=camera_speed*20
    if keys_pressed[pygame.K_x]:
        camera_scale-=camera_speed*20

    if camera_scale < 1:
        camera_scale = 1

    next_screen_button.check_click()
    if next_screen_button_pressed == True:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None
    
    all_sprites = pygame.sprite.Group()

    for sprite in camera.get_displayed_sprites(vec(camera_x, camera_y),vec(WIDTH,HEIGHT), camera_scale, render_everything=False):
        all_sprites.add(sprite)

    camera_pos_text.update_text(f"x: {round(camera_x,2)}, y {round(camera_y,2)}")
    camera_scale_text.update_text(f"scale: {camera_scale}")
    objects_rendered_text.update_text(f"objects_rendered: {len(all_sprites)}")

    for sprite in non_camera_sprites:
        all_sprites.add(sprite)

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)
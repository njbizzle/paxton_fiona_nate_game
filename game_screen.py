from ui_objects import *

from camera import camera
from game_timer import start_game_timer, update_enemies
from test_objects import Test_rect
from player import player

from datetime import datetime
import math, time, threading

vec = pygame.math.Vector2

HEIGHT = 900
WIDTH = 1600
CAMERA_MIN, CAMERA_MAX = 0.06, 3

CONTROLS = {"up":[pygame.K_UP, pygame.K_w], "down":[pygame.K_DOWN, pygame.K_s], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d],
"zoom_in":[pygame.K_z], "zoom_out":[pygame.K_x], "speed_up":[pygame.K_LSHIFT], "super_speed":[pygame.K_LCTRL]}

def check_control(keys_pressed, key_name):
    if True in [keys_pressed[key] for key in CONTROLS[key_name]]:
        return True
    else:
        return False

def check_controls(keys_pressed, key_names):
    return [check_control(keys_pressed, key_name) for key_name in key_names]

non_camera_sprites = pygame.sprite.Group()

camera_pos_text = text("x: 0.0 y 0.0", (200,50), (0,0,0), get_font(30), non_camera_sprites)
camera_scale_text = text("scale: 0", (200,100), (0,0,0), get_font(30), non_camera_sprites)
objects_rendered_text = text("objects_rendered: 0", (200,150), (0,0,0), get_font(30), non_camera_sprites)

# button ui
next_screen_button_pressed = False
show_lines = False
render_all = False
show_ground = False

def reset_button_click():
    game_screen_load()

def next_screen_button_click():
    global next_screen_button_pressed
    next_screen_button_pressed = True

def show_lines_click():
    global show_lines
    if show_lines:
        show_lines = False
        show_lines_button.update_text("show lines")
    else:
        show_lines = True
        show_lines_button.update_text("hide lines")


def render_all_click():
    global render_all
    if render_all:
        render_all = False
        render_all_button.update_text("render all")
    else:
        render_all = True
        render_all_button.update_text("render in camera")

def show_ground_click():
    global show_ground
    if show_ground:
        show_ground = False
        show_ground_button.update_text("hide ground")
    else:
        show_ground = True
        show_ground_button.update_text("show ground")

reset_button = button("reset", rect=pygame.Rect((100,200), (200,50)), on_click=reset_button_click, group=non_camera_sprites)
next_screen_button = button("to title screen", rect=pygame.Rect((100,260), (200,50)), on_click=next_screen_button_click, group=non_camera_sprites)
show_lines_button = button("show lines", rect=pygame.Rect((100,320), (200,50)), on_click=show_lines_click, group=non_camera_sprites)
render_all_button = button("render all", rect=pygame.Rect((100,380), (200,50)), on_click=render_all_click, group=non_camera_sprites)
show_ground_button = button("hide ground", rect=pygame.Rect((100,380), (200,50)), on_click=show_ground_click, group=non_camera_sprites)

def game_screen_init():
    pass

def game_screen_load():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale

    game_timer_thread = threading.Thread(target=start_game_timer)
    game_timer_thread.start()

    next_screen_button_pressed = False
    camera_x, camera_y, camera_scale = [0.0, 0.0, 1.0]

def game_screen_update():
    global next_screen_button_pressed, camera_x, camera_y, camera_scale

    keys_pressed = pygame.key.get_pressed()

    camera_move_speed = 0.05
    camera_scale_speed = 30
    
    player.update(check_controls(keys_pressed, ["up", "down", "left", "right"]))
    update_enemies()

    if check_control(keys_pressed, "zoom_in"):
        camera_scale = camera_scale*(1+1/camera_scale_speed)
    if check_control(keys_pressed, "zoom_out"):
        camera_scale = camera_scale*(1-1/camera_scale_speed)
    
    if camera_scale < CAMERA_MIN:
        camera_scale = CAMERA_MIN
    if camera_scale > CAMERA_MAX:
        camera_scale = CAMERA_MAX

    reset_button.check_click()
    next_screen_button.check_click()
    show_lines_button.check_click()
    render_all_button.check_click()

    if next_screen_button_pressed == True:
        next_screen = get_screens()["title_screen"]
    else:
        next_screen = None
    
    all_sprites = pygame.sprite.Group()

    player_pos = player.get_pos()

    camera_x, camera_y = interpolate((camera_x, camera_y), player_pos, camera_move_speed)

    camera.update_camera(vec(camera_x, camera_y),vec(WIDTH,HEIGHT), camera_scale, show_lines=show_lines, render_everything=render_all)
    displayed_sprites = camera.get_displayed_sprites()
    
    for sprite in displayed_sprites:
        all_sprites.add(sprite)

    camera_pos_text.update_text(f"x: {round(player_pos[0],2)}, y {round(player_pos[1],2)}")
    camera_scale_text.update_text(f"scale: {round(camera_scale, 2)}")
    objects_rendered_text.update_text(f"objects_rendered: {len(all_sprites)}")

    for sprite in non_camera_sprites:
        all_sprites.add(sprite)

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)

def interpolate(vec1, vec2, num):
    if num > 0.5:
        print("hell nah")
        return
    x1,y1 = vec1
    x2,y2 = vec2
    
    x_dif = x2-x1
    y_dif = y2-y1
    try:
        return (x1+num*x_dif, y1+num*y_dif)
    except:
        return (x1,y1)

vec1 = (20,20)
vec2 = (10,10)
for i in range(0,10):
    vec1 = interpolate(vec1, vec2, 0.5)
    print(vec1)
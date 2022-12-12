from ui_objects import *

from camera import camera
from test_objects import Test_rect
from player import player
from worldmap import worldmap

from datetime import datetime
import game_timer

vec = pygame.math.Vector2

HEIGHT = 900
WIDTH = 1600
CAMERA_MIN, CAMERA_MAX = 0.25, 3

# controls

CONTROLS = {"up":[pygame.K_UP, pygame.K_w], "down":[pygame.K_DOWN, pygame.K_s], "left":[pygame.K_LEFT, pygame.K_a], "right":[pygame.K_RIGHT, pygame.K_d],
"zoom_in":[pygame.K_z, pygame.K_PLUS], "zoom_out":[pygame.K_x, pygame.K_MINUS], "sprint":[pygame.K_LSHIFT], "debug1":[pygame.K_n], "debug2":[pygame.K_m], "pause":[pygame.K_ESCAPE], 
"shoot":[pygame.K_SPACE], "reload":[pygame.K_r]}

def check_control(keys_pressed, key_name):
    if True in [keys_pressed[key] for key in CONTROLS[key_name]]:
        return True
    else:
        return False

def check_controls(keys_pressed, key_names):
    return [check_control(keys_pressed, key_name) for key_name in key_names]

non_camera_sprites = pygame.sprite.Group()

wave_large_text = text("NOW DAY", (WIDTH/2,HEIGHT/2), (0,0,0), get_font(200), non_camera_sprites)

player_health_text = text("health: 100", (200,75), (0,0,0), get_font(30), non_camera_sprites)
player_stamina_text = text("stamina: 100", (500,75), (0,0,0), get_font(30), non_camera_sprites)
player_ammo_text = text("ammo: 100", (500,150), (0,0,0), get_font(50), non_camera_sprites)

wave_number_text = text("wave: 0", (200,150), (0,0,0), get_font(50), non_camera_sprites)

paused_sprites = pygame.sprite.Group()

next_screen = None

paused = False
paused_last = False


def reset_button_click():
    game_screen_load()

def to_title_screen():
    global next_screen
    next_screen = get_screens()["title_screen"]

title_screen_button = button("return to title screen", rect=pygame.Rect((WIDTH/2-200, HEIGHT/2+50), (400,75)), on_click=to_title_screen, group=paused_sprites)
reset_button = button("reset", rect=pygame.Rect((WIDTH/2-200, HEIGHT/2-100), (400,75)), on_click=reset_button_click, group=paused_sprites)

# debug

debug_sprites = pygame.sprite.Group()
debug_offset_y = 450
debug = False

camera_pos_text = text("x: 0.0 y 0.0", (200,50+debug_offset_y), (0,0,0), get_font(30), debug_sprites)
camera_scale_text = text("scale: 0", (200,100+debug_offset_y), (0,0,0), get_font(30), debug_sprites)
objects_rendered_text = text("objects_rendered: 0", (200,150+debug_offset_y), (0,0,0), get_font(30), debug_sprites)

show_lines = False
show_ground = False

def show_lines_click():
    global show_lines
    if show_lines:
        show_lines = False
        show_lines_button.update_text("show lines")
    else:
        show_lines = True
        show_lines_button.update_text("hide lines")

def show_ground_click():
    global show_ground
    if show_ground:
        show_ground = False
        show_ground_button.update_text("hide ground")
    else:
        show_ground = True
        show_ground_button.update_text("show ground")

show_lines_button = button("show lines", rect=pygame.Rect((100,260+debug_offset_y), (200,50)), on_click=show_lines_click, group=debug_sprites)
show_ground_button = button("hide ground", rect=pygame.Rect((100,320+debug_offset_y), (200,50)), on_click=show_ground_click, group=debug_sprites)

# actuall stuff

def game_screen_init():
    pass

def game_screen_load():
    global camera_x, camera_y, camera_scale, next_screen, paused, paused_last

    next_screen = None
    paused = False
    paused_last = False
    camera.set_dark(False)

    worldmap.reset()
    game_timer.reset()
    player.reset()

    camera_x, camera_y, camera_scale = [0.0, 0.0, 0.3]

def game_screen_update():
    global camera_x, camera_y, camera_scale, debug, paused, paused_last

    keys_pressed = pygame.key.get_pressed()

    camera_move_speed = 0.05
    camera_scale_speed = 30

    if check_control(keys_pressed, "pause"):
        if not(paused_last):
            paused = not(paused)
            camera.set_dark(paused)
        paused_last = True
    else:
        paused_last = False

    all_sprites = pygame.sprite.Group()
    
    if not(paused):
        player.update(check_controls(keys_pressed, ["up", "down", "left", "right", "shoot", "sprint", "reload"]))
        game_timer.game_timer()
        worldmap.enemy_sprites.update()

        if check_control(keys_pressed, "zoom_in"):
            camera_scale = camera_scale*(1+1/camera_scale_speed)
        if check_control(keys_pressed, "zoom_out"):
            camera_scale = camera_scale*(1-1/camera_scale_speed)

    camera.update_camera(vec(camera_x, camera_y),vec(WIDTH,HEIGHT), camera_scale, show_lines=show_lines, render_everything=show_ground)
    displayed_sprites = camera.get_displayed_sprites()

    for sprite in displayed_sprites:
        all_sprites.add(sprite)
        
    if camera_scale < CAMERA_MIN:
        camera_scale = CAMERA_MIN
    if camera_scale > CAMERA_MAX:
        camera_scale = CAMERA_MAX

    if check_controls(keys_pressed, ["debug1", "debug2"]) == [True, True]:
        debug = not(debug)

    camera_x, camera_y = interpolate((camera_x, camera_y), player.get_pos(), camera_move_speed)


    for sprite in non_camera_sprites:
        all_sprites.add(sprite)

    if debug:
        for button in debug_sprites:
            try:
                button.check_click()
            except:
                pass
        
        camera_pos_text.update_text(f"x: {round(player.get_pos()[0],2)}, y {round(player.get_pos()[1],2)}")
        camera_scale_text.update_text(f"scale: {round(camera_scale, 2)}")
        objects_rendered_text.update_text(f"objects_rendered: {len(all_sprites)}")

        for sprite in debug_sprites:
            all_sprites.add(sprite)
    

    if player.health < 30:
        player_health_text.update_text(f"health: {max(0, player.health)}", (255,0,0))
    else:
        player_health_text.update_text(f"health: {max(0, player.health)}", (0,0,0))

    if player.stamina < 30:
        player_stamina_text.update_text(f"stamina: {max(0, player.stamina)}", (255,0,0))
    else:
        player_stamina_text.update_text(f"stamina: {max(0, player.stamina)}", (0,0,0))

    reloading_text = ""

    if player.reloading:
        reloading_text = "(reloading)"

    if player.ammo == 0:
        player_ammo_text.update_text(f"ammo: 0 {reloading_text}", (255,0,0))
    else:
        player_ammo_text.update_text(f"ammo: {player.ammo} {reloading_text}", (0,0,0))

    wave = game_timer.get_wave()

    wave_number_text
    wave_number_text.update_text(f"wave: {wave}")

    if f"WAVE: {wave}" != wave_large_text.text_content:
        wave_large_text.update_text(f"WAVE: {wave}")
        wave_large_text.alpha = 255
    else:
        wave_large_text.update_text()

    wave_large_text.alpha -=5

    if paused:
        for sprite in paused_sprites:
            all_sprites.add(sprite)
            try:
                sprite.check_click()
            except:
                pass

    return {"sprite_group":all_sprites, "next_screen":next_screen}

game_screen = screen("game_screen", game_screen_init, game_screen_load, game_screen_update)

def interpolate(vec1, vec2, num):
    x1,y1 = vec1
    x2,y2 = vec2
    
    x_dif = x2-x1
    y_dif = y2-y1
    try:
        return (x1+num*x_dif, y1+num*y_dif)
    except:
        return (x1,y1)
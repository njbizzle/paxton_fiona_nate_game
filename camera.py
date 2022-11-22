from worldmap import worldmap
import pygame, math, time

HEIGHT = 900
WIDTH = 1600
RENDER_BUFFER = 100

CAMERA_LINE_WIDTH = 1
CAMERA_LINE_COLOR = (200,200,200)
CAMERA_LINES_GRID_SIZE = (100,100)

def convert_wm_surf(surf, wm_scale):
    surf_size = surf.get_size()
    return pygame.transform.scale(surf, (surf_size[0]* wm_scale, surf_size[1]* wm_scale))

def convert_wm_rect(rect, wm_scale, wall_l, wall_t):
    rect_pos = rect.topleft
    return pygame.Rect((wm_scale*(-wall_l + rect_pos[0]), wm_scale*(wall_t - rect_pos[1])), (rect.w*wm_scale, rect.h*wm_scale))

def convert_wm_sprite(sprite, wm_scale, wall_l, wall_t):
    new_surf = convert_wm_surf(sprite.surf, wm_scale)
    new_rect = convert_wm_rect(sprite.rect, wm_scale, wall_l, wall_t)
    return [new_surf, new_rect]
    
class Empty_sprite(pygame.sprite.Sprite):
    def __init__(self, surf, rect):
        super().__init__()
        self.surf = surf
        self.rect = rect

class Camera:
    def __init__(self):
        pass

    def get_displayed_sprites(self, pos_ws, size, wm_scale, use_rect_colliders = False, render_everything = False, show_lines = False):
        time_stamp = time.time()

        display_tile_h = size.x/wm_scale
        display_tile_w = size.y/wm_scale

        wall_l = (pos_ws.x - display_tile_h/2)
        wall_l_render = (pos_ws.x - display_tile_h/2) - RENDER_BUFFER

        wall_r = (pos_ws.x + display_tile_h/2)
        wall_r_render = (pos_ws.x + display_tile_h/2) + RENDER_BUFFER

        wall_b = (pos_ws.y - display_tile_w/2)
        wall_b_render = (pos_ws.y - display_tile_w/2) - RENDER_BUFFER
        
        wall_t = (pos_ws.y + display_tile_w/2)
        wall_t_render = (pos_ws.y + display_tile_w/2) + RENDER_BUFFER

        # gets [surface, position in wm]
        if render_everything:
            visable_sprites_wm = worldmap.get_all_sprites()
        elif use_rect_colliders:
            camera_rect = pygame.Rect(wall_l, wall_t, wall_r-wall_l, wall_t-wall_b) # uses rect collision
            visable_sprites_wm = worldmap.get_object_in_rect(camera_rect)
        else:
            visable_sprites_wm = worldmap.get_objects_in_tile_range((wall_l_render,wall_r_render),(wall_b_render,wall_t_render))

        visable_sprites_camera = []

        for sprite in visable_sprites_wm:
            new_surf, new_rect = convert_wm_sprite(sprite, wm_scale, wall_l, wall_t)
            visable_sprites_camera.append(Empty_sprite(new_surf, new_rect))
        
        if show_lines:
            lines = Empty_sprite(pygame.Surface((WIDTH,HEIGHT)), pygame.Rect(0,0,WIDTH,HEIGHT))
            lines.surf.set_colorkey((0,0,0))

            for hor_line_pos in range(math.floor(wall_b), math.ceil(wall_t)):
                if hor_line_pos%CAMERA_LINES_GRID_SIZE[0] == 0:
                    pos_on_camera = wm_scale*(wall_t - hor_line_pos)
                    pygame.draw.line(lines.surf, CAMERA_LINE_COLOR, (0, pos_on_camera), (WIDTH, pos_on_camera), 1)

            for vert_line_pos in range(math.floor(wall_l), math.ceil(wall_r)):
                if vert_line_pos%CAMERA_LINES_GRID_SIZE[1] == 0:
                    pos_on_camera = wm_scale*(-wall_l + vert_line_pos)
                    pygame.draw.line(lines.surf, CAMERA_LINE_COLOR, (pos_on_camera, 0), (pos_on_camera, HEIGHT), CAMERA_LINE_WIDTH)
                
            visable_sprites_camera.append(lines)
        
        return visable_sprites_camera # sprite class containing all the surfaces and their postion the camera

camera = Camera()
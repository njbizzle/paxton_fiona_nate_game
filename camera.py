from worldmap import worldmap
import pygame

RENDER_BUFFER = 10

class Sprite_on_camera(pygame.sprite.Sprite):
    def __init__(self, surf, rect):
        super().__init__()
        self.surf = surf
        self.rect = rect

class Camera:
    def __init__(self):
        pass

    def get_displayed_sprites_range(self, pos_ws, size, wm_scale):
        if wm_scale < 1:
            wm_scale = 1

        display_tile_h = size.x/wm_scale
        display_tile_w = size.y/wm_scale

        wall_l = round(pos_ws.x - display_tile_h/2)
        wall_l_render = round(pos_ws.x - display_tile_h/2) - RENDER_BUFFER

        wall_r = round(pos_ws.x + display_tile_h/2)
        wall_r_render = round(pos_ws.x + display_tile_h/2) + RENDER_BUFFER

        wall_b = round(pos_ws.y - display_tile_w/2)
        wall_b_render = round(pos_ws.y - display_tile_w/2) - RENDER_BUFFER
        
        wall_t = round(pos_ws.y + display_tile_w/2)
        wall_t_render = round(pos_ws.y + display_tile_w/2) + RENDER_BUFFER


        # gets [surface, position in wm]
        visable_sprites_wm = worldmap.get_object_at_tile_range((wall_l_render,wall_r_render),(wall_b_render,wall_t_render))

        visable_sprites_camera = []

        # convert to position on camera
        for sprite in visable_sprites_wm:
            surf_size = sprite.surf.get_size()
            new_surf = pygame.transform.scale(sprite.surf, (surf_size[0]* wm_scale, surf_size[1]* wm_scale))

            rect = sprite.rect
            rect_pos = sprite.rect.topleft
            new_rect = pygame.Rect((wm_scale*(-wall_l + rect_pos[0]), wm_scale*(wall_t - rect_pos[1])), (rect.w*wm_scale, rect.h*wm_scale))

            visable_sprites_camera.append(Sprite_on_camera(new_surf, new_rect))

        return visable_sprites_camera # sprite class containing all the surfaces and their postion the camera

camera = Camera()
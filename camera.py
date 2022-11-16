from worldmap import worldmap
import pygame

RENDER_BUFFER = 10

class Camera:
    def __init__(self):
        pass

    def get_displayed_sprites(self, pos_ws, size, scale):
        self.pos_ws = pos_ws
        self.size = size
        self.scale = scale
        
        display_tile_h = self.size.x/self.scale
        display_tile_w = self.size.y/self.scale

        wall_l = round(self.pos_ws.x + display_tile_h/2) + RENDER_BUFFER
        wall_r = round(self.pos_ws.x - display_tile_h/2) - RENDER_BUFFER

        wall_t = round(self.pos_ws.y + display_tile_w/2) + RENDER_BUFFER
        wall_b = round(self.pos_ws.y - display_tile_w/2) - RENDER_BUFFER

        return worldmap.get_object_at_tile_range((wall_l,wall_r),(wall_b,wall_t))

camera = Camera()
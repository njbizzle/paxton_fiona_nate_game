from worldmap import worldmap
import pygame, math, time

HEIGHT = 900
WIDTH = 1600
RENDER_BUFFER = 100 #equal to the radius of the largest sprite we have

CAMERA_LINE_WIDTH = 1
CAMERA_LINE_COLOR = (200,200,200)
CAMERA_LINES_GRID_SIZE = (100,100)

TIME_CHANGE_SPEED = 10
    
class Empty_sprite(pygame.sprite.Sprite):
    def __init__(self, surf, rect):
        super().__init__()
        self.surf = surf
        self.rect = rect

class Camera:
    def __init__(self):
        self.pos_ws = (0,0)
        self.size = (0,0)
        self.wm_scale = 0

        self.render_everything = False
        self.show_lines = False
        self.show_ground = False

        self.is_dark = False

        self.wall_l = 0
        self.wall_l_buffer = 0

        self.wall_r = 0
        self.wall_r_buffer = 0

        self.wall_b = 0
        self.wall_b_buffer = 0

        self.wall_t = 0
        self.wall_t_buffer = 0

        self.dark_screen_opacity = 0
        self.dark_screen_night_opacity = 150

        self.night_screen_surf = pygame.Surface((WIDTH,HEIGHT))
        self.night_screen_rect = self.night_screen_surf.get_rect(topleft=(0,0))

    def update_camera(self, pos_ws, size, wm_scale, use_rect_colliders = False, render_everything = False, show_lines = False):
        self.pos_ws = pos_ws
        self.size = size
        self.wm_scale = wm_scale

        self.render_everything = render_everything
        self.show_lines = show_lines


    def set_dark(self, is_dark):
        self.is_dark = is_dark

    def get_displayed_sprites(self):
        display_tile_h = self.size.x/self.wm_scale
        display_tile_w = self.size.y/self.wm_scale

        self.wall_l = (self.pos_ws.x - display_tile_h/2)
        self.wall_l_buffer = (self.pos_ws.x - display_tile_h/2) - RENDER_BUFFER

        self.wall_r = (self.pos_ws.x + display_tile_h/2)
        self.wall_r_buffer = (self.pos_ws.x + display_tile_h/2) + RENDER_BUFFER

        self.wall_b = (self.pos_ws.y - display_tile_w/2)
        self.wall_b_buffer = (self.pos_ws.y - display_tile_w/2) - RENDER_BUFFER
        
        self.wall_t = (self.pos_ws.y + display_tile_w/2)
        self.wall_t_buffer = (self.pos_ws.y + display_tile_w/2) + RENDER_BUFFER

        # gets [surface, position in wm]
        if self.render_everything:
            visable_sprites_wm = worldmap.get_all_sprites()
        else:
            visable_sprites_wm = worldmap.get_objects_in_tile_range((self.wall_l_buffer, self.wall_r_buffer),(self.wall_b_buffer, self.wall_t_buffer))

        visable_sprites_camera = []

        #time_ = time.time()
        for sprite in visable_sprites_wm:
            new_surf, new_rect = self.convert_wm_sprite(sprite)
            visable_sprites_camera.append(Empty_sprite(new_surf, new_rect))
        #print(f"time to convert sprites {round(time.time() - time_, 2)}")
        
        if self.show_lines:
            lines = Empty_sprite(pygame.Surface((WIDTH,HEIGHT)), pygame.Rect(0,0,WIDTH,HEIGHT))
            lines.surf.set_colorkey((0,0,0))

            for hor_line_pos in range(math.floor(self.wall_b), math.ceil(self.wall_t)):
                if hor_line_pos%CAMERA_LINES_GRID_SIZE[0] == 0:
                    pos_on_camera = self.wm_scale*(self.wall_t - hor_line_pos)
                    pygame.draw.line(lines.surf, CAMERA_LINE_COLOR, (0, pos_on_camera), (WIDTH, pos_on_camera), 1)

            for vert_line_pos in range(math.floor(self.wall_l), math.ceil(self.wall_r)):
                if vert_line_pos%CAMERA_LINES_GRID_SIZE[1] == 0:
                    pos_on_camera = self.wm_scale*(-self.wall_l + vert_line_pos)
                    pygame.draw.line(lines.surf, CAMERA_LINE_COLOR, (pos_on_camera, 0), (pos_on_camera, HEIGHT), CAMERA_LINE_WIDTH)
                
            visable_sprites_camera.append(lines)
        
        if self.is_dark:
            if self.dark_screen_opacity != self.dark_screen_night_opacity:
                self.dark_screen_opacity+=TIME_CHANGE_SPEED
        else:
            if self.dark_screen_opacity != 0:
                self.dark_screen_opacity-=TIME_CHANGE_SPEED
        
        self.night_screen_surf.fill((0,0,0))
        self.night_screen_surf.set_alpha(self.dark_screen_opacity)

        visable_sprites_camera.append(Empty_sprite(self.night_screen_surf, self.night_screen_rect))

        return visable_sprites_camera # sprite class containing all the surfaces and their postion the camera

        
    def convert_wm_sprite(self, sprite):
        new_surf = self.convert_wm_surf(sprite.surf)
        new_rect = self.convert_wm_rect(sprite.rect)
        return [new_surf, new_rect]

    def convert_wm_surf(self, surf):
        surf_size = surf.get_size()
        return pygame.transform.scale(surf, (surf_size[0]* self.wm_scale, surf_size[1]* self.wm_scale))

    def convert_wm_rect(self, rect):
        return pygame.Rect((self.wm_scale*(-self.wall_l + rect.left), self.wm_scale*(self.wall_t - rect.top)), (rect.w*self.wm_scale, rect.h*self.wm_scale))

    def convert_screenpos_to_wm(self, pos):
        pos = (pos[0]/self.wm_scale, -pos[1]/self.wm_scale)
        return (pos[0]+self.wall_l, pos[1]+self.wall_t)

camera = Camera()
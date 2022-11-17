import pygame

class Worldmap:
    def __init__(self):
        self.worldmap_sprites =  pygame.sprite.Group()
    
    def add_sprite(self, sprite):
        self.worldmap_sprites.add(sprite)
            
    def get_object_at_tile_range(self, xmin_max, ymin_max):
        xmin = xmin_max[0]
        xmax = xmin_max[1]

        ymin = ymin_max[0]
        ymax = ymin_max[1]

        sprites_in_range = []
        for sprite in self.worldmap_sprites:
            pos = sprite.rect.center
            if not(pos[0] > xmin and pos[0] < xmax): # skip it if its out of x range
                continue
            if not(pos[1] > ymin and pos[1] < ymax): # skip it if its out of y range
                continue
            sprites_in_range.append(sprite)

        return sprites_in_range

worldmap = Worldmap()
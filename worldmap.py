import pygame, noise

CHUNK_SIZE = (1000,1000)
NOISE_DETAIL = 100 # size of noise rects

#print(help(noise))

class Ground_chunk(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        size = (CHUNK_SIZE[0]+NOISE_DETAIL*2, CHUNK_SIZE[1]+NOISE_DETAIL*2)
        self.surf = pygame.Surface(size)
        self.rect = pygame.Rect((0,0), size)
        self.rect.topleft = (pos[0]-NOISE_DETAIL, pos[1]+NOISE_DETAIL)

        worldmap.add_sprite(self)
        self.generate_noise()

    def generate_noise(self):
        for noise_x in range(-NOISE_DETAIL, CHUNK_SIZE[0]+NOISE_DETAIL*2, NOISE_DETAIL):
            for noise_y in range(-NOISE_DETAIL, CHUNK_SIZE[1]+NOISE_DETAIL*2, NOISE_DETAIL):
                
                noise_color = (noise.pnoise2(noise_x/CHUNK_SIZE[0]+self.rect.left/CHUNK_SIZE[0], noise_y/CHUNK_SIZE[1]-self.rect.top/CHUNK_SIZE[1])+1)*255/2
                pygame.draw.rect(self.surf, (noise_color,0,0), pygame.Rect(noise_x, noise_y, NOISE_DETAIL, NOISE_DETAIL))

class Worldmap:
    def __init__(self):
        self.worldmap_sprites =  pygame.sprite.Group()
    
    def add_sprite(self, sprite):
        self.worldmap_sprites.add(sprite)
        print(len(self.worldmap_sprites))
            
    def get_objects_in_tile_range(self, xmin_max, ymin_max):
        xmin = xmin_max[0]
        xmax = xmin_max[1]

        ymin = ymin_max[0]
        ymax = ymin_max[1]

        sprites_in_range = []
        for sprite in self.worldmap_sprites:
            pos = (sprite.rect.centerx, sprite.rect.centery-sprite.rect.h) # idk why, this is just what works
            if not(pos[0] > xmin and pos[0] < xmax): # skip it if its out of x range
                continue
            if not(pos[1] > ymin and pos[1] < ymax): # skip it if its out of y range
                #print(ymin, pos[1], ymax)
                continue
            sprites_in_range.append(sprite)

        return sprites_in_range

    def get_object_in_rect(self, camera_rect):
        sprites_in_range = []

        for sprite in self.worldmap_sprites:
            if pygame.Rect.colliderect(camera_rect, sprite.rect):
                sprites_in_range.append(sprite)

        return sprites_in_range

    def get_all_sprites(self):
        return self.worldmap_sprites

worldmap = Worldmap()

#Ground_chunk((0,0))
if True:
    size = 3
    for x in range(-size,size):
        for y in range(-size,size):
            Ground_chunk((x*CHUNK_SIZE[0],y*CHUNK_SIZE[1]))
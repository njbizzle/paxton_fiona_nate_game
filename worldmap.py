import pygame, noise, math, random
#https://stackoverflow.com/questions/55192764/how-to-randomize-the-seed-of-the-noise-library

CHUNK_SIZE = (500,500)
NOISE_DETAIL = 100 # size of noise rects

NOISE_SCALE = 5000

def get_noise(x,y):
    return noise.pnoise2(x/NOISE_SCALE, y/NOISE_SCALE, octaves=4, persistence=0.5, lacunarity=2)

class Chunk(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        size = (CHUNK_SIZE[0]+NOISE_DETAIL*2, CHUNK_SIZE[1]+NOISE_DETAIL*2)
        self.surf = pygame.Surface(size)
        self.pos = pos

        self.rect = pygame.Rect((0,0), size)
        self.rect.topleft = (pos[0]-NOISE_DETAIL, pos[1]+NOISE_DETAIL)

        worldmap.add_sprite(self, is_ground_tile=True)
        self.generate()

    def delete_self(self):
        worldmap.remove_sprite(self, is_ground_tile=True)

    def generate(self):
        #self.surf.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

        for noise_x in range(-NOISE_DETAIL, CHUNK_SIZE[0]+NOISE_DETAIL*2, NOISE_DETAIL):
            for noise_y in range(-NOISE_DETAIL, CHUNK_SIZE[1]+NOISE_DETAIL*2, NOISE_DETAIL):
                noise_color = (get_noise(noise_x+self.rect.left, noise_y-self.rect.top)+1)*255/2
                pygame.draw.rect(self.surf, (noise_color, noise_color, noise_color), pygame.Rect(noise_x, noise_y, NOISE_DETAIL, NOISE_DETAIL))

class Worldmap:
    def __init__(self):
        self.worldmap_sprites =  pygame.sprite.Group()
        self.ground_tiles = {}
    
    def add_sprite(self, sprite, is_ground_tile=False):
        if is_ground_tile:
            self.ground_tiles[(sprite.pos)] = sprite
            return

        self.worldmap_sprites.add(sprite)

    def remove_sprite(self, sprite, is_ground_tile=False):
        if is_ground_tile:
            del self.ground_tiles[(sprite.pos)]
            return

        self.worldmap_sprites.remove(sprite)

    
    def get_ground_tile(self, pos):
        try:
            return self.ground_tiles[pos]
        except:
            return Chunk(pos)

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
                continue
            sprites_in_range.append(sprite)
        
        chunk_l = CHUNK_SIZE[0] * math.floor(xmin / CHUNK_SIZE[0])
        chunk_r = CHUNK_SIZE[0] * math.ceil(xmax / CHUNK_SIZE[0])

        chunk_b = CHUNK_SIZE[1] * math.floor(ymin / CHUNK_SIZE[0])
        chunk_t = CHUNK_SIZE[1] * math.ceil(ymax / CHUNK_SIZE[0])

        chunks_needed = []
        for chunk_x in range(chunk_l, chunk_r, CHUNK_SIZE[0]):
            for chunk_y in range(chunk_b, chunk_t, CHUNK_SIZE[0]):
                sprites_in_range.append(self.get_ground_tile((chunk_x, chunk_y+CHUNK_SIZE[1])))
        
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
import pygame, noise, math, random
from perlin_noise import PerlinNoise
CHUNK_SIZE = (500, 500)
NOISE_DETAIL = 100 # size of noise rects

NOISE_SCALE = 5000

def area_round(size, coords, radius=[0,0], area=True):
    if not(area):
        coords = [coords[0],coords[0],coords[1],coords[1]]

    x_min = math.floor((coords[0] - radius[0])/size[0]) * size[0]
    x_max = math.ceil((coords[1] + radius[0])/size[0]) * size[0]

    y_min = math.floor((coords[2] - radius[1])/size[1]) * size[1]
    y_max = math.ceil((coords[3] + radius[1])/size[1]) * size[1]

    return (x_min, x_max, y_min, y_max)
                    
class Worldmap:
    def __init__(self):
        self.reset()
    
    def reset(self):        
        self.seed = random.randint(0,999999999)

        self.height_map = Noise_map(scale=10000, octaves=3, persistence=0.5, lacunarity=2, seed=self.seed)
        self.tree_probability_map = Noise_map(scale=10000, octaves=1, persistence=0.5, lacunarity=2, seed=self.seed)

        self.worldmap_sprites =  pygame.sprite.Group()
        self.ground_tiles = {}
        self.noise_squares = {}

        self.active_collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

    def add_sprite(self, sprite, is_ground_tile=False):
        if is_ground_tile:
            self.ground_tiles[(sprite.pos)] = sprite
            return
        
        try:
            if sprite.is_enemy:
                self.enemy_sprites.add(sprite)
        except:
            pass
    
        self.worldmap_sprites.add(sprite)

    def remove_sprite(self, sprite, is_ground_tile=False):
        if is_ground_tile:
            del self.ground_tiles[(sprite.pos)]
            return

        try:
            if sprite.is_enemy:
                self.enemy_sprites.remove(sprite)
        except:
            pass

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

        chunk_l, chunk_r, chunk_b, chunk_t = area_round(CHUNK_SIZE, (xmin, xmax, ymin, ymax))

        for chunk_x in range(chunk_l, chunk_r, CHUNK_SIZE[0]):
            for chunk_y in range(chunk_b, chunk_t, CHUNK_SIZE[1]):
                chunk = self.get_ground_tile((chunk_x, chunk_y+CHUNK_SIZE[1]))
                sprites_in_range.append(chunk)
        
        self.active_collision_sprites = pygame.sprite.Group()

        for sprite in self.worldmap_sprites:
            pos = (sprite.rect.centerx, sprite.rect.centery-sprite.rect.h) # idk why, this is just what works
            if not(pos[0] > xmin and pos[0] < xmax) or not(pos[1] > ymin and pos[1] < ymax): # skip it if its out of x or y range
                try:
                    sprite.delete_off_screen = True
                    sprite.delete()
                    self.remove_sprite(sprite)
                except:
                    pass
                continue
            sprites_in_range.append(sprite)
            
            try:
                if sprite.collision:
                    self.active_collision_sprites.add(sprite)
            except:
                pass

        
        return sprites_in_range

    def get_all_sprites(self):
        return self.worldmap_sprites

    def get_chunks_at_pos(self, coords):

        cx_min, cx_max, cy_min, cy_max = area_round(CHUNK_SIZE, coords, [CHUNK_SIZE[0]/2, CHUNK_SIZE[1]/2], area=False)

        chunks_to_return = []

        for x in range(cx_min, cx_max, CHUNK_SIZE[0]):
            for y in range(cy_min, cy_max, CHUNK_SIZE[1]):
                chunk = self.get_ground_tile((x, y))
                chunks_to_return.append(chunk)

        return chunks_to_return

    def get_squares_at_coords(self, coords, radius=0):
        sx_min, sx_max, sy_min, sy_max = area_round([NOISE_DETAIL, NOISE_DETAIL], coords, [radius, radius], area=False)
        squares_to_return = []

        for x in range(sx_min, sx_max+NOISE_DETAIL, NOISE_DETAIL):
            for y in range(sy_min, sy_max+NOISE_DETAIL, NOISE_DETAIL):
                try:
                    squares_to_return.append(self.noise_squares[(x,y)])
                except:
                    pass
        return squares_to_return

class Noise_map:
    def __init__(self, scale=5000, octaves=1, persistence=0.5, lacunarity=2, seed=0):

        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

        self.noise = PerlinNoise(octaves=self.octaves, seed=seed)

    def get_noise(self, coords):
        coords = [coords[0], coords[1]]
        #return noise.pnoise2(coords[0]/self.scale, coords[1]/self.scale, octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity)
        return self.noise([coords[0]/self.scale, coords[1]/self.scale])

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
        for noise_x in range(-NOISE_DETAIL, CHUNK_SIZE[0]+NOISE_DETAIL*2, NOISE_DETAIL):
            for noise_y in range(-NOISE_DETAIL, CHUNK_SIZE[1]+NOISE_DETAIL*2, NOISE_DETAIL):

                coords = noise_x+self.rect.left, -noise_y+self.rect.top

                height_noise = worldmap.height_map.get_noise(coords)
                #tree_probability = worldmap.tree_probability_map.get_noise(coords)
                tree_probability = 0

                height_noise_color = (height_noise+1)*255/2

                square_color = (0, height_noise_color, 0)
                sqaure_rect = pygame.Rect(noise_x, noise_y, NOISE_DETAIL, NOISE_DETAIL)

                if height_noise < -0.22:
                    square_color = (255, 200, 100) # sand
                    tree_probability = 0
                    worldmap.noise_squares[coords] = "sand"

                if height_noise < -0.25:
                    square_color = (0, 100, 200) # water
                    worldmap.noise_squares[coords] = "water"
                else:
                    worldmap.noise_squares[coords] = "none"

                pygame.draw.rect(self.surf, square_color, sqaure_rect)

                #rand = random.randint(0,200)/100
                rand = 100
                if rand < (height_noise+tree_probability)/8:
                    try:
                        Tree(coords)
                    except:
                        from resources import Tree
                        Tree(coords)

worldmap = Worldmap()

import pygame, math
from worldmap import worldmap
from weapon import Laser

DEFAULT_ACCELETATION = 10
DEFAULT_FRICTION = 0.7
DEFAULT_MAX_SPEED = 10

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.size = (100,100)

        self.surf = pygame.Surface(self.size)
        self.surf.fill((255, 211, 67))
        self.rect = self.surf.get_rect()

        self.vel = (0,0)

        self.acceleration = DEFAULT_ACCELETATION
        self.friction = DEFAULT_FRICTION
        self.max_speed = DEFAULT_MAX_SPEED

        self.lasers = []

        worldmap.add_sprite(self)

    def get_pos(self):
        return self.rect.topleft

    def update(self, controls): # controls: up down left right
        up, down, left, right, shoot = controls # bools to see if key pressed

        if "water" in worldmap.get_squares_at_coords((self.get_pos()), 50):
            self.max_speed = 4
        else:
            self.max_speed = DEFAULT_MAX_SPEED

        if up:
            self.vel = add_vec(self.vel, (0, self.acceleration)) 
        if down:
            self.vel = add_vec(self.vel, (0, -self.acceleration))
        if right:
            self.vel = add_vec(self.vel, (self.acceleration, 0))
        if left:
            self.vel = add_vec(self.vel, (-self.acceleration, 0))
        if shoot:
            self.lasers.append(Laser(self.get_pos(), pygame.mouse.get_pos())) # when space is clicked, laser shoots

        for laser in self.lasers:
            laser.update()

        if pygame.sprite.spritecollide(self, worldmap.active_collision_sprites, False):
            #print("stuff is colliding but i dont know what do do about it")
            pass

        if pygame.sprite.spritecollide(self, worldmap.active_enemy_sprites, False):
            worldmap.reset()

            self.rect = self.surf.get_rect()

            self.vel = (0,0)

            self.acceleration = DEFAULT_ACCELETATION
            self.friction = DEFAULT_FRICTION
            self.max_speed = DEFAULT_MAX_SPEED

            worldmap.add_sprite(self)
        
        self.vel = max(-self.max_speed, min(self.vel[0]*self.friction, self.max_speed)), max(-self.max_speed, min(self.vel[1]*self.friction, self.max_speed))
        self.rect = pygame.Rect(add_vec(self.get_pos(), self.vel), self.size)

    def collide(self):
        self.vel = (0,0)


player = Player()
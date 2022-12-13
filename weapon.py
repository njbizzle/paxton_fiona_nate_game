import pygame, math, random
from worldmap import worldmap

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

class Laser(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos, group, damage=10, bloom=0, size=30, speed=100):
        super().__init__()

        self.delete_off_screen = True

        self.surf = pygame.Surface((size,size))
        self.surf.fill((255,0,0))

        self.rect = self.surf.get_rect(topleft=player_pos)

        self.mouse_x, self.mouse_y = mouse_pos
        self.speed = speed

        self.damage = damage

        # from u/no_Im_perfectly_sane
        self.angle = math.atan2(mouse_pos[1]-player_pos[1], mouse_pos[0]-player_pos[0]) + random.randint(1,1000)/1000*bloom
        self.move_vec = (math.cos(self.angle)*self.speed, math.sin(self.angle)*self.speed)

        self.group = group
        self.group.add(self)
        worldmap.add_sprite(self)

    def update(self):
        self.rect = pygame.Rect(add_vec(self.move_vec, self.rect), self.rect.size)
    
    def delete(self):
        self.group.remove(self)
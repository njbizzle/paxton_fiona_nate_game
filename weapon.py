import pygame 
from worldmap import worldmap

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])
#Creates the shape and speed of the Laser + color
class Laser:
    def __init__(self, player_pos, mouse_pos):
        self.surf = pygame.Surface((5,40))
        self.surf.fill((255,255,0))

        self.rect = self.surf.get_rect(topleft=player_pos)

        self.slope = player_pos[0]-mouse_pos[0]/player_pos[1]-mouse_pos[1]
        self.speed = 1

        worldmap.add_sprite(self)

    def update(self):
        self.rect = pygame.Rect(add_vec(self.rect.topleft, (self.speed, self.speed*self.slope)))

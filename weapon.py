import pygame 
from worldmap import worldmap

#Creates the shape and speed of the Laser + color
class Laser:
    def __init__(self, loc):
        self.image = pygame.Surface((5,40)).convert()
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect(center=loc)
        self.speed = 5
          
    def update(self):
        self.rect.y -= self.speed

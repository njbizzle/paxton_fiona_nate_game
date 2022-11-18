import pygame
from worldmap import worldmap

class Test_rect(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        super().__init__()

        self.rect = rect
        
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill(color)

        worldmap.add_sprite(self)
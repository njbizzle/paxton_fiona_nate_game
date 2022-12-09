import pygame
from worldmap import worldmap

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.surf = pygame.Surface((100,100))
        self.surf.fill((100,100,50))

        self.rect = self.surf.get_rect(topleft=pos)

        self.collision = True

        worldmap.add_sprite(self)

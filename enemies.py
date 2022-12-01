import pygame
from worldmap import worldmap

class Test_enemy(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        print(f"enemy spawn at {rect.center}")

        self.rect = rect
        
        self.surf = pygame.Surface(self.rect.size)
        self.surf.fill((0,0,0))

        worldmap.add_sprite(self)
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, surf, rect):
        super().__init__()
        self.surf = surf
        self.rect = rect
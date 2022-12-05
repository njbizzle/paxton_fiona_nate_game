import pygame
from worldmap import worldmap

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        self.size = (100,100)

        self.surf = pygame.Surface(self.size)
        self.surf.fill((255, 211, 67))
        self.rect = self.surf.get_rect()

        self.speed = 10

        worldmap.add_sprite(self)

    def get_pos(self):
        return self.rect.topleft

    def update(self, controls): # controls: up down left right
        up, down, left, right = controls # bools to see if key pressed

        move_vec = (0,0)

        if up:
            move_vec = add_vec(move_vec, (0, self.speed)) 
        if down:
            move_vec = add_vec(move_vec, (0, -self.speed))
        if right:
            move_vec = add_vec(move_vec, (self.speed, 0))
        if left:
            move_vec = add_vec(move_vec, (-self.speed, 0))

        self.rect = pygame.Rect(add_vec(self.get_pos(), move_vec), self.size)


player = Player()
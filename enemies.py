import pygame, math
from worldmap import worldmap
from player import player

class Test_enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed=10, image_path=None, enemy_group=None):
        super().__init__()

        self.pos = pos
        self.speed = speed

        self.is_enemy = True

        if image_path:
            self.surf = pygame.image.load(image_path)
        else:
            self.surf = pygame.Surface((100,100))
        self.rect = self.surf.get_rect(center=self.pos)

        self.agro = (0,0)
    
        worldmap.add_sprite(self)

        self.enemy_group = enemy_group
        if self.enemy_group:
            self.enemy_group.add(self)

    def set_agro(self, pos):
        self.agro = pos
    
    def update(self):
        self.set_agro(player.get_pos())
        pos_x, pos_y = (self.pos)
        agro_x, agro_y = (self.agro)

        x_dif = agro_x-pos_x
        y_dif = agro_y-pos_y

        a = math.sqrt(self.speed**2/(x_dif**2 + y_dif**2))
        update_pos = (a*x_dif+pos_x, a*y_dif+pos_y)

        self.pos = update_pos
        self.rect = self.surf.get_rect(center=self.pos)
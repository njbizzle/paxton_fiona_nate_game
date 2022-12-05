import pygame, math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, image_path, enemy_group=None):
        super().__init__()

        self.pos = pos
        self.speed = speed

        self.surf = pygame.image.load(image_path)
        self.rect = self.surf.get_rect(pos)

        self.agro = (0,0)
    
        self.enemy_group = enemy_group
        if self.enemy_group:
            self.enemy_group.add(self)

    def set_agro(self, pos):
        self.agro = pos
    
    def update(self):
        print("test enemy")
        pos_x, pos_y = (self.pos)
        agro_x, agro_y = (self.agro)

        x_dif = agro_x-pos_x
        y_dif = agro_y-pos_y

        step = 2
        a = math.sqrt(step**2/(x_dif**2 + y_dif**2))
        update_pos = (a*x_dif+pos_x, a*y_dif+pos_y)
        self.pos = update_pos
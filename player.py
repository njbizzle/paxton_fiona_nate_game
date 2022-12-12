import pygame, time, game_screen
from worldmap import worldmap
from weapon import Laser
from camera import camera

DEFAULT_ACCELETATION = 10
DEFAULT_FRICTION = 0.7
DEFAULT_MAX_SPEED = 10
SPRINT_MAX_SPEED = 20

STAMINA_MAX = 100
HEALTH_MAX = 100
STAMINA_LOSS = 2
STAMINA_REGEN = 1

MAX_AMMO = 10
RELOAD_TIME = 0.1

FIRE_RATE = 0.2

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.size = (100,100)
        self.surf = pygame.Surface(self.size)
        self.rect = self.surf.get_rect()

        self.lasers = pygame.sprite.Group()
        self.ammo = MAX_AMMO
        self.reloading = False
        self.reloading_done_time = 0

        self.fire_rate = FIRE_RATE
        self.last_fired = 0

        self.reset()

    def get_pos(self):
        return self.rect.topleft

    def update(self, controls): # controls: up down left right
        up, down, left, right, shoot, sprint, reload = controls # bools to see if key pressed

        if "water" in worldmap.get_squares_at_coords((self.get_pos()), 50):
            self.max_speed = 4
        else:
            if sprint:
                if self.stamina > 0:
                    self.max_speed = SPRINT_MAX_SPEED
                    self.stamina -=1

                elif self.stamina == 0:
                    self.stamina -=10
                    self.max_speed = DEFAULT_MAX_SPEED
            else:
                if self.stamina < STAMINA_MAX:
                    self.stamina +=1
                self.max_speed = DEFAULT_MAX_SPEED

        if up:
            self.vel = add_vec(self.vel, (0, self.acceleration)) 
        if down:
            self.vel = add_vec(self.vel, (0, -self.acceleration))
        if right:
            self.vel = add_vec(self.vel, (self.acceleration, 0))
        if left:
            self.vel = add_vec(self.vel, (-self.acceleration, 0))

        if shoot and not(self.reloading) and self.ammo > 0:
            time_ = time.time()
            if time_-self.last_fired > self.fire_rate:
                self.ammo -= 1
                self.last_fired = time_
                Laser(self.get_pos(), camera.convert_screenpos_to_wm(pygame.mouse.get_pos()), self.lasers) # when space is clicked, laser shoots

        if reload:
            self.reloading = True

        if self.reloading and time.time() > self.reloading_done_time:
            self.ammo += 1
            if self.ammo >= MAX_AMMO:
                self.reloading = False
            else:
                self.reloading_done_time = time.time()+RELOAD_TIME
            
        for laser in self.lasers:
            laser.update()

        if pygame.sprite.spritecollide(self, worldmap.active_collision_sprites, False):
            pass

        if pygame.sprite.spritecollide(self, worldmap.enemy_sprites, False):
            self.health -=3
            self.color = 255
        self.color -= 1

        if self.color <= 0:
            self.color = 0
        self.surf.fill((self.color, 255, 255))

        if self.health <= 0:
            self.die()
        
        self.vel = max(-self.max_speed, min(self.vel[0]*self.friction, self.max_speed)), max(-self.max_speed, min(self.vel[1]*self.friction, self.max_speed))
        self.rect = pygame.Rect(add_vec(self.get_pos(), self.vel), self.size)

    def die(self):
        game_screen.game_screen_load()
    
    def reset(self):
        self.vel = (0,0)

        self.acceleration = DEFAULT_ACCELETATION
        self.friction = DEFAULT_FRICTION
        self.max_speed = DEFAULT_MAX_SPEED

        self.health = HEALTH_MAX
        self.stamina = STAMINA_MAX
        self.color = 0

        worldmap.add_sprite(self)

player = Player()
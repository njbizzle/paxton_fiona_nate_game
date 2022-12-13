import pygame, time, game_screen, random
from worldmap import worldmap
from weapon import Laser
from camera import camera

DEFAULT_ACCELETATION = 10
DEFAULT_FRICTION = 0.9
DEFAULT_MAX_SPEED = 15
SPRINT_MAX_SPEED = 25

STAMINA_MAX = 100
HEALTH_MAX = 100
STAMINA_LOSS = 2
STAMINA_REGEN = 1

LAUNCH_DIST = 100
IFRAMES_TIME = 1.5

default = {"ammo":15, "reload_time":0.1, "bullet_count":1, "bloom":0, "size":30, "damage":10, "speed":100, "fire_rate":0.2} 
god_weapon = {"ammo":100, "reload_time":0.01, "bullet_count":10, "bloom":0.5, "size":50, "damage":1, "speed":50, "fire_rate":0.01} 

def swap_to_god_weapon():
    if player.weapon == default:
        player.weapon = god_weapon
        player.ammo = god_weapon["ammo"]

    elif player.weapon == god_weapon:
        player.weapon = default

def add_vec(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])

def min_max(num, max_, min_=None):
    if not(min_):
        min_ = -max_
    return min(max_, max(num, min_))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.size = (100,100)
        self.surf = pygame.Surface(self.size)
        self.rect = self.surf.get_rect()

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

        accel_vec = (0,0)

        if up:
            accel_vec = add_vec(accel_vec, (0, self.acceleration))
        if down:
            accel_vec = add_vec(accel_vec, (0, -self.acceleration))
        if right:
            accel_vec = add_vec(accel_vec, (self.acceleration, 0))
        if left:
            accel_vec = add_vec(accel_vec, (-self.acceleration, 0))
        
        max_accel_x = self.max_speed-self.vel[0]
        min_accel_x = -self.max_speed-self.vel[0]

        max_accel_y = min_max(self.max_speed-self.vel[1], self.max_speed)
        min_accel_y = min_max(-self.max_speed-self.vel[1], self.max_speed)
        
        accel_x = min_max(accel_vec[0], max_accel_x, min_accel_x)
        accel_y = min_max(accel_vec[1], max_accel_y, min_accel_y)

        self.vel = add_vec(self.vel, (accel_x, accel_y))

        self.vel = (self.vel[0]*self.friction, self.vel[1]*self.friction)

        if self.ammo > self.weapon["ammo"]:
            self.ammo = self.weapon["ammo"]

        if shoot and not(self.reloading) and self.ammo > 0:
            time_ = time.time()
            if time_-self.last_fired > self.weapon["fire_rate"]:
                self.ammo -= 1
                self.last_fired = time_
                for i in range(0, self.weapon["bullet_count"]):
                    Laser(self.get_pos(), camera.convert_screenpos_to_wm(pygame.mouse.get_pos()), self.lasers,
                    damage=self.weapon["damage"], bloom=self.weapon["bloom"], size=self.weapon["size"], speed=self.weapon["speed"]) # when space is clicked, laser shoots

        if reload:
            self.reloading = True

        if self.reloading and time.time() > self.reloading_done_time:
            if self.ammo >= self.weapon["ammo"]:
                self.reloading = False
            else:
                extra_time = 0
                if self.ammo + 1 == self.weapon["ammo"]:
                    extra_time = 1
                self.reloading_done_time = time.time() + self.weapon["reload_time"] + extra_time
                self.ammo += 1
            
        for laser in self.lasers:
            laser.update()

        if pygame.sprite.spritecollide(self, worldmap.active_collision_sprites, False):
            pass

        if pygame.sprite.spritecollide(self, worldmap.enemy_sprites, False) and not(self.iframes):
            self.vel = (random.randint(-LAUNCH_DIST, LAUNCH_DIST), random.randint(-LAUNCH_DIST, LAUNCH_DIST))
            self.health -= 25

            self.iframes_time = time.time()+IFRAMES_TIME
            self.iframes = True

        if self.iframes:
            self.color = 255
            if time.time() > self.iframes_time:
                self.iframes = False

        self.color -= 5

        if self.color <= 0:
            self.color = 0
        self.surf.fill((self.color, 255, 255))

        if self.health <= 0:
            self.die()

        self.rect = pygame.Rect(add_vec(self.get_pos(), self.vel), self.size)

    def die(self):
        game_screen.game_screen_load(die=True)
    
    def reset(self):
        self.lasers = pygame.sprite.Group()

        self.weapon = default

        self.ammo = self.weapon["ammo"]
        self.reloading = False
        self.reloading_done_time = 0

        self.last_fired = 0

        self.vel = (0,0)

        self.acceleration = DEFAULT_ACCELETATION
        self.friction = DEFAULT_FRICTION
        self.max_speed = DEFAULT_MAX_SPEED

        self.health = HEALTH_MAX
        self.stamina = STAMINA_MAX
        self.color = 0

        self.iframes = False
        self.iframes_time = 0

        worldmap.add_sprite(self)

player = Player()

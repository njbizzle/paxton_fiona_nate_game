import time, random, math, pygame
from enemies import Test_enemy
from camera import camera
from player import player
from worldmap import worldmap
#from main import add_thread, remove_thread

DAY_TIME = 3 #seconds
NIGHT_TIME = 30
day_night = "day"

ENEMY_SPAWN_CIRCLE = 5000 #radius
enemy_wave = 0
enemies = pygame.sprite.Group()

swap_time = time.time()+DAY_TIME

def get_wave():
    global enemy_wave
    return enemy_wave

def reset():
    global day_night, enemy_wave, enemies, swap_time
    swap_time = time.time()
    enemy_wave = 0
    enemies = pygame.sprite.Group()

def game_timer():
    global enemy_wave
    #print(len(worldmap.enemy_sprites))
    if len(worldmap.enemy_sprites) == 0:
        enemy_wave += 1

        wave_enemies = []
        for i in range(0, enemy_wave): # temp
            wave_enemies.append("test_enemy")

        spawn_enemies(wave_enemies)

def spawn_enemies(wave):
    global enemies
    random_precision = 1000

    for enemy in wave:
        rand = random.randint(0, 2 * random_precision)/random_precision - 1

        player_x, player_y = player.get_pos()

        x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi) + player_x
        y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi) + player_y

        if enemy == "test_enemy":
            enemies.add(Test_enemy((x, y)))

'''
def game_timer():
    global day_night, swap_time
    for enemy in enemies:
        enemy.update()
    
    time_ = time.time()

    if time_ > swap_time:
        if day_night == "night":
            print("now day")
            day_night = "day"
            swap_time = time_ + DAY_TIME

            day_start()
            camera.set_night(False)

        elif day_night == "day":
            print("now night")
            day_night = "night"
            swap_time = time_ + NIGHT_TIME

            night_start()
            camera.set_night(True)

def day_start():
    pass

def night_start():
    global enemy_wave
    enemy_wave += 1

    wave_enemies = []
    for i in range(0, enemy_wave): # temp
        wave_enemies.append("enemy")

    spawn_enemies(wave_enemies)

def spawn_enemies(wave):
    global enemies
    random_precision = 1000

    for enemy in wave:
        rand = random.randint(0, 2 * random_precision)/random_precision - 1

        player_x, player_y = player.get_pos()

        x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi) + player_x
        y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi) + player_y

        enemies.add(Test_enemy((x, y)))


#    wait_times = []
#    for i in range(len(wave)):
#        wait_times.append(time.time() + NIGHT_TIME / len(wave)*i)
#
#    current_enemy = 0
#    while True:
#        if current_enemy >= len(wave):
#            return
#
#        elif time.time() > wait_times[current_enemy]:
#            rand = random.randint(0, 2 * random_precision)/random_precision - 1
#
#            x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi)
#            y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi)
#
#            enemies.add(Test_enemy((x, y)))
#            current_enemy += 1

'''
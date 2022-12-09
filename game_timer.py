import time, random, math, pygame, threading
from enemies import Test_enemy
from camera import camera
from player import player
#from main import add_thread, remove_thread

DAY_TIME = 20 #seconds
NIGHT_TIME = 20
DAY_CHANGE_TIME = 3
day_night = "day"

ENEMY_SPAWN_CIRCLE = 5000 #radius
enemy_wave = 0
enemies = pygame.sprite.Group()

def start_game_timer():
    global day_night
    
    while True:
        if day_night == "day":
            print("now day")
            day_start()

            time.sleep(DAY_TIME-DAY_CHANGE_TIME)
            camera.set_night(True)
            time.sleep(DAY_CHANGE_TIME)

            day_night = "night"

        elif day_night == "night":
            print("now night")
            night_start()

            time.sleep(NIGHT_TIME-DAY_CHANGE_TIME)
            camera.set_night(False)
            time.sleep(DAY_CHANGE_TIME)

            day_night = "day"

def day_start():
    pass

def night_start():
    global enemy_wave
    enemy_wave += 1

    wave_enemies = []
    for i in range(0, enemy_wave): # temp
        wave_enemies.append("enemy")

    spawn_enemies_thread = threading.Thread(target=spawn_enemies, args=(wave_enemies,))
    spawn_enemies_thread.start()

def spawn_enemies(wave):
    global enemies
    random_precision = 1000

    for enemy in wave:
        rand = random.randint(0, 2 * random_precision)/random_precision - 1

        player_x, player_y = player.get_pos()

        x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi) + player_x
        y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi) + player_y

        enemies.add(Test_enemy((x, y)))

'''
    wait_times = []
    for i in range(len(wave)):
        wait_times.append(time.time() + NIGHT_TIME / len(wave)*i)

    current_enemy = 0
    while True:
        if current_enemy >= len(wave):
            return

        elif time.time() > wait_times[current_enemy]:
            rand = random.randint(0, 2 * random_precision)/random_precision - 1

            x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi)
            y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi)

            enemies.add(Test_enemy((x, y)))
            current_enemy += 1
'''
def update_enemies():
    global enemies
    for enemy in enemies:
        enemy.update()

def get_enemies():
    global enemies
    return enemies
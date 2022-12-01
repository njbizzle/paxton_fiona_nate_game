import time, random, math, pygame, threading
from enemies import Test_enemy
#from main import add_thread, remove_thread

DAY_TIME = 10 #seconds
NIGHT_TIME = 10 #seconds
day_night = "day"

ENEMY_SPAWN_CIRCLE = 10000 #radius
enemy_wave = 0

def start_game_timer():
    global day_night
    
    while True:
        if day_night == "day":
            print("now day")
            day_start()
            time.sleep(DAY_TIME)
            day_night = "night"

        elif day_night == "night":
            print("now night")
            night_start()
            time.sleep(NIGHT_TIME)
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
    wait_times = []
    random_precision = 10000

    for i in range(len(wave)):
        wait_times.append(time.time() + NIGHT_TIME / len(wave)*i)

    print(f"wait_times = {wait_times}")
    current_enemy = 0
    while True:
        if current_enemy >= len(wave):
            return

        elif time.time() > wait_times[current_enemy]:
            rand = random.randint(0, 2 * random_precision)/random_precision - 1

            x = ENEMY_SPAWN_CIRCLE * math.cos(rand * 2 * math.pi)
            y = ENEMY_SPAWN_CIRCLE * math.sin(rand * 2 * math.pi)

            Test_enemy(pygame.Rect(x, y, 100, 100))
            current_enemy += 1
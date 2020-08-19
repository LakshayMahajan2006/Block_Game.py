# Block_Game.py

import pygame
import sys
import random

#Initalize pygame window
pygame.init()

#Setting height, width
WIDTH = 1000
HEIGHT = 700  

#Some colours and background colour.
GRAY = (0,0,255)
CYAN = (0,255, 255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (105,105,105)

#Setting captions
pygame.display.set_caption("Game by Lakshay Mahajan")

# Player size, player pos
player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

# Enemy size, enemy pos
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

#Define set_level function
def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 8
    elif score < 60:
        SPEED = 12
    elif score < 100:
        SPEED =15
    else:
        SPEED = 25
    return SPEED

#Defining Drop_enemies function
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 7 and delay < 0.1:
        x_pos = random.randint(0, WIDTH -enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

#Defining draw_enemies function
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen,CYAN, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

#Defining update_enemy_positions function
def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score

#Defining collision_check function
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

#Defining detect_collision function
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y) and e_y < (p_y + player_size) or (p_y >= e_y and p_y < (e_y +  enemy_size)):
            return True
    return False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]
            
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOR)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)
    
    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, GRAY, (player_pos[0] ,player_pos[1] ,player_size ,player_size))

    clock.tick(30)

    pygame.display.update()

print("Score : ", score)

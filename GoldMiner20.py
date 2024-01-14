from cmath import rect
import random
import math
from re import X
import os

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN

pygame.init()

os.chdir("C:\\Users\\cindz\\Year1\\CompSci\\GoldMinerUpdated")

WIDTH = 1000
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
SAND = (100,90,50)
GOLD = (244,205,81)
STONE = (112,109,99)
START = (WIDTH / 2,150)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("GOLD MINER")
font = pygame.font. SysFont('Comfortaa', 50)

# ---------------------------
# Initialize global variables

gold = pygame.image.load("gold.png")
rock = pygame.image.load("rock.png")
claw = pygame.image.load("claw.png")
miner = pygame.image.load("miner.png")
miner = pygame.transform.scale(miner, (100,100))
claw = pygame.transform.scale(claw, (50,50))
big_gold = pygame.transform.scale(gold, (70,70))
medium_gold = pygame.transform.scale(gold, (50,50))
small_gold = pygame.transform.scale(gold, (30,30))
big_rock = pygame.transform.scale(rock,(70,70))
medium_rock = pygame.transform.scale(rock,(50,50))
small_rock = pygame.transform.scale(rock,(30,30))
#____________gold__________________
big_gold_rect = big_gold.get_rect()
big_gold_width = big_gold.get_width()
big_gold_height = big_gold.get_height()
medium_gold_rect = medium_gold.get_rect()
medium_gold_width = medium_gold.get_width()
medium_gold_height = medium_gold.get_height()
small_gold_rect = small_gold.get_rect()
small_gold_width = small_gold.get_width()
small_gold_height = small_gold.get_height()
#__________rock________________
big_rock_rect = big_rock.get_rect()
big_rock_width = big_rock.get_width()
big_rock_height = big_rock.get_height()
medium_rock_rect = medium_rock.get_rect()
medium_rock_width = medium_rock.get_width()
medium_rock_height = medium_rock.get_height()
small_rock_rect = small_rock.get_rect()
small_rock_width = small_rock.get_width()
small_rock_height = small_rock.get_height()
claw_width = claw.get_width()

# ---------------------------

big_gold_pos = [] 
medium_gold_pos = []
small_gold_pos = []
big_rock_pos = []
medium_rock_pos = []
small_rock_pos = []
collected = []

claw_pos = (475,220)
state = 1 # 1: swing, 2: fetch; 3: return to start
start_pos = (0,0)
claw_angle = 0
swing_direction = 1 
grabbed_index = -1
org_speed = 4


# a list of the position of each gold/gold rect, when claw rect collide with gold rect, gold moves

def form_big_gold():
    for big_gold in range(random.randint(1,2)):
        big_gold_pos.append((random.randint(0,WIDTH - big_gold_width),random.randint(180,HEIGHT - big_gold_height)))

def draw_big_gold():
    for pos in big_gold_pos:
        screen.blit(big_gold,pos)

def form_medium_gold():
    for medium_gold in range(random.randint(1,2)):
        medium_gold_pos.append((random.randint(0,WIDTH - medium_gold_width),random.randint(180,HEIGHT - medium_gold_height)))

def draw_medium_gold():
    for pos in medium_gold_pos:
        screen.blit(medium_gold,pos)

def form_small_gold():
    for small_gold in range(random.randint(1,2)):
        small_gold_pos.append((random.randint(0,WIDTH - small_gold_width),random.randint(180,HEIGHT - small_gold_height)))

def draw_small_gold():
    for pos in small_gold_pos:
        screen.blit(small_gold,pos)


def form_big_rock():
    for big_rock in range(random.randint(1,2)):
        big_rock_pos.append((random.randint(0,WIDTH - big_rock_width),random.randint(250,HEIGHT - big_rock_height)))

def draw_big_rock():
    for pos in big_rock_pos:
        screen.blit(big_rock,pos)

def form_medium_rock():
    for medium_rock in range(random.randint(1,2)):
        medium_rock_pos.append((random.randint(0,WIDTH - medium_rock_width),random.randint(250,HEIGHT - medium_rock_height)))

def draw_medium_rock():
    for pos in medium_rock_pos:
        screen.blit(medium_rock,pos)

def form_small_rock():
    for small_rock in range(random.randint(1,2)):
        small_rock_pos.append((random.randint(0,WIDTH - small_rock_width),random.randint(250,HEIGHT - small_rock_height)))

def draw_small_rock():
    for pos in small_rock_pos:
        screen.blit(small_rock,pos)

def draw_collected():
    for collected_item in collected:
        item = collected_item[0]
        pos = collected_item[1]
        if item == 'bg':
            screen.blit(big_gold,pos)
        elif item == 'mg':
            screen.blit(medium_gold,pos)
        elif item == 'sg':
            screen.blit(small_gold,pos)
        elif item == 'br':
            screen.blit(big_rock,pos)
        elif item == 'mr':
            screen.blit(medium_rock,pos)
        elif item == 'sr':
            screen.blit(small_rock,pos)

def get_all_rects():
    rects = []
    for pos in big_gold_pos:
        rects.append(pygame.Rect(pos[0],pos[1],big_gold_width,big_gold_height))
    for pos in medium_gold_pos:
        rects.append(pygame.Rect(pos[0],pos[1],medium_gold_width,medium_gold_height))
    for pos in small_gold_pos:
        rects.append(pygame.Rect(pos[0],pos[1],small_gold_width,small_gold_height))
    for pos in big_rock_pos:
        rects.append(pygame.Rect(pos[0],pos[1],big_rock_width,big_rock_height))
    for pos in medium_rock_pos:
        rects.append(pygame.Rect(pos[0],pos[1],medium_rock_width,medium_rock_height))
    for pos in small_rock_pos:
        rects.append(pygame.Rect(pos[0],pos[1],small_rock_width,small_rock_height))
    
    # for rect in rects:
    #     pygame.draw.rect(screen, (0,0,0), rect, 1)
    return rects

def update_rect_pos( new_pos):
    index = grabbed_index
    if index < len(big_gold_pos):
        big_gold_pos[index] = new_pos
        return

    index = index - len(big_gold_pos)
    if index < len(medium_gold_pos):
        medium_gold_pos[index]= new_pos
        return
    index = index - len(medium_gold_pos)
    if index < len(small_gold_pos):
        small_gold_pos[index]= new_pos
        return
    index = index - len(small_gold_pos)
    if index < len(big_rock_pos):
        big_rock_pos[index]= new_pos
        return
    index = index - len(big_rock_pos)
    if index < len(medium_rock_pos):
        medium_rock_pos[index]= new_pos
        return
    index = index - len(medium_rock_pos)
    if index < len(small_rock_pos):
        small_rock_pos[index]= new_pos

def get_type_of_grabbed_item():
    index = grabbed_index
    if index < len(big_gold_pos):
        return 'bg'

    index = index - len(big_gold_pos)
    if index < len(medium_gold_pos):
        return 'mg'

    index = index - len(medium_gold_pos)
    if index < len(small_gold_pos):
        return 'sg'

    index = index - len(small_gold_pos)
    if index < len(big_rock_pos):
        return 'br'

    index = index - len(big_rock_pos)
    if index < len(medium_rock_pos):
        return 'mr'

    index = index - len(medium_rock_pos)
    if index < len(small_rock_pos):
        return 'sr'

    return 'nothing'

def remove_grabbed_rect_pos():
    index = grabbed_index
    if index < len(big_gold_pos):
        del big_gold_pos[index]
        return 'bg'

    index = index - len(big_gold_pos)
    if index < len(medium_gold_pos):
        del medium_gold_pos[index]
        return 'mg'
    index = index - len(medium_gold_pos)
    if index < len(small_gold_pos):
        del small_gold_pos[index]
        return 'sg'
    index = index - len(small_gold_pos)
    if index < len(big_rock_pos):
        del big_rock_pos[index]
        return 'br'
    index = index - len(big_rock_pos)
    if index < len(medium_rock_pos):
        del medium_rock_pos[index]
        return 'mr'
    index = index - len(medium_rock_pos)
    if index < len(small_rock_pos):
        del small_rock_pos[index]
        return 'sr'

def cal_score():
    score = 0
    for item in collected:
        type = item[0]
        if type == 'bg':
            score += 60
        elif type == 'br':
            score += 20
        elif type == 'mg':
            score += 50
        elif type == 'mr':
            score += 10
        elif type == 'sg':
            score += 40
        elif type == 'sr':
            score += 5
    return score

def cal_angle():
    x = claw_pos[0] + (claw_width/2)- START[0]
    y = claw_pos[1] - START[1]
    angle = math.degrees(math.atan2(x,y))
    return angle

def swing_rope():
    global claw_pos, state, swing_direction, claw_angle
    current_angle = cal_angle() 
    x = claw_pos[0] + (claw_width/2)- START[0]
    y = claw_pos[1] - START[1]
    
    current_rope_length = y / math.cos(math.radians(current_angle))
    if swing_direction == 1:
        current_angle += 1
        claw_angle += 2
        if current_angle >= 90:
            swing_direction = -1
    elif swing_direction == -1:
        current_angle -= 1
        claw_angle -= 2
        if current_angle <= -90:
            swing_direction = 1

    new_x = current_rope_length * math.sin(math.radians(current_angle))
    new_y = current_rope_length * math.cos(math.radians(current_angle))

    x_added = new_x - x
    y_added = new_y - y

    y = claw_pos[1] + y_added
    x = claw_pos[0] + x_added

    claw_pos = (x,y)

def draw_score():
    score = cal_score()
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    # score_text_rect = score_text.get_rect()
    # score_text_rect.x = score_text_rect.get_width()
    screen.blit(score_text, (700,50))

def draw_rope_n_claw():
    line = pygame.draw.line(screen, (0,0,0), START, (claw_pos[0] + (claw_width/2),claw_pos[1]))
    screen.blit(claw, claw_pos)
    claw_rect = pygame.Rect(claw_pos[0],claw_pos[1],50,50)
    # pygame.draw.rect(screen, (0,0,0),claw_rect,1)
    return claw_rect

def fetch():
    global claw_pos
    global state
    current_angle = cal_angle()

    x = claw_pos[0] + (claw_width/2)- START[0]
    y = claw_pos[1] - START[1]
    
    current_rope_length = y / math.cos(math.radians(current_angle))
    current_rope_length += org_speed
    new_x = current_rope_length * math.sin(math.radians(current_angle))
    new_y = current_rope_length * math.cos(math.radians(current_angle))
    x_added = new_x - x
    y_added = new_y - y
    y = claw_pos[1] + y_added
    x = claw_pos[0] + x_added
    claw_pos = (x,y)


def back():
    global claw_pos
    global state
    current_angle = cal_angle()
    x = claw_pos[0] + (claw_width/2)- START[0]
    y = claw_pos[1] - START[1]
    current_rope_length = y / math.cos(math.radians(current_angle))
    if state == 3:
        type = get_type_of_grabbed_item()
        if type == 'bg' or type =='br':
            speed = 1
        elif type == 'mg' or type =='mr':
            speed = 2
        elif type == 'sg' or type =='sr':
            speed = 3
    
        current_rope_length -= speed

    else:
        speed = org_speed
        current_rope_length -= speed
        
    
    new_x = current_rope_length * math.sin(math.radians(current_angle))
    new_y = current_rope_length * math.cos(math.radians(current_angle))
    x_added = new_x - x
    y_added = new_y - y
    y = claw_pos[1] + y_added
    x = claw_pos[0] + x_added
    claw_pos = (x,y)
    global grabbed_index

    if grabbed_index >= 0:
        update_rect_pos(claw_pos)

    return_rect = (400,150,200,50)
    if claw_rect.colliderect(return_rect):
        if state == 3:
            item = remove_grabbed_rect_pos()
            state = 1
            grabbed_index = -1
            num_of_collected_items = len(collected)
            collected.append((item,(num_of_collected_items * 75 + 20,20)))
        else:
            state = 1
running = True

form_big_gold()
form_medium_gold()
form_small_gold()
form_big_rock()
form_medium_rock()
form_small_rock()

while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONUP:
            state = 2

        elif event.type == QUIT:
            running = False
    
    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command
    pygame.draw.rect(screen, SAND, (0, 150, WIDTH, HEIGHT - 150))
    claw_rect = draw_rope_n_claw()
    screen.blit(miner,(WIDTH / 2 - 40, 50))
    draw_big_gold()
    draw_medium_gold()
    draw_small_gold()
    draw_big_rock()
    draw_medium_rock()
    draw_small_rock()
    draw_collected()
    draw_score()
    if state == 1:
       swing_rope()
    elif state == 2:
        fetch()
    elif state == 3 or state ==4:
        back()

    rects = get_all_rects()

    ind = pygame.Rect.collidelist(claw_rect,rects)
    if (ind != -1):
        state = 3
        grabbed_index = ind
    if claw_pos[0] > 1000 or claw_pos[0] < 0 or claw_pos[1] > 700:
        state = 4
    
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
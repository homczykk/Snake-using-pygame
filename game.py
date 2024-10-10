import pygame
from sys import exit
import random

RESOLUTION = (32*20, 32*20)
FRAMERATE = 15

def draw_grid():
    if is_grid:
        for i in range(20):
            pygame.draw.line(window, "gray30", (32*i, 0), (32*i, RESOLUTION[1]))
            
        for i in range(20):
            pygame.draw.line(window, "gray30", (0, 32*i), (RESOLUTION[1], 32*i))

        grid_msg_surf = font.render(f"Grid: ON", False, "white")
    else:
        grid_msg_surf = font.render(f"Grid: OFF", False, "white")

    grid_msg_rect = grid_msg_surf.get_rect(midbottom = (100, 40))
    window.blit(grid_msg_surf, grid_msg_rect)

def take_direction():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        snake_direction[0] = 0
        snake_direction[1] = -32
    if keys[pygame.K_a]:
        snake_direction[0] = -32
        snake_direction[1] = 0
    if keys[pygame.K_s]:
        snake_direction[0] = 0
        snake_direction[1] = 32
    if keys[pygame.K_d]:
        snake_direction[0] = 32
        snake_direction[1] = 0

    return snake_direction

def segments_movement():
    if len(segment_list) > 1:
        for i in range(len(segment_list)-1):
            segment_list[len(segment_list)-i-1].centerx = segment_list[len(segment_list)-i-2].centerx
            segment_list[len(segment_list)-i-1].centery = segment_list[len(segment_list)-i-2].centery
    
    for i in range(len(segment_list)-1):
        window.blit(segment_surf, segment_list[i+1])

def snake_growth():
    score = 0
    if head_rect.colliderect(food_rect):
        food_rect.x = random.randint(0, 19) * 32 + 1
        food_rect.y = random.randint(0, 19) * 32 + 1

        segment_list.append(segment_surf.get_rect(topleft = (1,1)))
        score = 1

    window.blit(food_surf, food_rect)
    return score

def show_score():
    score_surf = font.render(f"Score: {score}", False, "white")
    score_rect = score_surf.get_rect(midbottom = (32*16, 40))
    window.blit(score_surf, score_rect)

def game_end():
    if head_rect.centerx < 0 or head_rect.centerx > 32*20: 
        pygame.quit()
        exit()
    if head_rect.centery < 0 or head_rect.centery > 32*20:
        pygame.quit()
        exit()

def snake_movement():
    head_rect.centerx += take_direction()[0]
    head_rect.centery += take_direction()[1]
    window.blit(head_surf, head_rect)

pygame.init()
window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf', 50)
score = 0

head_surf = pygame.Surface((31,31))
head_rect = head_surf.get_rect(topleft = (1,1))
head_surf.fill("green")
snake_direction = [32, 0]

food_surf = pygame.Surface((32,32))
food_rect = food_surf.get_rect(topleft = (32*10+1,32*10+1))
food_surf.fill("red")

segment_surf = pygame.Surface((30,30))
segment_surf.fill("green")
segment_list = [head_rect]

is_grid = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                if is_grid:
                    is_grid = False
                else:
                    is_grid = True

    window.fill("black")

    segments_movement()
    score += snake_growth()
    snake_movement()
    draw_grid()
    show_score()
    game_end()

    pygame.display.update()
    clock.tick(FRAMERATE)

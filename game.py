import pygame, random
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((CELL_SIZE-1, CELL_SIZE-1))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = (CELL_SIZE*3/2,CELL_SIZE*3/2))

        self.direction = [26, 0]

        self.segment_surf = pygame.Surface((CELL_SIZE-3,CELL_SIZE-3))
        self.segment_surf.fill("green")
        self.segment_list = [self.rect,
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE))]
        self.score = 0
    
    def segments_movement(self):
        if len(self.segment_list) > 1:
            for i in range(len(self.segment_list)-1):
                self.segment_list[len(self.segment_list)-i-1].centerx = self.segment_list[len(self.segment_list)-i-2].centerx
                self.segment_list[len(self.segment_list)-i-1].centery = self.segment_list[len(self.segment_list)-i-2].centery
        
        for i in range(len(self.segment_list)-1):
            window.blit(self.segment_surf, self.segment_list[i+1])
        
    def snake_grow(self):
        if pygame.sprite.spritecollide(player_group.sprite, food_group, False):
            food.rect.centerx = random.randint(0, 19)*CELL_SIZE + 13
            food.rect.centery = random.randint(1, 19)*CELL_SIZE + 13
            
            self.segment_list.append(self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE)))
            self.score += 1

    def snake_move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction[0] = 0
            self.direction[1] = -CELL_SIZE
        if keys[pygame.K_s]:
            self.direction[0] = 0
            self.direction[1] = CELL_SIZE
        if keys[pygame.K_a]:
            self.direction[0] = -CELL_SIZE
            self.direction[1] = 0
        if keys[pygame.K_d]:
            self.direction[0] = CELL_SIZE
            self.direction[1] = 0

        self.rect.centerx += self.direction[0]
        self.rect.centery += self.direction[1]

    def end_game(self):
        if self.rect.centerx > RESOLUTION[0] or self.rect.centerx < 0:
            pygame.quit()
            exit()
        if self.rect.centery > RESOLUTION[1] or self.rect.centery < CELL_SIZE:
            pygame.quit()
            exit()
        
        for i in range(2, len(self.segment_list)):
            if self.segment_list[i].centerx == self.rect.centerx and self.segment_list[i].centery == self.rect.centery:
                pygame.quit()
                exit()

    def update(self):
        self.end_game()
        self.segments_movement()
        self.snake_move()
        self.snake_grow()


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((CELL_SIZE-1, CELL_SIZE-1))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = (CELL_SIZE*10+13, CELL_SIZE*10+13))
def draw_grid():
    for i in range(CELL_NUMBER + 1):
        if i == 0:
            pass
        else:
            pygame.draw.line(window, "gray30", (i*CELL_SIZE, CELL_SIZE), (i*CELL_SIZE, RESOLUTION[1]))
            pygame.draw.line(window, "gray30", (0, i*CELL_SIZE), (RESOLUTION[1], i*CELL_SIZE))
            
def score_zone(score):
    score_zone_surf = pygame.Surface((RESOLUTION[0], CELL_SIZE))
    score_zone_surf.fill("gray20")
    score_zone_rect = score_zone_surf.get_rect(topleft = (0,0))

    score_surf = FONT.render(f'Score: {score}', False, "white")
    score_rect = score_surf.get_rect(center = (RESOLUTION[0]/2, 18))

    window.blit(score_zone_surf, score_zone_rect)
    window.blit(score_surf, score_rect)

CELL_SIZE = 26
CELL_NUMBER = 27
RESOLUTION = (CELL_SIZE*CELL_NUMBER+1,CELL_SIZE*CELL_NUMBER+1)
FRAMERATE = 15

pygame.init()

FONT = pygame.font.Font('font/Pixeltype.ttf', 50)
window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

food_group = pygame.sprite.GroupSingle()
food = Food()
food_group.add(food)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.fill("black")
    draw_grid()

    score_zone(player.score)

    player_group.draw(window)
    food_group.draw(window)
    player_group.update()
    food_group.update()

    pygame.display.update()
    clock.tick(FRAMERATE)
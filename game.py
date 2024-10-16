import pygame, random, json
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((CELL_SIZE-1, CELL_SIZE-1))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = (round(CELL_SIZE*3/2),round(CELL_SIZE*3/2)))

        self.direction = [CELL_SIZE, 0]

        self.segment_surf = pygame.Surface((CELL_SIZE-3,CELL_SIZE-3))
        self.segment_surf.fill("green")
        self.segment_list = [self.rect,
                             self.segment_surf.get_rect(center = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(center = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(center = (-CELL_SIZE, -CELL_SIZE))]
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
            food.rect.centerx = random.randint(0, CELL_NUMBER-1)*CELL_SIZE + round(CELL_SIZE/2)
            food.rect.centery = random.randint(1, CELL_NUMBER-1)*CELL_SIZE + round(CELL_SIZE/2)
            
            self.segment_list.append(self.segment_surf.get_rect(center = (-CELL_SIZE, -CELL_SIZE)))
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

    def save_score(self):
        with open("scores.json", "r") as f:
            data = json.load(f)

        if self.score >= 5:
            data["scores"].append({"score": self.score})
        
        with open("scores.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def reset_state(self):
        self.score = 0       
        self.rect.center = (CELL_SIZE*3/2,CELL_SIZE*3/2)
        self.segment_list = [self.rect,
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE)),
                             self.segment_surf.get_rect(topleft = (-CELL_SIZE, -CELL_SIZE))]
        self.direction = [CELL_SIZE, 0]

    def update(self):
        self.segments_movement()
        self.snake_move()
        self.snake_grow()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((CELL_SIZE-1, CELL_SIZE-1))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = (CELL_SIZE*round(CELL_NUMBER/2)+round(CELL_SIZE/2), CELL_SIZE*round(CELL_NUMBER/2)+round(CELL_SIZE/2)))

def draw_grid():
    for i in range(CELL_NUMBER + 1):
        if i == 0:
            pass
        else:
            pygame.draw.line(window, "gray30", (i*CELL_SIZE, CELL_SIZE), (i*CELL_SIZE, RESOLUTION[1]))
            pygame.draw.line(window, "gray30", (0, i*CELL_SIZE), (RESOLUTION[1], i*CELL_SIZE))
            
def score_zone(score):
    score_zone_surf = pygame.Surface((RESOLUTION[0], CELL_SIZE))
    score_zone_surf.fill("gray5")
    score_zone_rect = score_zone_surf.get_rect(topleft = (0,0))

    score_surf = FONT.render(f'Score: {score}', False, "white")
    score_rect = score_surf.get_rect(center = (RESOLUTION[0]/2, CELL_SIZE*0.65))

    window.blit(score_zone_surf, score_zone_rect)
    window.blit(score_surf, score_rect)

def ranking():
    window.blit(end_game_title, end_game_title_rect)
    window.blit(end_game_msg, end_game_msg_rect)

    with open('scores.json') as f:
        data = json.load(f) 
        
    sorted_data = sorted(data["scores"], key=lambda x: x["score"], reverse=True)

    first_place_score = int(sorted_data[0]["score"])
    second_place_score = int(sorted_data[1]["score"])
    third_place_score = int(sorted_data[2]["score"])

    spaces = ' '*10
    first_place_surf = FONT.render(f"  1.{spaces}{first_place_score}", False, "gold")
    second_place_surf = FONT.render(f"2.{spaces}{second_place_score}", False, "silver")
    third_place_surf = FONT.render(f"3.{spaces}{third_place_score}", False, "darkorange3")

    offset = 65
    first_place_rect = first_place_surf.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]/2 - offset))
    second_place_rect = second_place_surf.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]/2))
    third_place_rect = third_place_surf.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]/2 + offset))
    
    window.blit(ranking_surf, ranking_rect)
    window.blit(first_place_surf, first_place_rect)
    window.blit(second_place_surf, second_place_rect)
    window.blit(third_place_surf, third_place_rect)

def end_game():
    if player.rect.centerx > RESOLUTION[0] or player.rect.centerx < 0:
        return True
    if player.rect.centery > RESOLUTION[1] or player.rect.centery < CELL_SIZE:
        return True
    for i in range(2, len(player.segment_list)):
        if player.segment_list[i].centerx == player.rect.centerx and player.segment_list[i].centery == player.rect.centery:
            return True
    
    return False

# These can be changed
FRAMERATE = 15 # At least 15 FPS.
CELL_SIZE = 40 # This must be even
CELL_NUMBER = 15 

RESOLUTION = (CELL_SIZE*CELL_NUMBER+1,CELL_SIZE*CELL_NUMBER+1)

pygame.init()

FONT = pygame.font.Font('font/Pixeltype.ttf', 50)
FONT_TITLE = pygame.font.Font('font/ARCADE.ttf', CELL_NUMBER * 8)

window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

food_group = pygame.sprite.GroupSingle()
food = Food()
food_group.add(food)

end_game_title = FONT_TITLE.render('SNAKE', False, "green")
end_game_title_rect = end_game_title.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]/4))

end_game_msg = FONT.render('-- press r to play --', False, "grey30")
end_game_msg_rect = end_game_msg.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]*9/10))

ranking_surf = pygame.Surface((200, 200))
ranking_surf.fill("grey5")
ranking_rect = ranking_surf.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[0]/2))

is_first_attempt = True
is_score_saved = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if end_game():
                    player.reset_state()
                    is_score_saved = False
                if is_first_attempt:
                    is_first_attempt = False

    if end_game() or is_first_attempt:
        
        if not is_score_saved:
            player.save_score()
            is_score_saved = True

        window.fill("black")
        ranking()

    else:
        window.fill("black")
        draw_grid()

        score_zone(player.score)

        player_group.draw(window)
        food_group.draw(window)
        player_group.update()
        food_group.update()

    pygame.display.update()
    clock.tick(FRAMERATE)
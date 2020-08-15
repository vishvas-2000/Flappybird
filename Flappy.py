import pygame, sys
import random


# Game Variables
screen_width = 288
screen_height = 512
BASE_MOVE = 0
PIPES_MOVE = 0
BIRD_FLAP = 0
BIRD_ANIMATION = 30
GRAVITY = 6
BIRD_JUMP = 5
PIPE_HEIGHT = [180, 260, 350]

class hello_bird():
    def __init__(self, bird_surface, bird_jump, gravity):
#         self.frames = bird_frames
        self.y = 256
        self.jumpCount = bird_jump
        self.gravity = gravity
        self.surface = bird_surface
        self.rect = self.surface.get_rect()
        self.isJump = False 
        self.score = 0
        self.high_score = 0
 
    def draw(self):
        self.y += self.gravity
#        bird_rect = self.surface.get_rect()
#        pygame.draw.rect(screen, (255, 0,0),(bird_rect.topleft[0],bird_rect.topleft[1],bird_rect.bottomright[0],bird_rect.bottomright[1]),4)
        screen.blit(self.surface, (100, self.y))

    def hit(self, pipes_list):
        if bird.y >= -20 and bird.y <= 400:
            for pipe in pipes_list:
                self.rect = self.surface.get_rect(center = (100,self.y))
                if self.rect.colliderect(pipe):
                    death_sound.play()
                    return True
        else:
            death_sound.play()
            return True
        
class hii_pipes():
    def __init__(self, pipe_height, pipe_surface):
        self.count = 0
        self.surface = pipe_surface
        self.height_list = pipe_height
        self.max = 8
        self.list = []
        
    def create_list(self):
        position  = random.choice(self.height_list)
        bottom_pipe = pipe_surface.get_rect(midtop = (350, position))
        top_pipe = pipe_surface.get_rect(midbottom = (350, position - 160))
        self.list.extend([bottom_pipe, top_pipe])
        if len(self.list) >self.max:
            self.list.pop(0)
            self.list.pop(1)
    
    def move(self):
        for pipe in self.list:
            pipe.centerx -= 5
        return self.list
    
    def draw(self):
        for pipe in self.list:
            if pipe.bottom > 300:
 #               pygame.draw.rect(screen, (255, 0,0),(pipe.topleft[0],pipe.topleft[1],pipe.bottomright[0],pipe.bottomright[1]),4)
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface,False,True)
#                pygame.draw.rect(screen, (255, 0,0),(pipe.topleft[0],pipe.topleft[1],pipe.bottomright[0],pipe.bottomright[1]),4)
                screen.blit(flip_pipe,pipe)
 
def draw_base(base, BASE_MOVE):
    if BASE_MOVE <288:
        screen.blit(base, (-BASE_MOVE,450))
        screen.blit(base, (288-BASE_MOVE,450))
        return BASE_MOVE + 1
    else:
        BASE_MOVE = 0
        screen.blit(base, (-BASE_MOVE,450))
        screen.blit(base, (288-BASE_MOVE,450))
        return BASE_MOVE
    
 # Game Assets
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((screen_width,screen_height))

bg = pygame.image.load('images/background-day.png')

bird_upflap = pygame.image.load('images/bluebird-upflap.png').convert_alpha()
bird_midflap = pygame.image.load('images/bluebird-midflap.png').convert_alpha()
bird_downflap = pygame.image.load('images/bluebird-downflap.png').convert_alpha()
bird_frames = [bird_upflap, bird_midflap, bird_downflap]


base = pygame.image.load('images/base.png').convert()

game_over_surface = pygame.image.load('images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

pipe_surface = pygame.image.load('images/pipe-green.png').convert_alpha()

flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')

clock = pygame.time.Clock()

bird = hello_bird(bird_midflap, BIRD_JUMP, GRAVITY)
pipes = hii_pipes(PIPE_HEIGHT, pipe_surface)

def redraw(BASE_MOVE):
    screen.blit(bg, (0,0))
    bird.draw()
    pipes.draw()
    font = pygame.font.SysFont('comicsans', 40, True)
    text = font.render('Score : ' + str(bird.score), 1 ,(0, 0, 0) )
    text_rect = text.get_rect(center = (144, 40))
    screen.blit(text, text_rect)
    BASE_MOVE = draw_base(base, BASE_MOVE)
    pygame.display.update()
    return BASE_MOVE
# Main loop
game_active = True
game_over = False
pipe_spawner = 0
score_loop = 0
while game_active :
    pipe_spawner +=1
    if pipe_spawner >= 60:
        pipe_spawner = 0
        pipes.create_list()
        
    score_loop +=1
    if score_loop >= 20:
        bird.score += 1
        score_loop = 0

    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not(bird.isJump):
        if keys[pygame.K_SPACE]:
            bird.isJump = True
            flap_sound.play()
    else:
        if bird.jumpCount >= -1 and bird.jumpCount <=BIRD_JUMP:
            neg = 1
            if bird.jumpCount < 0:
                neg = -1
            bird.y -= (bird.jumpCount ** 2)* 2 * neg
            bird.jumpCount -= 1
            bird.surface = pygame.transform.rotozoom(bird_midflap,bird.jumpCount * 6,1)
            bird.x = 100
        else:
            bird.surface = pygame.transform.rotozoom(bird_midflap,bird.jumpCount * 12,1)
            bird.isJump = False
            bird.jumpCount = BIRD_JUMP



    game_over = bird.hit(pipes.list)
    if not game_over:
        pipes.list = pipes.move()
        BASE_MOVE = redraw(BASE_MOVE)

    if game_over:
        if bird.score >= bird.high_score:
            bird.high_score = bird.score
        font = pygame.font.SysFont('comicsans', 40, True)
        text = font.render('Score : ' + str(bird.score), 1 ,(0, 0, 0) )
        text_rect = text.get_rect(center = (144, 40))
        screen.blit(text, text_rect) 
        text2 = font.render('High Score : ' + str(bird.high_score), 1 ,(0, 0, 0) )
        text2_rect = text2.get_rect(center = (144, 400))
        screen.blit(text2, text2_rect)
        screen.blit(game_over_surface, game_over_rect)
        pipes.list.clear()
        bird.y = 256
        bird.score = 0
        pygame.display.update()
        key = pygame.key.get_pressed()
        for i in range(20000):
            if key[pygame.QUIT]:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        game_over = False  
        


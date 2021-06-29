import pygame
import numpy as np 
import random
screen_width = 288
screen_height = 512

class flappy_bird():
    def __init__(self):
        self.y = 256
        self.maxJump = 5
        self.jumpCount = 5
        self.gravity = 6
        self.bird = pygame.image.load('images/bluebird-midflap.png').convert_alpha()
        self.surface = self.bird
        self.rect = self.surface.get_rect()
        self.isJump = False 
        self.score = 0
        self.high_score = 0
        self.radius = 12
        self.hitbox = [100, self.y, self.radius]
        self.isAlive = True
        self.pipe = pipe()
        
    def update(self):
        self.y += self.gravity
        
    def draw(self, screen):
        screen.blit(self.surface, (100, self.y))
              
    def jump(self):
        if not(self.isJump):
            self.isJump = True
        else:
            if self.jumpCount >= -1 and self.jumpCount <= self.maxJump:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2)* 2 * neg
                self.jumpCount -= 1
                self.surface = pygame.transform.rotozoom(self.bird, self.jumpCount * 6,1)
                self.x = 100
            else:
                self.surface = pygame.transform.rotozoom(self.bird, self.jumpCount * 12,1)
                self.isJump = False
                self.jumpCount = self.maxJump
                
    def distance(self, pipes_list):
        if len(pipes_list) > 0:
            dist = pipes_list[0][0] - 100
            bottom = pipes_list[0][1] - self.y
            top = self.y - pipes_list[1][3]
            return dist, top, bottom
            
            
    def collision(self, pipes_list):
        if self.y >= -20 and self.y <= 420:
            for pipe in pipes_list:
                if pipe[0]<=130 and pipe[0]>=75:
                    if pipe[3]>350:
                        if pipe[1]-self.y < 22:
                              self.isAlive = False
                        
                        elif self.y - pipe[1] < - 320 + 115 + 22:
                              self.isAlive = False

        else:
            self.isAlive = False

class pipe():
    def __init__(self):
        self.count = 0
        self.pipe = pygame.image.load('images/pipe-green.png').convert_alpha()
        self.flipped = pygame.image.load('images/pipe-green-flipped.png').convert_alpha()
        self.height_list = [180, 240, 310, 370]
        self.height = 320
        self.width = 52
        self.max = 8
        self.list = []
        self.create_list()
        
    def create_list(self):
        position  = random.choice(self.height_list)
        bottom_pipe = [350, position, 350 + self.width, position + self.height]
        top_pipe = [350, position-self.height-160, 350 + self.width, position-160]
        self.list.extend([bottom_pipe, top_pipe])
        for pipe in self.list:
            if pipe[0]<= 0:
                self.list.pop(0)
                self.list.pop(0)
                break
                
    def draw(self):
        for pipe in self.list:
            if pipe[3] > 350:
                screen.blit(self.pipe,(pipe[0], pipe[1]))
            else:
                screen.blit(self.flipped,(pipe[0], pipe[1]))

    def update(self):
        for pipe in self.list:
            pipe[0] -= 5
            pipe[2] -= 5
    
    def draw(self, screen):
        for pipe in self.list:
            if pipe[3] > 350:
                screen.blit(self.pipe,(pipe[0], pipe[1]))
            else:
                screen.blit(self.flipped,(pipe[0], pipe[1]))
                
                
class base():
    def __init__(self):
        self.base_move = 0
        self.base_surface = pygame.image.load('images/base.png').convert()
    
    def update(self):
        if self.base_move <288:
            self.base_move += 1
        else:
            self.base_move = 0
            self.base_move += 1
            
    def draw(self, screen):
        screen.blit(self.base_surface, (-self.base_move, 450))
        screen.blit(self.base_surface, (288 - self.base_move, 450))

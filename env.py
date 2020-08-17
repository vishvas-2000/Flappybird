import pygame
import numpy as np 
import random

class FlappyBird2D():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.mode = 0
        self.bird = flappy_bird()
        self.pipes = pipe()
        self.base = base()
        self.maxSteps = 2000
        self.steps = 0
        self.bg = pygame.image.load('images/background-day.png') 
        self.pipe_spawner = 0
    
    def action(self, action):
        if action == 0:
            self.clock.tick(20)
            
            if self.pipe_spawner%60 == 0:
                self.pipes.create_list()
                self.pipe_spawner = 1
            self.pipe_spawner += 1
            
            self.pipes.update()
            self.base.update()
            self.bird.update()
            
            self.bird.collision(self.pipes.list)
            
            self.steps += 1
            
        elif action == 1:
            self.clock.tick(20)
            
            if self.pipe_spawner%60 == 0:
                self.pipes.create_list()
                self.pipe_spawner = 1
            self.pipe_spawner += 1
            
            self.bird.jump()
            self.pipes.update()
            self.base.update()
            self.bird.update()
            
            self.bird.collision(self.pipes.list)
            
            self.steps += 1
            
    def evaluate(self):
        reward = 0 
        if self.bird.isAlive:
            reward = 1
        else:
            reward = 0
        return reward
    
    def is_done(self):
        if not self.bird.isAlive or self.steps >= self.maxSteps:
            return True
        return False
    
    def observe(self):
        return self.bird.distance(self.pipes.list)
    
    def view(self):
        # draw game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                done = True
                
        self.screen.blit(self.bg, (0, 0))
        self.bird.draw(self.screen)
        self.base.draw(self.screen)
        self.pipes.draw(self.screen)
        
        text = self.font.render('Score : ' + str(self.bird.score), 1 ,(255, 0, 0) )
        text_rect = text.get_rect(center = (144, 40))
        self.screen.blit(text, text_rect)

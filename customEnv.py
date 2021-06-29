from env import *
from gym import spaces
import numpy as np
class CustomEnv():
    def __init__(self):
        self.pygame = FlappyBird2D()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(np.array([0, 0, 0]),np.array([200,200,200]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = FlappyBird2D()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()
        

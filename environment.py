import gym
from gym import spaces
import pygame
import random
import numpy as np

class ShoverWorldEnv(gym.Env):
    def __init__(self, n_rows: int = 6, n_cols: int = 6, max_timestep: int = 100, number_of_boxes: int  = 10, number_of_barriers: int = 4) -> None:
        super().__init__()
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.max_timestep = max_timestep
        self.number_of_boxes = number_of_boxes
        self.number_of_barriers = number_of_barriers

        self.observation_space = spaces.Box(low=-1, high=2, shape=(self.n_rows, self.n_cols), dtype=int)
        self.action_space = spaces.Tuple((spaces.Discrete(self.n_rows), spaces.Discrete(self.n_cols), spaces.Discrete(4)))
        '''
            0 -> Up
            1 -> Right
            2 -> Down
            3 -> Left
        '''

        self.map = [[0 for j in range(self.n_cols)] for i in range(self.n_rows)]
        self.last_pos = None
        self.last_dir = None
        self._generate_map()
        
    def reset(self):
        self.map = [[0 for j in range(self.n_cols)] for i in range(self.n_rows)]
        self.last_dir = None
        self.last_pos = None
        self._generate_map()

    def step(self, action):
        pass

    def _generate_map(self):
        '''
            -1 -> Lava
            0 -> Empty slot
            1 -> Box
            2 -> barrier
        '''
        for i in range(self.n_rows):
            if i == 0 or i == self.n_rows - 1:
                self.map[i] = [-1 for _ in range(self.n_cols)]
            
            else:
                self.map[i][0] = -1
                self.map[i][-1] = -1
        
        k = 0
        while True:
            if k == self.number_of_barriers:
                break
            
            pos_x = random.randint(1, self.n_rows-1)
            pos_y = random.randint(1, self.n_cols-1)

            if self.map[pos_x][pos_y] == 0:
                self.map[pos_x][pos_y] = 2
                k += 1
            
        k = 0
        while True:
            if k == self.number_of_boxes:
                break

            pos_x = random.randint(1, self.n_rows-1)
            pos_y = random.randint(1, self.n_cols-1)

            if self.map[pos_x][pos_y] == 0:
                self.map[pos_x][pos_y] = 1
                k += 1
                



    def _get_obs(self):
        return self.map

    def _get_info(self):
        return {"previous_direction": self.last_dir, 'previous_position': self.last_pos}

    def render(self):
        pass
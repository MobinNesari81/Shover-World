import gym
from gym import spaces
import pygame
import random
import numpy as np
from typing import Optional
import sys

class ShoverWorldEnv(gym.Env):
    metadata = {
        "render_modes": ['human', 'ansi', 'rgb_array']
    }
    def __init__(self, render_mode: Optional[str] = None, n_rows: int = 6, n_cols: int = 6, max_timestep: int = 100, number_of_boxes: int  = 10, number_of_barriers: int = 4) -> None:
        super().__init__()
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.max_timestep = max_timestep
        self.number_of_boxes = number_of_boxes
        self.number_of_barriers = number_of_barriers

        self.observation_space = spaces.Box(low=-1, high=2, shape=(self.n_rows, self.n_cols), dtype=int)
        self.action_space = spaces.Tuple((spaces.Discrete(self.n_rows), spaces.Discrete(self.n_cols), spaces.Discrete(4)))

        self.map = [[0 for j in range(self.n_cols)] for i in range(self.n_rows)]
        self.last_pos = None
        self.last_dir = None
        self.time_step = 1 

        # Initialize Pygame for visualization
        self.pygame_initialized = False
        self.render_mode = render_mode
        self.window = None
        self.cell_size = None

    def reset(self):
        self.map = [[0 for j in range(self.n_cols)] for i in range(self.n_rows)]
        self.last_dir = None
        self.last_pos = None
        self._generate_map()
        return self._get_obs()

    def step(self, action):
        # ... your existing step function ...
        # Make sure to update the environment state based on the action taken
        self.time_step += 1
        if self.time_step > self.max_timestep:
            self.render()
            return self._get_obs(), 0, True, self._get_info()

        reward = 0 
        # Check if the action is the same as the last one
        if self.last_pos == (action[0], action[1]) and self.last_dir==action[2]:
            reward += 1 
        
        # update the last pose and dir 
        self.last_pos = (action[0], action[1])
        self.last_dir = action[2]
             
        directions = {
            0 : (-1, 0), # Up 
            1 : (0, 1),  # Right 
            2 : (1, 0),  # Down 
            3 : (0, -1)  # Left
        }

        self.last_action = action
        row, col = action[0], action[1]
        dr, dc = directions[action[2]]

        if self.map[action[0]][action[1]] != 1: # if the selected point is a box
            return self.map 
        else: 
            # Counting boxes in the same direction line
            count_one = 0 
            while self.map[row][col] == 1: 
                count_one += 1 
                row += dr 
                col += dc 
            row -= dr 
            col -= dc 
            reward -= count_one 
        


        # Moving the box and any boxes in line with it (recursively) 
        for _ in range(count_one): 
            if (0 <= row+dr < len(self.map) and 0 <= col+dc < len(self.map[0]) and self.map[row+dr][col+dc] != 2):
                # If next point is lava, remove the box
                if self.map[row+dr][col+dc] == -1: 
                    self.map[row][col] = 0 
                    row -= dr 
                    col -= dc               
                # If next point is empty, move the box
                elif self.map[row+dr][col+dc] == 0:
                    self.map[row][col], self.map[row+dr][col+dc] = self.map[row+dr][col+dc], self.map[row][col]
                    print(self.map[row][col], self.map[row+dr][col+dc])
                    row -= dr 
                    col -= dc 
                else:
                    break 

            else:
                break 
        
        if not any(1 in row for row in self.map):
            self.render()
            return self._get_obs(), reward, True, self.get_info()
        else:
            self.render()
            return self._get_obs(), reward, False, self._get_info()

    def render(self):
        if self.render_mode == "human":
            if not self.pygame_initialized:
                pygame.init()
                self.pygame_initialized = True
                window_size = 500  # You can adjust this window size
                self.cell_size = window_size // max(self.n_rows, self.n_cols)
                self.window = pygame.display.set_mode((self.cell_size * self.n_cols, self.cell_size * self.n_rows))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.window.fill((255, 255, 255))

            for row in range(self.n_rows):
                for col in range(self.n_cols):
                    value = self.map[row][col]
                    color = None
                    if value == -1:
                        color = (255, 0, 0)  # Red for lava
                    elif value == 0:
                        color = (255, 255, 255)  # White for empty slot
                    elif value == 1:
                        color = (255, 255, 0)  # Yellow for boxes
                    elif value == 2:
                        color = (0, 0, 0)  # Black for barriers

                    if color:
                        pygame.draw.rect(self.window, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

            self._draw_grid()
            pygame.display.flip()
            pygame.event.pump()
            pygame.display.update()
            pygame.time.Clock().tick(4)

    def close(self):
        pygame.quit()

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

    def _draw_grid(self):
        for x in range(0, self.n_rows * self.cell_size, self.cell_size):
            pygame.draw.line(self.window, (0, 0, 0), (x, 0), (x, self.n_cols * self.cell_size))
        for y in range(0, self.n_cols * self.cell_size, self.cell_size):
            pygame.draw.line(self.window, (0, 0, 0), (0, y), (self.n_rows * self.cell_size, y))
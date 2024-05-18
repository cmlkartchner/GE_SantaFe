import random as re
import pygame

''' TODO: 
        - agent is responding to keybaord commands (moves with arrows)
        - remove the keyboard move feature and implement allowed moves
        - study more about fitness and how that impacts the agent's performance
'''

class Agent:
    ''' Moves that can be performed by agent: move left, move right, move ahead '''
    def __init__(self, size, rows):
        self.size = size
        self.rows = rows
        self.grid_size = size // rows
        self.x = re.randint(0, rows - 1) * self.grid_size
        self.y = re.randint(0, rows - 1) * self.grid_size
        self.color = (0, 255, 0)

    def move(self, direction):
        if direction == 'up':
            self.y = max(self.y - self.grid_size, 0)
        elif direction == 'down':
            self.y = min(self.y + self.grid_size, self.size - self.grid_size)
        elif direction == 'left':
            self.x = max(self.x - self.grid_size, 0)
        elif direction == 'right':
            self.x = min(self.x + self.grid_size, self.size - self.grid_size)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.grid_size, self.grid_size))
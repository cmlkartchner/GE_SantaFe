import pygame
import sys
import random
from agent import Agent

class Environment:
    def __init__(self, size, rows, num_rewards):
        self.size = size
        self.rows = rows
        self.num_rewards = num_rewards
        self.rewards_list = self.generate_rewards()
        self.agent = Agent(size, rows)
        self.window = pygame.display.set_mode((size, size))
        pygame.display.set_caption("Environment")

    def generate_rewards(self):
        ''' This method generates random rewards within the grid '''
        grid_size = self.size // self.rows
        rewards_list = []
        occupied_positions = set()
        # for _ in range(self.num_rewards):
        #     x = random.randint(0, self.rows - 1) * grid_size
        #     y = random.randint(0, self.rows - 1) * grid_size
        #     rewards_list.append((x, y))
        while len(rewards_list) < 89:
            x = random.randint(0, self.rows - 1) * grid_size
            y = random.randint(0, self.rows - 1) * grid_size
            if (x, y) not in occupied_positions:
                rewards_list.append((x, y))
                occupied_positions.add((x, y))
        return rewards_list

    def draw_grid(self):
        ''' This method uses pygame to generate the environment for the agent '''
        grid_size = self.size // self.rows
        for i in range(self.rows + 1):
            pygame.draw.line(self.window, (255, 255, 255), (i * grid_size, 0), (i * grid_size, self.size))
            pygame.draw.line(self.window, (255, 255, 255), (0, i * grid_size), (self.size, i * grid_size))
        for reward in self.rewards_list:
            pygame.draw.circle(self.window, (255, 0, 0), (reward[0] + grid_size // 2, reward[1] + grid_size // 2), grid_size // 4)
        self.agent.draw(self.window)

    def redraw(self):
        ''' This method is used to regenerate the environment '''
        self.window.fill((0, 0, 0))
        self.draw_grid()
        pygame.display.update()

    def run(self):
        ''' This method sets up and runs the game loop '''
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.agent.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.agent.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.agent.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.agent.move('right')
            self.redraw()

env = Environment(640, 32, 10)
env.run()
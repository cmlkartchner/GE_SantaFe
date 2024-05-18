import pygame
import sys
import random

''' This function is used to generate random rewards within the grid '''
def generate_rewards(size, rows, num_rewards):
    grid_size = size // rows
    rewards_list = []
    for _ in range(num_rewards):
        x = random.randint(0, rows - 1) * grid_size
        y = random.randint(0, rows - 1) * grid_size
        rewards_list.append((x, y))
    return rewards_list

''' This function is used to use pygame and generate the environment for the agent '''
def draw_grid(window, size, rows, rewards_list):
    grid_size = size // rows
    for i in range(rows + 1):
        pygame.draw.line(window, (255, 255, 255), (i * grid_size, 0), (i * grid_size, size))
        pygame.draw.line(window, (255, 255, 255), (0, i * grid_size), (size, i * grid_size))
    for reward in rewards_list:
        pygame.draw.circle(window, (255, 0, 0), (reward[0] + grid_size // 2, reward[1] + grid_size // 2), grid_size // 4)

''' This function is used to regenerate the environment '''
def redraw(window, size, rows, rewards_list):
    window.fill((0, 0, 0))
    draw_grid(window, size, rows, rewards_list)
    pygame.display.update()

''' This function is used to set the details and create the environment '''
def environment():
    pygame.init()
    size = 500
    rows = 20
    num_rewards = 10
    window = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Environment")
    rewards_list = generate_rewards(size, rows, num_rewards)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        redraw(window, size, rows, rewards_list)

environment()  # running environment
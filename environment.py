import pygame
import sys

def grid(window, size, rows):
    distance_between_rows = size // rows
    for i in range(rows + 1):
        pygame.draw.line(window, (255, 255, 255), (i * distance_between_rows, 0), (i * distance_between_rows, size))
        pygame.draw.line(window, (255, 255, 255), (0, i * distance_between_rows), (size, i * distance_between_rows))

def redraw(window, size, rows):
    window.fill((0, 0, 0))
    grid(window, size, rows)
    pygame.display.update()

def environment():
    pygame.init()
    size = 500
    rows = 20
    window = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Grid Example")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        redraw(window, size, rows)

    pygame.quit()
    sys.exit()

environment()  # running environment
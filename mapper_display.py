```python
import random
import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '-2560,0'

pygame.init()

WIDTH, HEIGHT = 2560, 1440
SCALE = 10  # each "pixel" is 1x1 screen pixels

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Grid")
clock = pygame.time.Clock()

pixel_x = 50
pixel_y = 50
color = (255, 255, 255)  # White color

running = True
while running:
    # screen.fill((0, 0, 0))
    rect = (pixel_x * SCALE, pixel_y * SCALE, SCALE, SCALE)
    pixel_x = random.randint(0, WIDTH - SCALE)  # Move left, right, or stay
    pixel_y = random.randint(0, HEIGHT - SCALE)  # Move up, down, or stay
    SCALE = random.randint(5, 20)  # Randomly change scale
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
    pygame.draw.rect(screen, color, rect)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    pygame.display.flip()
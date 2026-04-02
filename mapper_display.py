import random
from routes import routes
import pygame
import os

WIDTH, HEIGHT = 2560, 1440
os.environ['SDL_VIDEO_WINDOW_POS'] = f'-{WIDTH},0'

pygame.init()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Grid")
clock = pygame.time.Clock()

# Bounding box
LAT_TOP = 39.0037
LAT_BOTTOM = 38.925210
LON_LEFT = -95.3333
LON_RIGHT = -95.177244

def gps_to_pixels(lat, lon):
    x = (lon - LON_LEFT) / (LON_RIGHT - LON_LEFT) * WIDTH
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * HEIGHT
    return (int(x), int(y))

x, y = gps_to_pixels(38.942624, -95.307217)

running = True
print(gps_to_pixels(38.981319, -95.316411))
basemap = pygame.image.load("basemap.png")
while running:
    screen.blit(basemap, (0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    pygame.display.flip()
import random
from routes import routes
import pygame
import os
from stations import stations

WIDTH, HEIGHT = 1920, 1080
#os.environ['SDL_VIDEO_WINDOW_POS'] = f'-{WIDTH},0'
os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,-{HEIGHT}'

pygame.init()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Grid")
clock = pygame.time.Clock()

# Bounding box
LAT_TOP = 39.007504945
LAT_BOTTOM = 38.920453917
LON_LEFT = -95.334342203
LON_RIGHT = -95.172563635

# Map position and size on screen
MAP_X = 0        # pixels from left edge of screen
MAP_Y = 0        # pixels from top edge of screen
MAP_W = 1440     # width of map in pixels
MAP_H = 775     # height of map in pixels

def gps_to_pixels(lat, lon):
    x = MAP_X + (lon - LON_LEFT) / (LON_RIGHT - LON_LEFT) * MAP_W
    y = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * MAP_H
    return (int(x), int(y))

running = True
print(gps_to_pixels(38.981319, -95.316411))
basemap = pygame.image.load("basemap.png")
while running:
    screen.blit(basemap, (0, 0))
    for station_id in stations:
        station = stations[station_id]
        x, y = gps_to_pixels(station["lat"], station["lon"])
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    pygame.display.flip()
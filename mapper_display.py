import math
import pygame
import os
from stations import stations

# Setup for Mercator Meter Mapping
METERS_TOP = 4723671.7973
METERS_BOTTOM = 4709564.8942
METERS_LEFT = -10615542.1886
METERS_RIGHT = -10589604.7236

# Radius of the Earth in meters for Web Mercator math
R_MAJOR = 6378137.0

# --- 2. DISPLAY CONFIGURATION ---
WIDTH, HEIGHT = 1920, 1080
MAP_X, MAP_Y = 0, 0
MAP_W, MAP_H = 1438, 782


# Function to convert GPS (Lat/Lon) to pixel coordinates on the Mercator map
def gps_to_pixels(lat, lon):
    x_m = R_MAJOR * math.radians(lon)
    y_m = R_MAJOR * math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0))
    
    # Map those meters into your pixel workspace
    pixel_x = MAP_X + (x_m - METERS_LEFT) / (METERS_RIGHT - METERS_LEFT) * MAP_W
    pixel_y = MAP_Y + (METERS_TOP - y_m) / (METERS_TOP - METERS_BOTTOM) * MAP_H
    
    return (int(pixel_x), int(pixel_y))



# Pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mercator Meter Mapping")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)

# Load basemap (EPSG:3857 from QGIS)
basemap = pygame.image.load("basemap.png")

# Main loop
running = True
while running:
    #screen.fill((255, 255, 255))
    screen.blit(basemap, (MAP_X, MAP_Y))
    
    # Draw Stations using Lat/Lon
    for station_id, station in stations.items():
        x, y = gps_to_pixels(station["lat"], station["lon"])
        
        # Draw dot and label
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 6)
        label = font.render(station_id, True, (0, 0, 0))
        screen.blit(label, (x + 10, y - 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
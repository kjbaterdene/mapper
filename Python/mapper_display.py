import math
import pygame
import os
import json
from stops import stations

# Routes Data
ROUTES_DIR = "Static_Data/routes_latlon.geojson"

# Setup for Mercator Meter Mapping
METERS_TOP = 4722541.43230000045150518
METERS_BOTTOM = 4710777.48199999984353781
METERS_LEFT = -10613259.2040999997407198
METERS_RIGHT = -10595681.939899999648332

# Radius of the Earth in meters for Web Mercator math
R_MAJOR = 6378137.0

# DISPLAY CONFIGURATION ---
WIDTH, HEIGHT = 2560, 1440
MAP_X, MAP_Y = 0, 0
MAP_W, MAP_H = 2151, 1440
os.environ['SDL_VIDEO_WINDOW_POS'] = f'-{WIDTH},0'

# Load routes data
with open(ROUTES_DIR) as f:
    routes_data = json.load(f)

# Function to convert GPS (Lat/Lon) to pixel coordinates on the Mercator map
def gps_to_pixels(lat, lon):
    x_m = R_MAJOR * math.radians(lon)
    y_m = R_MAJOR * math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0))
    
    # Map those meters into your pixel workspace
    pixel_x = MAP_X + (x_m - METERS_LEFT) / (METERS_RIGHT - METERS_LEFT) * MAP_W
    pixel_y = MAP_Y + (METERS_TOP - y_m) / (METERS_TOP - METERS_BOTTOM) * MAP_H
    
    return (int(pixel_x), int(pixel_y))

def build_route_points(feature):
    """Flatten all segments of a route into one list of pixel coords"""
    points = []
    for segment in feature["geometry"]["coordinates"]:
        for lon, lat in segment:
            points.append(gps_to_pixels(lat, lon))
    return points

# Pick a route to trace - change the index to try different routes
tracer_feature = routes_data["features"][0]
tracer = {
    "points": build_route_points(tracer_feature),
    "index": 0,
    "progress": 0.0,
    "speed": 3.0,
    "color": tuple(int(tracer_feature["properties"]["route_color"][i:i+2], 16) for i in (0, 2, 4))
}

def update_tracer(tracer):
    points = tracer["points"]
    if len(points) < 2:
        return

    tracer["progress"] += tracer["speed"]

    # Get current segment length
    p1 = points[tracer["index"]]
    p2 = points[(tracer["index"] + 1) % len(points)]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    segment_length = math.sqrt(dx*dx + dy*dy)

    # Advance to next segment if past end
    if tracer["progress"] >= segment_length:
        tracer["progress"] -= segment_length
        tracer["index"] = (tracer["index"] + 1) % (len(points) - 1)

def get_tracer_pos(tracer):
    points = tracer["points"]
    p1 = points[tracer["index"]]
    p2 = points[(tracer["index"] + 1) % len(points)]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return p1
    t = tracer["progress"] / length
    x = p1[0] + dx * t
    y = p1[1] + dy * t
    return (int(x), int(y))


# Pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mercator Meter Mapping")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)

# Load basemap (EPSG:3857 from QGIS)
basemap = pygame.image.load("Maps/Basemap.png")

# Main loop
running = True
while running:
    screen.fill((0,0,0))
    #screen.blit(basemap, (MAP_X, MAP_Y))
    
    # Draw Stations using Lat/Lon
    for station_id, station in stations.items():
        x, y = gps_to_pixels(station["lat"], station["lon"])
        
        # Draw dot and label
        #pygame.draw.circle(screen, (255, 0, 0), (x, y), 3)
        #label = font.render(station_id, True, (0, 0, 0))
        #screen.blit(label, (x + 10, y - 10))

    for feature in routes_data["features"]:
        color_hex = feature["properties"]["route_color"]
        color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        for segment in feature["geometry"]["coordinates"]:
            points = [gps_to_pixels(lat, lon) for lon, lat in segment]
            if len(points) >= 2:
                pygame.draw.lines(screen, color, False, points, 4)

    update_tracer(tracer)
    x, y = get_tracer_pos(tracer)
    pygame.draw.circle(screen, tracer["color"], (x, y), 6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
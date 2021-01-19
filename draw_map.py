import pgzrun
import pygame
import csv
from pgzero.builtins import Actor, keyboard, Rect, mouse
from math import sqrt

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window
MAPPATH = 'maps/map.csv'

saving = False

wallImage = pygame.image.load("images/wall.png")
wallImageSize = 10
wallImage = pygame.transform.scale(wallImage, (wallImageSize, wallImageSize))


coords = []

def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    # screen.blit(wallImage, (0, 0))
    for coord in coords:
        draw_wall(coord)

def update():
    global coords
    if (keyboard.space):
        save_map(MAPPATH)

    if (keyboard.right):
        coords = read_map(MAPPATH)

def save_map(mapPath):
    global saving
    if (saving is not True):
        saving = True
        # prompt for file name?
        with open(mapPath, 'w', newline='') as f:
            csv_out = csv.writer(f)
            for row in coords:
                csv_out.writerow(row)
        saving = False

def read_map(mapPath):
    with open(mapPath, 'r') as f:
        reader = csv.reader(f)
        return [(int(row[0]), int(row[1])) for row in reader]

def draw_wall(pos):
    global wallImage
    screen.blit(wallImage, (pos))

def add_wall(pos):
    # check if coord overlaps with another coord in list
    placeWall = True
    for coord in coords:
        center_x = coord[0] + (wallImageSize/2)
        center_y = coord[1] + (wallImageSize/2)

        point_x = pos[0] + (wallImageSize/2)
        point_y = pos[1] + (wallImageSize/2)

        print(sqrt((point_x - center_x)**2 + (point_y - center_y)**2))
        print("point", (wallImageSize/2)**2)

        if(sqrt((point_x - center_x)**2 + (point_y - center_y)**2)<wallImageSize):
            print('in_circle')
            placeWall = False
            break
    
    if placeWall == True:
        print('appended')
        coords.append(pos)
    

def on_mouse_move(pos, rel, buttons):
    global coords
    if(mouse.LEFT in buttons):
        print("You clicked at", pos)
        add_wall(pos)

pgzrun.go()
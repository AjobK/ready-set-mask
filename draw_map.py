import pgzrun
import pygame
import csv
from pgzero.builtins import Actor, keyboard, Rect, mouse
from math import sqrt

class TriggerBox:
    x = 0
    y = 0
    width = 0
    height = 0
    color = (0,0,0)
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 100
        self.color = (200,0,0)

class CarSpawn:
    x = 0
    y = 0
    width = 0
    height = 0
    color = (0,0,0)
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (0, 200, 0)

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window
MAPPATH = 'maps/map.csv'

mousePos = (0, 0)
saving = False

wallImage = pygame.image.load("images/wall.png")
wallImageSize = 10
wallImage = pygame.transform.scale(wallImage, (wallImageSize, wallImageSize))

carSpawn = CarSpawn(0, 0)
triggerBox = TriggerBox(0, 0)
coords = []

def draw():
    global triggerBox
    screen.clear()
    screen.fill((255, 255, 255))
    # screen.blit(wallImage, (0, 0))
    if (triggerBox is not None):
        draw_finish((triggerBox.x, triggerBox.y))
    if (carSpawn is not None):
        draw_spawn((carSpawn.x, carSpawn.y))
    for coord in coords:
        draw_wall(coord)

def update():
    global mousePos
    global carSpawn
    global coords
    if (keyboard.space):
        save_map(MAPPATH)

    if (keyboard.right):
        read_map(MAPPATH)

    if (keyboard.left):
        carSpawn = CarSpawn(mousePos[0], mousePos[1])

def save_map(mapPath):
    global saving
    if (saving is not True):
        saving = True
        # prompt for file name?
        with open(mapPath, 'w', newline='') as f:
            csv_out = csv.writer(f)
            if(triggerBox is not None):
                csv_out.writerow(['TRIGGERBOX', triggerBox.x, triggerBox.y])

            if(carSpawn is not None):
                csv_out.writerow(['CARSPAWN', carSpawn.x, carSpawn.y])

            for row in coords:
                csv_out.writerow(row)

        saving = False

def read_map(mapPath):
    global triggerBox
    global carSpawn
    global coords
    with open(mapPath, 'r') as f:
        reader = csv.reader(f)
        firstLine = next(reader)
        if(firstLine[0] == 'TRIGGERBOX'):
            triggerBox = TriggerBox(int(firstLine[1]), int(firstLine[2]))
        secondLine = next(reader)
        if(secondLine[0] == 'CARSPAWN'):
            carSpawn = CarSpawn(int(secondLine[1]), int(secondLine[2]))
            
        coords = [(int(row[0]), int(row[1])) for row in reader]
    return triggerBox, carSpawn, coords

def draw_wall(pos):
    global wallImage
    screen.blit(wallImage, (pos))

def draw_finish(pos):
    global triggerBox
    screen.draw.rect(Rect((triggerBox.x,triggerBox.y),(triggerBox.width,triggerBox.height)), triggerBox.color)

def draw_spawn(pos):
    global carSpawn
    screen.draw.rect(Rect((carSpawn.x,carSpawn.y),(carSpawn.width,carSpawn.height)), carSpawn.color)

def add_wall(pos):
    # check if coord overlaps with another coord in list
    placeWall = True
    for coord in coords:
        center_x = coord[0] + (wallImageSize/2)
        center_y = coord[1] + (wallImageSize/2)

        point_x = pos[0] + (wallImageSize/2)
        point_y = pos[1] + (wallImageSize/2)

        if(sqrt((point_x - center_x)**2 + (point_y - center_y)**2)<wallImageSize):
            placeWall = False
            break
    
    if placeWall == True:
        coords.append(pos)
    
def on_mouse_move(pos, rel, buttons):
    global mousePos
    global coords
    
    mousePos = pos

    if(mouse.LEFT in buttons):
        add_wall(pos)

def on_mouse_down(pos, button):
    global triggerBox
    if(button == mouse.RIGHT):
        triggerBox = TriggerBox(pos[0], pos[1])

pgzrun.go()
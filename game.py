#!/usr/bin/python3
import pgzrun
import pygame
from detect_mask_video import MaskDetector
import threading
import math
import csv
from pgzero.builtins import Actor, keyboard, Rect, mouse
# import draw_map


WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window 

car = Actor("racecar2")
car.pos = 350, 560
speed = 2
direction_speed_multiplier = [0, 1]
gassing = False
velocity = 0
# TODO: Put direction in this variable
direction = None # should be "LEFT", "RIGHT" or None
triggerBoxes = []
carImage = pygame.image.load("images/racecar2.png")
wallImage = pygame.image.load("images/wall.png")
wallImage = pygame.transform.scale(wallImage, (10, 10))
walls = []
levelNumber = 1
pressingRestart = False
# surface = pygame.display.set_mode((400,300))

class TriggerBox:
    x = 0
    y = 0
    width = 0
    height = 0
    color = (0,0,0)
    def __init__(self,x,y,width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

def is_gassing():
    global gassing
    global direction;

    direction = md.detectHand()
    gassing = md.is_gassing()
    threading.Timer(0.3, is_gassing).start()

def draw():
    global gassing

    screen.fill((75, 156, 75)) # BG color
    car.draw()
    screen.draw.text("GASSING" if gassing else "REVERSE", (20, 20))
    screen.draw.text("STEERING " + ("STRAIGHT" if not direction else direction), (20, 45))
    screen.draw.text("PRESS R TO RESTART", (20, 70))
    # Chunky boi
    # if(len(triggerBoxes) == 0):
    #     # print('Creating triggerboxes')
    #     boxStraight = TriggerBox(250,100,200,100, (200,0,0))
    #     boxBottom = TriggerBox(250, 600, 200, 100,(200,0,0) )
    #     triggerBoxes.append(boxBottom)
    #     triggerBoxes.append(boxStraight)

    # print('Triggerboxes')
    # print(triggerBoxes)
    # boxStraight = triggerBoxes[0]
    # boxBottom = triggerBoxes[1]
    
    for triggerBox in triggerBoxes:
        screen.draw.rect(Rect((triggerBox.x,triggerBox.y),(triggerBox.width,triggerBox.height)), triggerBox.color)

    # if len(walls) == 0:
    #     counter = 5
    #     richting = True
    #     startY = 0
    #     stopY = 800
    #     stepSize = 10
    #     for y in range(startY,stopY,stepSize):
    #         rect = wallImage.get_rect()
    #         line1X = 275 - counter
    #         rect = rect.move((line1X, y))
    #         walls.append(rect)

    #         rect = wallImage.get_rect()
    #         line2X = 425 - counter
    #         rect = rect.move((line2X, y))
    #         walls.append(rect)

    #         if counter == 150:
    #             richting = False
    #         elif counter == 0:
    #             richting = True

    #         if richting:
    #             counter = counter + 5
    #         else: 
    #             counter = counter - 5
    drawWall()


def update(): 
    global gassing, speed, direction, velocity, WIDTH, HEIGHT, pressingRestart, levelNumber

    if (direction == "LEFT"):
        car.angle += 2 * abs(velocity) / speed
    if (direction == "RIGHT"):
        car.angle -= 2 * abs(velocity) / speed


    direction_speed_multiplier[0] = math.sin(math.radians(car.angle))
    direction_speed_multiplier[1] = math.cos(math.radians(car.angle))

    # print('KEY?')

    # Level restart
    if keyboard.K_r and not pressingRestart:
        pressingRestart = True
    elif not keyboard.K_r and pressingRestart:
        pressingRestart = False
        read_map('./maps/level_' + str(levelNumber) + '.csv')


    if gassing:
        velocity = velocity - 0.075

        if (velocity <= -speed):
            velocity = -speed
    else:
        velocity = velocity + 0.075

        if (velocity >= speed):
            velocity = speed

    new_pos = (car.pos[0] + direction_speed_multiplier[0] * (velocity), car.pos[1] + direction_speed_multiplier[1] * velocity)

    collision = checkCollision(new_pos, direction_speed_multiplier)

    # Basic edge collision detection
    if (new_pos[0] <= 25 or new_pos[0] >= WIDTH-25 or new_pos[1] <= 25 or new_pos[1] >= HEIGHT-25) or not collision:
        velocity = 0

    car.pos = (car.pos[0] + direction_speed_multiplier[0] * (velocity), car.pos[1] + direction_speed_multiplier[1] * velocity)

def drawWall():
    global wallImage, walls
    # print('Gonna draw wall now')
    for wall in walls: 
        screen.blit(wallImage, wall)

def checkCollision(pos, angle):
    global levelNumber

    for triggerBox in triggerBoxes:
        if triggerBox.x  < pos[0]-15 and triggerBox.x + triggerBox.width > pos[0]-15 and triggerBox.y < pos[1]-15 and triggerBox.y  + triggerBox.height > pos[1]-15:
            levelNumber += 1
            read_map('./maps/level_' + str(levelNumber) + '.csv')
            triggerBox.color = (0, 255, 0)
        
    return checkWallCollision(pos,angle)

def checkWallCollision(pos, angle):
    global carImage

    driving = True
    carWidth = carImage.get_width()
    carHeith = carImage.get_height()
    carCollionBox = [carWidth*abs(angle[0])+carWidth,(carHeith*abs(angle[1])+carHeith)/2]

    startX = int(math.floor(pos[0]-carCollionBox[0]/2))
    startY = round(pos[1]-carCollionBox[1]/2)
    endX = round(startX+carCollionBox[0])
    endY = round(startY+carCollionBox[1])
    
    topX = 22 * math.sin(math.radians(car.angle))
    topY = 22 * math.cos(math.radians(car.angle))
    for wall in walls:
        wallLeft = wall.centerx - 5
        wallRight = wall.centerx + 5
        wallTop = wall.centery - 5
        wallBottom = wall.centery + 5
        if(startX < wallRight and
            endX > wallLeft and
            startY < wallBottom and 
            endY > wallTop
            ):
            for x in range(int(carWidth/2)):
                if(not gassing):
                    lineTopX = car.centerx + topX - x * (math.sin(math.radians(car.angle+90)))
                    lineTopY = car.centery + topY - x * (math.cos(math.radians(car.angle+90)))
                    lineTopX2 = car.centerx + topX + x * (math.sin(math.radians(car.angle+90)))
                    lineTopY2 = car.centery + topY + x * (math.cos(math.radians(car.angle+90)))
                    if(lineTopX < wallRight and
                        lineTopX > wallLeft and
                        lineTopY < wallBottom and 
                        lineTopY > wallTop):
                        driving = False
                    if(lineTopX2 < wallRight and
                        lineTopX2 > wallLeft and
                        lineTopY2 < wallBottom and 
                        lineTopY2 > wallTop):
                        driving = False
                else:
                    lineBottomX = car.centerx - topX - x * (math.sin(math.radians(car.angle+90)))
                    lineBottomY = car.centery - topY - x * (math.cos(math.radians(car.angle+90)))
                    lineBottomX2 = car.centerx - topX + x * (math.sin(math.radians(car.angle+90)))
                    lineBottomY2 = car.centery - topY + x * (math.cos(math.radians(car.angle+90)))
                    if(lineBottomX < wallRight and
                        lineBottomX > wallLeft and
                        lineBottomY < wallBottom and 
                        lineBottomY > wallTop):
                        driving = False
                    if(lineBottomX2 < wallRight and
                        lineBottomX2 > wallLeft and
                        lineBottomY2 < wallBottom and 
                        lineBottomY2 > wallTop):
                        driving = False
    # print(driving)
    return driving

def read_map(mapPath):
    global triggerBoxes, velocity, walls

    velocity = 0
    triggerBoxes = []
    walls = []

    triggerBox = None
    coords = None
    with open(mapPath, 'r') as f:
        reader = csv.reader(f)
        firstLine = next(reader)
        if(firstLine[0] == 'TRIGGERBOX'):
            triggerBoxes.append(TriggerBox(int(firstLine[1]), int(firstLine[2]), 100, 100, (200, 0, 0)))
        secondLine = next(reader)
        if(secondLine[0] == 'CARSPAWN'):
            car.pos = (int(secondLine[1]), int(secondLine[2]))
            
        coords = [(int(row[0]), int(row[1])) for row in reader]

        for coord in coords:
            rect = wallImage.get_rect()
            rect = rect.move(coord)
            walls.append(rect)

md = MaskDetector()

read_map('./maps/level_' + str(levelNumber) + '.csv')

# recurrent
is_gassing()

pgzrun.go()


#!/usr/bin/python3
import pgzrun
import pygame
from detect_mask_video import MaskDetector
import threading
import math

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window 

car = Actor("racecar2")
car.pos = 350, 560
speed = 2
direction_speed_multiplier = [0, 1]
gassing = False
# TODO: Put direction in this variable
direction = None # should be "LEFT", "RIGHT" or None

def is_gassing():
    global gassing

    gassing = md.is_gassing()
    threading.Timer(0.3, is_gassing).start()

def draw():
    global gassing

    screen.fill((75, 156, 75)) # BG color
    car.draw()
    screen.draw.text("GASSING" if gassing else "REVERSE", (20, 20))
    screen.draw.text("STEERING " + ("STRAIGHT" if not direction else direction), (20, 45))

def update(): 
    global gassing, speed, WIDTH, HEIGHT

    # Attempt to rotation using sine and cosine
    # print(car.angle)

    # if (keyboard.left):
    #     car.angle += 1
    # elif (keyboard.right):
    #     car.angle -= 1

    # direction_speed_multiplier[0] = math.cos(car.angle / 50)
    # direction_speed_multiplier[1] = math.sin(car.angle / 50)

    if gassing and car.y + speed > 0: car.y -= speed * direction_speed_multiplier[1]
    elif car.y - speed < HEIGHT: car.y += speed * direction_speed_multiplier[1]

    car.x += direction_speed_multiplier[0] * speed

md = MaskDetector()

# recurrent
is_gassing()

pgzrun.go()

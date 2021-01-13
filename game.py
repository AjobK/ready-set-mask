#!/usr/bin/python3
import pgzrun
import pygame
from detect_mask_video import MaskDetector
import threading
import math
from pgzero.builtins import Actor, keyboard

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window 

car = Actor("racecar2")
car.pos = 350, 560
speed = 3
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
    global gassing, speed, direction, WIDTH, HEIGHT

    if (keyboard.right != keyboard.left):
        if (keyboard.left):
            car.angle += 2
            direction = "LEFT"

        if (keyboard.right):
            car.angle -= 2
            direction = "RIGHT"
    else:
        direction = "STRAIGHT"

    direction_speed_multiplier[0] = math.sin(math.radians(car.angle))
    direction_speed_multiplier[1] = math.cos(math.radians(car.angle))

    if gassing:
        car.pos = (car.pos[0] - direction_speed_multiplier[0] * speed, car.pos[1] - direction_speed_multiplier[1] * speed)
    else:
        car.pos = (car.pos[0] + direction_speed_multiplier[0] * speed, car.pos[1] + direction_speed_multiplier[1] * speed)

md = MaskDetector()
# recurrent
is_gassing()

pgzrun.go()

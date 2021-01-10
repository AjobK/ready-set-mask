#!/usr/bin/python3
import pgzrun
import pygame
from detect_mask_video import MaskDetector
import threading

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window 

car = Actor("racecar2")
car.pos = 350, 560
speed = 2
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

    if gassing and car.y + speed > 0: car.y -= speed
    elif car.y - speed < HEIGHT: car.y += speed

md = MaskDetector()

# recurrent
is_gassing()

pgzrun.go()

#!/usr/bin/python3
import pgzrun
from detect_mask_video import MaskDetector
import threading

WIDTH = 700 # width of the window
HEIGHT = 800 # height of the window 

car = Actor("racecar2")
car.pos = 350, 560
speed = 2
gassing = False

def is_gassing():
    global gassing
    gassing = md.is_gassing()
    threading.Timer(0.3, is_gassing).start()

def draw():
    screen.fill((75, 156, 75)) # BG color
    car.draw()

def update(): 
    global gassing, speed

    if gassing: car.y -= speed
    else: car.y += speed

md = MaskDetector()

# recurrent
is_gassing()

pgzrun.go()

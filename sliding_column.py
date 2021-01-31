#!/usr/bin/env python3

import time
import math
import random
from gpiozero import Button

from unicornhatmini import UnicornHATMini
from colorsys import hsv_to_rgb

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.2)
unicornhatmini.set_rotation(180)
width, height = unicornhatmini.get_shape()


def grid_init():
    grid = {(x,y): just_one() for x in range(width) for y in range(height)}
    return grid

def just_one():
    number = random.randrange(3)
    if number == 0:
        return [255,0,0]
    if number == 1:
        return [0,0,0]
        #return [0,255,0]
    if number == 2:
        return [0,0,255]


def grid_iter(grid):
    new_grid = {}
    for x in range(width):
        for y in range(height):
            if x == 0:
                new_grid[(x,y)] = just_one()
            else:
                new_grid[(x,y)] = grid[(x-1,y)]
    return new_grid

def show_grid(grid):
    for x in range(width):
        for y in range(height):
            unicornhatmini.set_pixel(x, y, *grid[(x, y)])
            unicornhatmini.show()


def main():
    grid = grid_init()
    while True:
        show_grid(grid)
        grid = grid_iter(grid)
        time.sleep(1/600)


try: 
    main()
except KeyboardInterrupt:
    print("Exiting")

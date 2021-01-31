#!/usr/bin/env python3

import time
import math
import random
from gpiozero import Button

from unicornhatmini import UnicornHATMini
from colorsys import hsv_to_rgb

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.2)
#unicornhatmini.set_rotation(180)
width, height = unicornhatmini.get_shape()

cell = [122,122,0]
space = [0,0,0]

# Each square's neighbour coordinates
area = ((-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1))

def grid_init():
    grid = {(x,y): (cell if random.random() <= .25 else space) for x in range(width) for y in range(height)}
    return grid

def grid_iter(grid):
    new_grid = {}
    for x in range(width):
        for y in range(height):
            count = 0
            for dx, dy in area:
                if grid.get((x + dx, y + dy), space) == cell:
                    count += 1

            if grid[(x,y)] == cell:
                if count < 2:
                    new_grid[(x,y)] = space
                elif count > 4:
                    new_grid[(x,y)] = space
                else:
                    new_grid[(x,y)] = cell
            if grid[(x,y)] == space:
                if count == 3:
                    new_grid[(x,y)] = cell

    return new_grid

def show_grid(grid):
    unicornhatmini.clear()
    for x in range(width):
        for y in range(height):
            unicornhatmini.set_pixel(x, y, *grid[(x, y)])
    unicornhatmini.show()

def print_grid(grid):
    print(grid)
def main():
    grid = grid_init()
    while True:
        print_grid(grid)
        show_grid(grid)
        grid = grid_iter(grid)
        time.sleep(1/600)


try: 
    main()
except KeyboardInterrupt:
    print("Exiting")

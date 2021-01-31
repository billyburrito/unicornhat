#!/usr/bin/env python3

# Forest fire model cellular automaton. Simulates the growth
# of trees in a forest, with sporadic outbreaks of forest fires.

# https://en.wikipedia.org/wiki/Forest-fire_model

# Based on Rosetta Code Python Forest Fire example.
# https://rosettacode.org/wiki/Forest_fire#Python

import random
import time

from unicornhatmini import UnicornHATMini

print("""
Unicorn HAT Mini: The game of life

Press Ctrl+C to exit!
""")


# Avoid retina-searage!
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
unicornhatmini.set_rotation(0)

# The height and width of the forest.
width, height = unicornhatmini.get_shape()

# Initial probability of a grid square having a tree
initial_life = 0.15

# p = probability of life growing, f = probability of fire
p = 0.0001
f = 0.0005

# Brightness values for a tree, fire, and blank space
life = [100, 0, 0]
burning = [255, 0, 0]
space = [10, 10, 10]

# Each square's neighbour coordinates
hood = ((-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1))


# Function to populate the initial forest
def initialise():
    grid = {(x, y): (life if random.random() <= initial_life else space) for x in range(width) for y in range(height)}
    return grid


# Display the forest, in its current state, on UnicornHATMini
def show_grid(grid):
    unicornhatmini.clear()
    for x in range(width):
        for y in range(height):
            unicornhatmini.set_pixel(x, y, *grid[(x, y)])
    unicornhatmini.show()


# Go through grid, update grid squares based on state of
# square and neighbouring squares
def update_grid(grid):
    new_grid = {}
    for x in range(width):
        for y in range(height):
            count = 0
            for dx, dy in hood:
                if grid.get((x + dx, y + dy), space) == life:
                    count += 1
            #print(x,y,count)

            if grid[(x,y)] == life:
                if count < 2:
                    new_grid[(x,y)] = space
                elif count > 4:
                    new_grid[(x,y)] = space
                else:
                    new_grid[(x,y)] = life
            if grid[(x,y)] == space:
                if count == 3:
                    new_grid[(x,y)] = life
                else:
                    new_grid[(x,y)] = space
		

    #print (new_grid)
    return new_grid


# Main function. Initialises grid, then shows, updates, and
# waits for 1/60 of a second.
def main():
    grid = initialise()
    cycles = 0
    while True:
        show_grid(grid)
        new_grid = update_grid(grid)
        if (new_grid == grid):
            grid = initialise()
            cycles = 0
        else:
            grid = new_grid
            cycles += 1
        if (cycles > 500):
            print("limit reached")
            cycles = 0
            grid = initialise()
        time.sleep(1 / 6.0)


# Catches control-c and exits cleanly
try:
    main()

except KeyboardInterrupt:
    print("Exiting")

# FIN!

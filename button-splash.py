#!/usr/bin/env python3

import time
import math
from gpiozero import Button

from unicornhatmini import UnicornHATMini
from colorsys import hsv_to_rgb


print("""Unicorn HAT Mini: buttons.py

Demonstrates the use of Unicorn HAT Mini's buttons with gpiozero.

Splashes a rainbow across the screen, originating at the pressed button.

Press Ctrl+C to exit!

""")


unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.5)
unicornhatmini.set_rotation(0)
width, height = unicornhatmini.get_shape()


splash_origin = (0, 0)
splash_time = 0


def pressed(button):
    global splash_origin, splash_time
    button_name, x, y = button_map[button.pin.number]
    splash_origin = (x, y)
    splash_time = time.time()
    print(f"Button {button_name} pressed!")


button_map = {5: ("A", 0, 0),    # Top Left
              6: ("B", 0, 6),    # Bottom Left
              16: ("X", 16, 0),  # Top Right
              24: ("Y", 16, 7)}  # Bottom Right

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)


def distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


try:
    button_a.when_pressed = pressed
    button_b.when_pressed = pressed
    button_x.when_pressed = pressed
    button_y.when_pressed = pressed

    while True:
        if splash_time > 0:
            splash_x, splash_y = splash_origin
            splash_progress = time.time() - splash_time
            for x in range(width):
                for y in range(height):
                    d = distance(x, y, splash_x, splash_y)
                    if (d / 30.0) < splash_progress and splash_progress < 0.6:
                        h = d / 17.0
                        r, g, b = [int(c * 255) for c in hsv_to_rgb(h, 1.0, 1.0)]
                        unicornhatmini.set_pixel(x, y, r, g, b)
                    elif (d / 30.0) < splash_progress - 0.6:
                        unicornhatmini.set_pixel(x, y, 0, 0, 0)

        unicornhatmini.show()

        time.sleep(.1/ 60.0)

except KeyboardInterrupt:
    button_a.close()
    button_b.close()
    button_x.close()
    button_y.close()

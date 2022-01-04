# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


pixel_pin = board.D21
num_pixels = 7
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

# Red Ring
loopcount = range(3)
pixring = range(1,num_pixels)
for n in loopcount:
    for i in pixring:
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.075)
        pixels[i] = (0, 0, 0)

# Green Ring
loopcount = range(3)
pixring = range(1,num_pixels)
for n in loopcount:
    for i in pixring:
        pixels[i] = (0, 255, 0)
        pixels.show()
        time.sleep(0.075)
        pixels[i] = (0, 0, 0)

# Blue Ring
loopcount = range(3)
pixring = range(1,num_pixels)
for n in loopcount:
    for i in pixring:
        pixels[i] = (0, 0, 255)
        pixels.show()
        time.sleep(0.075)
        pixels[i] = (0, 0, 0)

# Pixels Off
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)

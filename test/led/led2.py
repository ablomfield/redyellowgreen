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


def rainbow_cycle(wait):
    for j in range(255):
            pixel_index = (i * 256 // num_pixels) + j


# Pixels White
pixels.fill((255, 255, 255))
pixels.show()
time.sleep(1)

# Red Ring
loopcount = range(10)
pixring = range(1,num_pixels)
for n in loopcount:
    for i in pixring:
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.05)
        pixels[i] = (255, 255, 255)

# Pixels Off
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)


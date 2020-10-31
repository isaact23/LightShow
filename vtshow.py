#!/user/bin/env python

import time
from time import sleep
import random
import colorsys # HSV to RGB
import board # GPIO
import neopixel # Set LED values

# Colors
DARK_RED = (80, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 70, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 80, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
DARK_BLUE = (0, 0, 80)
BLUE = (0, 0, 255)
PURPLE = (80, 0, 255)
MAGENTA = (255, 0, 255)
PINK = (255, 0, 80)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF = (0, 0, 0)
BLACK = (0, 0, 0)

VT = (RED, ORANGE)

USA = (RED, WHITE, BLUE, OFF)
GERMANY = (OFF, RED, YELLOW)
MEXICO = (DARK_GREEN, WHITE, RED) # Also Italy
SPAIN = (RED, (100, 100, 0), RED)
INDIA = (ORANGE, WHITE, DARK_GREEN)
CHINA = (RED, YELLOW)

corner = 125 # Corner point pixel no.
size = 150
pixels = neopixel.NeoPixel(board.D18, size, auto_write=False)

# Input is normalized (1, 1, 1), output is not (255, 255, 255)
def hsv2rgb(h, s, v):
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Set all lights to one color.
def fill(color):
	pixels.fill(color)
	pixels.write()

# Turn off all lights.
def turnOff():
	pixels.fill(OFF)
	pixels.write()

# Alternate the entire strip between multiple colors.
def blink(colors=(RED, OFF), times=3, sec=0.2):
	for i in range(times):
		for color in colors:
			fill(color)
			sleep(sec)

# Generate a random color.
def randomColor():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Generate a random fully-saturated color.
def randomHue():
	return hsv2rgb(random.random(), 1, 1)

# Set each LED to a random color.
def random_colors():
	for i in range(size):
		pixels[i] = randomColor()
	pixels.write()

# Send rainbow of colors to LED.
def rainbow(shift=0, frequency=2, sat=1, vis=1):
	for i in range(size):
		pixels[i] = hsv2rgb((i + shift) * frequency / 255, sat, vis)
	pixels.write()

# Call rainbow multiple times, shifting over time.
def movingRainbow(sec=5, speed=1, frequency=2, sat=1, vis=1):
	startTime = time.time()
	shift=0
	while (time.time() - startTime < sec):
		rainbow(shift=shift, frequency=frequency, sat=sat, vis=vis)
		shift = shift + speed
		sleep(0.01)
		
# Move through RGB spectrum, with entire strip the same color at one time.
def solidRainbow(times=1, speed=1, sat=1, vis=1):
	frameCount = round(100 / speed)
	for i in range(times):
		for frame in range(frameCount):
			fill(hsv2rgb(frame / frameCount, sat, vis))
			sleep(0.01)

# Transpose from a solid color to a rainbow.
def solidToRainbow(startHue=0, speed=1, frequency=2, sat=1, vis=1):
	startTime = time.time()
	frameCount = round(100 / speed)
	for frame in range(frameCount):
		ratio = frame / frameCount
		for i in range(size):
			pixels[i] = hsv2rgb(((startHue / 255) * (1 - ratio)) +
								(((i * frequency) / 255) * ratio), sat, vis)
		pixels.write()

# Move one color in staggered gradients down the strip.
def icicle(sec=5, speed=1, width=10, color=CYAN):
	startTime = time.time()
	shift = 0
	while(time.time() - startTime < sec):
		for i in range(size):
			factor = (((i + shift / 5) % width) / width) ** 4
			pixels[i] = (int(color[0] * factor), int(color[1] * factor), int(color[2] * factor))
		pixels.write()
		shift += speed
		sleep(0.01)

# Send multiple color stripes down the strip.
def multiStripe(sec=5, speed=1, width=10, colors=(RED, GREEN, BLUE)):
	startTime = time.time()
	shift = 0
	while(time.time() - startTime < sec):
		for i in range(size):
			pixels[i] = colors[round((i + shift) / width) % len(colors)]
		pixels.write()
		shift = shift + speed
		sleep(0.01)	

# Send stripes down the strip to fill it up.
def tetris(width=5, onColor=RED, offColor=GRAY, doBlink=False):
	pixelsRemaining = size
	fill(offColor)
	for unit in range((size // width) + 1):
		for i in range(pixelsRemaining):
			if i >= width:
				pixels[i - width] = offColor
			pixels[i] = onColor
			pixels.write()
			sleep(0.01)
		pixelsRemaining -= width
	if doBlink:
		blink(colors=(onColor, offColor), times=3, sec=0.4)

# Run tetris with random settings
def randomTetris():
	COLOR = randomHue()
	COLOR2 = randomHue()
	WIDTH = random.randint(5, 25)
	tetris(width=WIDTH, onColor=COLOR, offColor=COLOR2)

# Fill a range with specified color.
def fillRange(start=0, end=150, color=RED):
	for i in range(start, end):
		pixels[i % size] = color
	pixels.write()

# Have stripes explode from the specified point.
def explodeFromPoint(corner=0, color=RED, count=1, fillTime = 1):
	for i in range(count):
		startTime = time.perf_counter()
		dist = 0
		while dist < size / 2:
			dist = int(0.5 * size * (time.perf_counter() - startTime) / fillTime)
			fillRange(corner - dist, corner + dist, color)
			sleep(0.01)
		if color != OFF:
			explodeFromPoint(corner, color=OFF, fillTime=fillTime)

#explodeFromPoint(corner, ORANGE, count=10, fillTime=0.8)
#multiStripe(sec=8,speed=0.5,colors=VT,width=10)
#icicle(8, color=RED)

turnOff()

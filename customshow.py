#!/user/bin/env python

import time
from time import sleep
import random
import colorsys # HSV to RGB
import board # GPIO
import neopixel # Set LED values

DARK_RED = (80, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 80, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
DARK_BLUE = (0, 0, 80)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF = (0, 0, 0)

USA = (RED, WHITE, BLUE, OFF)
GERMANY = (OFF, RED, YELLOW)
MEXICO = (DARK_GREEN, WHITE, RED) # Also Italy
SPAIN = (RED, (100, 100, 0), RED)
INDIA = (ORANGE, WHITE, DARK_GREEN)

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

# Fill all of the lights several different colors in sequence.
def fillTest():
	fill(RED)
	sleep(1)
	fill(YELLOW)
	sleep(1)
	fill(GREEN)
	sleep(1)
	fill(CYAN)
	sleep(1)
	fill(BLUE)
	sleep(1)
	fill(MAGENTA)
	sleep(1)

# Like fillTest, but turn lights off in between each color.
def blinkTest():
	fill(RED)
	sleep(0.2)
	turnOff()
	sleep(0.2)
	fill(YELLOW)
	sleep(0.2)
	turnOff()
	sleep(0.2)
	fill(GREEN)
	sleep(0.2)
	turnOff()
	sleep(0.2)
	fill(CYAN)
	sleep(0.2)
	turnOff()
	sleep(0.2)
	fill(BLUE)
	sleep(0.2)
	turnOff()
	sleep(0.2)
	fill(MAGENTA)
	sleep(0.2)

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
def tetris(width=5, onColor=RED, offColor=GRAY, doBlink=True):
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

def show1():
	movingRainbow(sec=5, speed=5, frequency=3, sat=1, vis=1)
	multiStripe(sec=5)
	movingRainbow(sec=5, speed=10, frequency=6, sat=1, vis=1)
	multiStripe(sec=5, colors=(CYAN, YELLOW))
	movingRainbow(sec=5, speed=2, frequency=1, sat=0.5, vis=1)
	blinkTest()
	turnOff()

def show2():
	movingRainbow(frequency=1, sec=10)
	multiStripe(sec=10, speed=1, width=5, colors=(RED, WHITE, BLUE))
	blink(colors=(RED, WHITE, BLUE), times=3)
	icicle(sec=10)
	tetris(width=8, onColor=BLUE, offColor=OFF)
	
def BLIPPISHOW(sec=10):
	multiStripe(sec=sec,width=10,speed=1,colors=(ORANGE,BLUE))
	movingRainbow(sec=sec,frequency=5)
	multiStripe(sec=sec,width=10,speed=1,colors=(RED,BLUE))
	movingRainbow(sec=sec,frequency=5,vis=0.2)
	tetris(onColor=ORANGE,offColor=BLUE)
	
def patrioticShow():
	for j in range(3):
		for i in range(0, 255, 25):
			fill((255, i, i))
			sleep(0.01)
		for i in range(255, 0, -25):
			fill((i, i, 255))
			sleep(0.01)
	
	blink(colors=(RED, OFF, WHITE, OFF, BLUE, OFF), times=2, sec=0.5)
	
	multiStripe(sec=5, speed=1, width=15, colors=(RED, WHITE, BLUE))
	
	for j in range(5):
		for i in range(0, 255, 50):
			fill((255, i, i))
			sleep(0.01)
		for i in range(255, 0, -50):
			fill((i, i, 255))
			sleep(0.01)
	
	blink(colors=(RED, OFF, WHITE, OFF, BLUE, OFF), times=4, sec=0.2)
	
	multiStripe(sec=5, speed=3, width=8, colors=(RED, WHITE, BLUE))
	
	for j in range(8):
		for i in range(0, 255, 80):
			fill((255, i, i))
			sleep(0.01)
		for i in range(255, 0, -80):
			fill((i, i, 255))
			sleep(0.01)
	
	blink(colors=(RED, OFF, WHITE, OFF, BLUE, OFF), times=6, sec=0.1)
	
	multiStripe(sec=4, speed=10, width=3, colors=(RED, WHITE, BLUE))

#movingRainbow(sec=12,frequency=10,vis=1,sat=1)
#BLIPPISHOW()

#show2()
#icicle(sec=10, speed=10, width=60)

#blink()
#multiStripe(sec=60, width=5, speed=2, colors=(RED, WHITE, BLUE))
#patrioticShow()

turnOff()

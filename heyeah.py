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

tempo = 140
size = 150
pixels = neopixel.NeoPixel(board.D18, size, auto_write=False)

# Input is normalized (1, 1, 1), output is not (255, 255, 255)
def hsv2rgb(h, s, v):
	return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Set all lights to one color.
def fill(color):
	pixels.fill(color)

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

# Set LED strip to rainbow.
def rainbow(shift=0, frequency=2, sat=1, vis=1):
	for i in range(size):
		pixels[i] = hsv2rgb((i + shift) * frequency / 255, sat, vis)
	pixels.write()

# Multiple colors in series.
def multiStripe(shift=0, speed=1, width=10, colors=(RED, GREEN, BLUE)):
	for i in range(size):
		pixels[i] = colors[round((i + shift) / width) % len(colors)]
	pixels.write()

# Fill a range with specified color.
def fillRange(start=0, end=150, color=RED):
	for i in range(start, end):
		pixels[i % size] = color
	pixels.write()

# Start show
beat = 0 # Beat count from start
startTime = time.time()
while beat < 296:
	beat = ((time.time() - startTime) * tempo) / 60
	if beat < 8: # For 8 beats
		fillRange(end=round((beat/8)*size), color=YELLOW)
	elif beat < 23: # 15 beats
		if beat % 2 < 0.5:
			multiStripe(colors=(YELLOW,OFF))
		elif beat % 2 < 1 or beat % 2 >= 1.5:
			fill(OFF)
			pixels.write()
		else:
			multiStripe(colors=(OFF, YELLOW))
	elif beat < 26: # 3 beats
		fill(OFF)
		fillRange(int(75 - (75 * (beat % 1))), int(75 + (75 * (beat % 1))))
	elif beat < 36: # 10 beats
		if beat % 2 < 0.5:
			fill(BLUE)
		elif beat % 2 < 1:
			fill(RED)
		elif beat % 2 < 1.5:
			fill(YELLOW)
		else:
			fill(GREEN)
		pixels.write()
	elif beat < 40: # 4 beats
		fill(OFF)
		fillRange(end=round(((beat-36) / 4) * size), color=YELLOW)
	elif beat < 56: # 16 beats
		if beat % 4 < 0.5:
			multiStripe(colors=(RED, WHITE, BLUE))
		elif beat % 4 < 1:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 1.5:
			multiStripe(colors=(WHITE, OFF))
		elif beat % 4 < 2:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 2.5:
			multiStripe(colors=(GREEN, BLUE, MAGENTA))
		elif beat % 4 < 3:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 3.5:
			multiStripe(colors=(ORANGE, BLUE))
		else:
			fill(OFF)
			pixels.write()
	elif beat < 68: # 12 beats
		if beat % 4 < 0.5:
			multiStripe(colors=(RED, YELLOW, ORANGE, OFF))
		elif beat % 4 < 1:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 1.5:
			multiStripe(colors=(RED, YELLOW, ORANGE, OFF))
		elif beat % 4 < 2:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 2.5:
			multiStripe(colors=(GREEN, MAGENTA, BLUE, OFF))
		elif beat % 4 < 3:
			fill(OFF)
			pixels.write()
		elif beat % 4 < 3.5:
			multiStripe(colors=(GREEN, MAGENTA, BLUE, OFF))
		else:
			fill(OFF)
			pixels.write()
	elif beat < 72: # 4 beats
		fill(OFF)
		fillRange(end=round(((beat-68) / 4) * size), color=YELLOW)
	elif beat < 88: # 16 beat chorus
		rainbow(shift=beat*20)
	elif beat < 100: # 12 beats
		if beat % 4 < 0.5:
			fill(OFF)
			fillRange(start=0,end=int(size/2),color=RED)
		elif beat % 4 < 0.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 1.25:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 1.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 2:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 2.5:
			fill(OFF)
			fillRange(start=int(size/2),end=size, color=RED)
		elif beat % 4 < 2.75:
			fillRange(start=int(size/2),end=size, color=YELLOW)
		elif beat % 4 < 3.25:
			fillRange(start=int(size/2),end=size, color=RED)
		elif beat % 4 < 3.75:
			fillRange(start=int(size/2),end=size, color=YELLOW)
		elif beat % 4 < 4:
			fillRange(start=int(size/2),end=size, color=RED)
	elif beat < 104: # 4 beats
		fill(OFF)
		fillRange(end=round(((beat - 100) / 4) * size), color=YELLOW)
	elif beat < 120: # 16 beat chorus
		rainbow(shift=beat * 20)
	elif beat < 128: # 8 beats
		if beat % 4 < 0.5:
			fill(OFF)
			fillRange(start=0,end=int(size/2),color=RED)
		elif beat % 4 < 0.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 1.25:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 1.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 2:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 2.5:
			fill(OFF)
			fillRange(start=int(size/2),end=size, color=RED)
		elif beat % 4 < 2.75:
			fillRange(start=int(size/2),end=size, color=YELLOW)
		elif beat % 4 < 3.25:
			fillRange(start=int(size/2),end=size, color=RED)
		elif beat % 4 < 3.75:
			fillRange(start=int(size/2),end=size, color=YELLOW)
		elif beat % 4 < 4:
			fillRange(start=int(size/2),end=size, color=RED)
	elif beat < 136: # 8 beats
		fill(OFF)
		fillRange(end=round(((beat - 128) / 8) * size), color=BLUE)
	elif beat < 152: # 16 beats
		multiStripe(shift=beat*10,width=10,colors=(BLUE, DARK_BLUE, GREEN, DARK_GREEN))
	elif beat < 160:  # 8 beats
		multiStripe(shift=beat * 10, width=10, colors=(DARK_BLUE, PURPLE, MAGENTA, PINK))
	elif beat < 168: # 8 beats
		multiStripe(shift=beat * 10, width=10, colors=(ORANGE, RED, MAGENTA, PINK))
	elif beat < 184: # 16 beats
		if beat % 2 < 0.5:
			multiStripe(colors=(ORANGE,OFF))
		elif beat % 2 < 1 or beat % 2 >= 1.5:
			fill(OFF)
			pixels.write()
		else:
			multiStripe(colors=(OFF, ORANGE))
	elif beat < 196: # 12 beats
		if beat % 2 < 0.5:
			multiStripe(colors=(YELLOW,OFF,RED,OFF))
		elif beat % 2 < 1 or beat % 2 >= 1.5:
			fill(OFF)
			pixels.write()
		else:
			multiStripe(colors=(OFF,RED,OFF,YELLOW))
	elif beat < 200:  # 4 beats
		fill(OFF)
		fillRange(end=round(((beat - 196) / 4) * size), color=YELLOW)
	elif beat < 216: # 16 beats
		rainbow(shift=beat * 20)
	elif beat < 228:  # 12 beats
		if beat % 4 < 0.5:
			fill(OFF)
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 0.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 1.25:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 1.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 2:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 2.5:
			fill(OFF)
			fillRange(start=int(size / 2), end=size, color=RED)
		elif beat % 4 < 2.75:
			fillRange(start=int(size / 2), end=size, color=YELLOW)
		elif beat % 4 < 3.25:
			fillRange(start=int(size / 2), end=size, color=RED)
		elif beat % 4 < 3.75:
			fillRange(start=int(size / 2), end=size, color=YELLOW)
		elif beat % 4 < 4:
			fillRange(start=int(size / 2), end=size, color=RED)
	elif beat < 232:  # 4 beats
		fill(OFF)
		fillRange(end=round(((beat - 228) / 4) * size), color=YELLOW)
	elif beat < 248: # 16 beats
		rainbow(shift=beat * 20)
	elif beat < 256: # 8 beats
		multiStripe(shift=beat*10, colors=(RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,PINK),width=15)
	elif beat < 264: # 8 beats
		multiStripe(shift=beat*10, colors=(RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,PINK),width=5)
	elif beat < 276: # 12 beats
		multiStripe(shift=beat*5, colors=(WHITE, GRAY),width=30,speed=0.5)
	elif beat < 280: # 4 beats
		multiStripe(shift=beat*30, colors=(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK), width=10)
	elif beat < 292: # 12 beats
		if beat % 4 < 0.5:
			fill(OFF)
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 0.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 1.25:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 1.75:
			fillRange(start=0, end=int(size / 2), color=YELLOW)
		elif beat % 4 < 2:
			fillRange(start=0, end=int(size / 2), color=RED)
		elif beat % 4 < 2.5:
			fill(OFF)
			fillRange(start=int(size / 2), end=size, color=RED)
		elif beat % 4 < 2.75:
			fillRange(start=int(size / 2), end=size, color=YELLOW)
		elif beat % 4 < 3.25:
			fillRange(start=int(size / 2), end=size, color=RED)
		elif beat % 4 < 3.75:
			fillRange(start=int(size / 2), end=size, color=YELLOW)
		elif beat % 4 < 4:
			fillRange(start=int(size / 2), end=size, color=RED)
	elif beat < 296: # 4 beats
		fill(OFF)
		fillRange(end=round(((beat - 292) / 4) * size), color=GREEN)

turnOff()

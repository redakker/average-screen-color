# Author: redakker 
# email: redman at redman dot hu

from PIL import ImageGrab
import time
import os
from colour import Color


# Config
LOOP_INTERVAL  = 3    # how often we calculate screen colour (in seconds)
DURATION       = 3    # how long it takes bulb to switch colours (in seconds)
SKIP_PIXELS       = 10   # skip every SKIP_PIXELS number of pixels to speed up calculation




# run loop
while True:
	
	red   = 0
	green = 0
	blue  = 0
	
	time.sleep(LOOP_INTERVAL) #calm down little bit
	
	# Calculate the average color
	image = ImageGrab.grab()  # take a screenshot
	
	for y in range(0, image.size[1], SKIP_PIXELS):  #loop over the height
		for x in range(0, image.size[0], SKIP_PIXELS):  #loop over the width
			
			color = image.getpixel((x, y))  #grab a pixel
			# calculate sum of each component (RGB)
			red = red + color[0]
			green = green + color[1]
			blue = blue + color[2]
	
	red = (( red / ( (image.size[1]/SKIP_PIXELS) * (image.size[0]/SKIP_PIXELS) ) ) )/255.0
	green = ((green / ( (image.size[1]/SKIP_PIXELS) * (image.size[0]/SKIP_PIXELS) ) ) )/255.0
	blue = ((blue / ( (image.size[1]/SKIP_PIXELS) * (image.size[0]/SKIP_PIXELS) ) ) )/255.0
	c = Color(rgb=(red, green, blue))  
	#print (c)
	
	#print ("\n average   red:%s green:%s blue:%s" % (red,green,blue))	
	print ("\n average  (hex) "+  (c.hex))
	
	# TODO
    # Send an MQTT command with the Hex value
    # and/or
    # call a webhook
	


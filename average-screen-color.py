# Author: redakker 
# email: redman at redman dot hu

from PIL import ImageGrab # pip install pillow
import time
import os
import math 
from colour import Color # pip install colour
import paho.mqtt.client as mqtt # pip install paho-mqtt
import logging
from config import Config

config = Config();
logging.basicConfig(filename=config.logfile,level=logging.DEBUG,format='%(asctime)s %(message)s');


# Config
LOOP_INTERVAL  = 1    # how often we calculate screen colour (in seconds)
SKIP_PIXELS       = 10   # skip every SKIP_PIXELS number of pixels to speed up calculation

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code "+str(rc))
	


client = mqtt.Client()
client.will_set(config.baseTopic, "0,0,0")
client.on_connect = on_connect


#Set userid and password
client.username_pw_set(config.user, config.password)

#Connect
client.connect(config.broker, config.port, config.keepalive)


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
	
	r = (math.floor(c.get_red() * 255))
	g = (math.floor(c.get_green() * 255))
	b = (math.floor(c.get_blue() * 255))

	rgb = "" + str(r) + "," + str(g) + "," + str(b)

	 

	client.publish(config.baseTopic,rgb)
	# TODO
    # Send an MQTT command with the Hex value
    # and/or
    # call a webhook
	


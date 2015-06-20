#!/usr/bin/env python

import time
from datetime import datetime
import os
from sensor import Sensor
from output import Output
from graph import Graph
import argparse

# Grab our command line args
parser = argparse.ArgumentParser( description = "Environment control")
parser.add_argument('sensor_pin', type=int, help = "GPIO input pin")
parser.add_argument('output_pin', type=int, help = "GPIO output pin")
parser.add_argument('--humiditymin', type=int, action="store", default=95)
parser.add_argument('--humiditymax', type=int, action="store", default=95)
parser.add_argument('--graphupdate', type=int, action="store", default=10)
args = parser.parse_args()

# Output
output = Output(args.output_pin)

# Sensor - and link it to the output
sensor = Sensor(args.sensor_pin, output)

# Graphs
graph = Graph(sensor)
last_drawn = datetime.now()

while True:
	temperature = sensor.temperature
	humidity = sensor.humidity
	
	if not temperature and not humidity:
		print "No sensor reading on pin " + str(sensor.pin)

	if humidity < args.humiditymin and output.state == False:
		output.state = True
	elif humidity > args.humiditymax and output.state == True:
		output.state = False

	# Wait for a while
	time.sleep(2)

	# Update graphs occasionally
	if (datetime.now() - last_drawn).seconds > args.graphupdate:
		last_drawn = datetime.now()
		graph.draw()


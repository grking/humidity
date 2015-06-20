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
parser.add_argument('sensor_pin', type=int,
	help="The GPIO pin number which the AM2302 data line is connected to")
parser.add_argument('output_pin', type=int,
	help="The GPIO pin number which the output is connected to")
parser.add_argument('--humiditymin', type=int, action="store", default=95,
	help="Minimum humidity in percent.  Output goes high when humidity falls to this level. (default: %(default)s)")
parser.add_argument('--humiditymax', type=int, action="store", default=95,
	help="Maximum humidity in percent.  Output goes low when humidity rises to this level. (default: %(default)s)")
parser.add_argument('--graphupdate', type=int, action="store", default=10,
	help="How often we generate graphs in seconds. (default: %(default)s)")
parser.add_argument('--graphdir', type=str, action="store", default="/var/www",
	help="Full pathname of directory into which graphs are generated. (default: %(default)s)")
args = parser.parse_args()

# Output
output = Output(args.output_pin)

# Sensor - and link it to the output
sensor = Sensor(args.sensor_pin, output)

# Graphs
graph = Graph(args.graphdir, sensor)
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


# sensor.py
# AM2302 Sensor helper
# 
# Runs in a background thread constantly fetching the latest values from
# the sensor.

import Adafruit_DHT
import time
import os
from threading import Thread, Lock
import random
import rrdtool

class Sensor(Thread):

	@property
	def humidity(self):
		if not self.is_alive():
			return None
		return self._humidity

	@property
	def temperature(self):
		if not self.is_alive():
			return None
		return self._temperature

	@property
	def name(self):
		return "sensor-pin-%s" % self.pin

	@property
	def graph(self):
		self._lock.acquire()
		value = self._graph
		self._lock.release()
		return value
	@graph.setter
	def graph(self, value):
		self._lock.acquire()
		self._graph = value
		self._lock.release()

	def __init__(self, pin, output):
		super(Sensor, self).__init__()
		self.sensor = Adafruit_DHT.AM2302
		self.pin = pin
		self._output = output
		self.terminated = False
		self.daemon = True
		self._humidity = 0.0
		self._temperature = 0.0
		self._graph = True
		self._lock = Lock()
		self.create_db()
		self.start()

	def create_db(self):
		# Create our rrd database if it doesn't exist
		if os.path.exists(self.name + '.rrd'):
			return
		datasources = [
			'DS:temperature:GAUGE:10:-20:50',
			'DS:humidity:GAUGE:10:0:100',
			'DS:state:GAUGE:10:0:1'
		]
		rrdtool.create(self.name + '.rrd',
			# 5 second update cycle
			'--step', '5',
			'--no-overwrite',
			datasources,
			# 1 hour in 30 second intervals
			'RRA:AVERAGE:0.5:6:120',
			'RRA:MIN:0.5:6:120',
			'RRA:MAX:0.5:6:120',
			# 24 hours in 1 minute intervals
			'RRA:AVERAGE:0.5:12:1440',
			'RRA:MIN:0.5:12:1440',
			'RRA:MAX:0.5:12:1440',
			# 7 days in 1 hour intervals
			'RRA:AVERAGE:0.5:720:168',
			'RRA:MIN:0.5:720:168',
			'RRA:MAX:0.5:720:168'
		)

	def stop(self):
		self.terminated = True

	def run(self):
		while not self.terminated:
			# Read the sensor
			humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
			# If it returned a value, remember it
			if humidity and temperature:
				self._temperature = temperature
				self._humidity = humidity
				# Save to db
				if self.graph:
					self._lock.acquire()
					state = int(self._output.state)
					rrdtool.update(self.name+'.rrd', 'N:{0:0.1f}:{1:0.1f}:{2}'.format(temperature, humidity, state))
					self._lock.release()
			# Sensor has minimum refresh of 2 seconds
			time.sleep(2)


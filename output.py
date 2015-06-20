# output.py
# GPIO Output Helper
#
# Provides a simple wrapper for GPIO output with protection to stop too 
# frequent state changes.  

import time
import os
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

class Output(object):

	# Fastest we allow state changes in seconds
	MINIMUM_STATE_CHANGE_TIME = 60

	@property
	def state(self):
		return self._state
	@state.setter
	def state(self, value):
		if self._lastchange:
			delta = (datetime.now() - self._lastchange).seconds
			if delta < self.MINIMUM_STATE_CHANGE_TIME:
				return			
		GPIO.output(self.pin, value)
		self._state = value
		print "State change: output "+str(self._state)
		self._lastchange = datetime.now()

	def __init__(self, pin):
		super(Output, self).__init__()
		self.pin = pin
		GPIO.setmode( GPIO.BCM )
		GPIO.setwarnings( False )
		GPIO.setup( self.pin, GPIO.OUT )
		self._lastchange = None
		# Default state
		self.state = False
		

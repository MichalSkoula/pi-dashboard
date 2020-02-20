#!/usr/bin/python

import sys
import Adafruit_DHT

sensor = 11
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

print '{0:0.1f}'.format(temperature)

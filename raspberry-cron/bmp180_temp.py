#http://raspberrypi-aa.github.io/session3/i2c-temp-pressure.html

import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()
sensor.mode = BMP085.BMP085_ULTRAHIGHRES     
temp = sensor.read_temperature()
#pressure = sensor.read_pressure()

print '{0:0.1f}'.format(temp)
#print '{0:0.2f}'.format(pressure)

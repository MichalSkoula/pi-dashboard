# pi-dashboard
Personal project. Dashboard for my Raspberries, showing temperature, pressure and humidity from different places. Available sensors: LM75, DHT11, BMP180, Capacitive sensor (all plugged into Arduino). 

Live demo: https://pi.skoula.cz


## dashboard 
Vue application - frontend. Fetch JSON from webserver, show it and repeat.

## raspberry-cron 
Python script to fetch data from sensors, save to database and upload JSON to remote webserver.

## arduino-sensor
Arduino connected to Raspberry, sending JSON via serial connection. 

# pi-dashboard
Personal project. Dashboard for my Raspberries, showing temperature, pressure and humidity from different places. Available sensors: LM75, DHT11 and BMP180.


## dashboard 
Vue application - frontend. Fetch JSON from webserver, show it and repeat.

## raspberry-cron 
Python and even PHP scripts to fetch data from sensors. Running from secret bash cron script: fetch data, insert into MySQL, create JSON and upload it to real webserver.

## arduino-sensor
Arduino connected to Raspberry, sending JSON via serial connection. An alternative to connecting sensors directly to the Raspberry.

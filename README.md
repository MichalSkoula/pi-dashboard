# pi-dashboard
Personal project. Dashboard for my Raspberries, showing temperature, pressure and humidity from different places. Available sensors: LM75, DHT11, BMP180, Capacitive sensor (all plugged into Arduino). 

Live demo: http://ledtechpi.skoula.cz


## dashboard 
Vue application - frontend. Fetch JSON from webserver, show it and repeat.

## hardware

### arduino-sensor
Arduino connected to Raspberry, sending JSON via serial connection. 

### cron.py + config.py
Python script to fetch data from sensors, save to database and JSON file.

* sudo apt install fswebcam motion python-pandas libffi-dev
* pip install psutil gpiozero pyserial mysql-connector-python requests plotly paramiko

### log.sql 
MySQL table to save data.

### sketch.fzz + sketch.png
How to connect it.

![image](https://github.com/MichalSkoula/pi-dashboard/blob/master/hardware/sketch.png)

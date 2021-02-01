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

#### config.py
Better to name your devices like /dev/arduino_in, ... 

1. udevadm info -a -n /dev/video0 | less OR udevadm info -a -n /dev/ttyUSB0 | less
2. sudo nano /etc/udev/rules.d/99-arduino.rules
3. unplug
4. sudo /etc/init.d/udev reload
5. plug 
6. ls /dev/...bude tam

example of 99-arduino.rules:

* SUBSYSTEM=="tty", KERNEL=="ttyACM*", KERNELS=="1-1.4.2", SYMLINK+="arduino_in"
* SUBSYSTEM=="tty", KERNEL=="ttyACM*", KERNELS=="1-1.4.3", SYMLINK+="arduino_out"
* KERNEL=="video0",SUBSYSTEM=="video4linux",KERNELS=="1-1.4.1:1.0",SUBSYSTEMS=="usb",DRIVERS=="uvcvideo", SYMLINK+="camera_out"
* KERNEL=="video2",SUBSYSTEM=="video4linux",KERNELS=="1-1.3.4:1.0",SUBSYSTEMS=="usb",DRIVERS=="sonixj", SYMLINK+="camera_in1"
* KERNEL=="video3",SUBSYSTEM=="video4linux",KERNELS=="1-1.3.3:1.0",SUBSYSTEMS=="usb",DRIVERS=="uvcvideo", SYMLINK+="camera_in2"


#### install
* sudo apt install fswebcam motion python-pandas libffi-dev
* pip install psutil gpiozero pyserial mysql-connector-python requests plotly paramiko

### log.sql 
MySQL table to save data.

### sketch.fzz + sketch.png
How to connect it.

![image](https://github.com/MichalSkoula/pi-dashboard/blob/master/arduino-sensor/sketch.png)

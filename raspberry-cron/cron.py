#!/usr/bin/env python
from gpiozero import CPUTemperature
import psutil
import os
import serial
import mysql.connector
import config
import json
from paramiko import SSHClient
from scp import SCPClient
import paramiko
from datetime import datetime

# functions
def readLastLine(ser):
    last_data=''
    while True:
        data=ser.readline()
        if data!='':
            last_data=data
        else:
            return last_data

def isJson(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

# get date 
now = datetime.now()
datetime = now.strftime("%d. %m. %Y %H:%M:%S")

# get CPU temp
cpuTemp = CPUTemperature().temperature
print(cpuTemp)

# get memory usage
memory = psutil.virtual_memory().percent
print(memory)

# get CPU load
cpuLoad = psutil.cpu_percent()
print(cpuLoad)

# uses Fswebcam to take picture
os.system('fswebcam -r 640x480 -d ' + config.cameras['outdoor_cam'] + ' ' + config.ssh['local_path'] + 'outdoor.jpg') 
os.system('fswebcam -r 640x480 -d ' + config.cameras['indoor_cam']  + ' ' + config.ssh['local_path'] + 'indoor.jpg') 

# get data from arduino sensors
count = 0
max_guesses_allowed = 10
found = False
while not found and count < max_guesses_allowed:
    outdoor = readLastLine(serial.Serial(config.android_devices['outdoor_dev'], 115200, timeout=3))
    indoor = readLastLine(serial.Serial(config.android_devices['indoor_dev'], 115200, timeout=3))

    if isJson(outdoor) and isJson(indoor):
        outdoor = json.loads(outdoor)
        print(outdoor)
        indoor = json.loads(indoor)
        print(indoor)

        found = True

    print("wrong")
    count += 1

if found == False:
    exit()

# average 
indoorTemp = (indoor['temp1'] + indoor['temp2'] + indoor['temp3']) / 3
outdoorTemp = (outdoor['temp1'] + outdoor['temp2'] + outdoor['temp3']) / 3


# save to DB
mydb = mysql.connector.connect(
    host=config.mysql['host'],
    database=config.mysql['db'],
    user=config.mysql['user'],
    password=config.mysql['password']
)

mycursor = mydb.cursor(dictionary=True)
sql = """
    INSERT INTO log (indoor_temp, indoor_pressure, indoor_humidity, indoor_moisture, outdoor_temp, outdoor_pressure, outdoor_humidity, cpu_temp, cpu_load, memory) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
val = (
    indoorTemp,
    indoor['pressure'],
    indoor['humidity'],
    indoor['moisture'],
    outdoorTemp,
    outdoor['pressure'],
    outdoor['humidity'],
    cpuTemp,
    cpuLoad,
    memory
)
mycursor.execute(sql, val)
mydb.commit()

# get average temps
mycursor.execute("""
    SELECT 
        MIN(indoor_temp) AS min_indoor_temp, 
        MAX(indoor_temp) AS max_indoor_temp,
        AVG(indoor_temp) AS avg_indoor_temp,
        MIN(outdoor_temp) AS min_outdoor_temp, 
        MAX(outdoor_temp) AS max_outdoor_temp,
        AVG(outdoor_temp) AS avg_outdoor_temp
    FROM log 
    WHERE DATE(inserted_at) = DATE(NOW());
""")
averageTemps = mycursor.fetchone()
print(averageTemps)

# save to JSON 
data = {
    'indoor_temp': {
        'actual': indoorTemp,
        'min': averageTemps['min_indoor_temp'],
        'max': averageTemps['max_indoor_temp'],
        'avg': averageTemps['avg_indoor_temp'],
    },
    'indoor_pressure': indoor['pressure'],
    'indoor_humidity': indoor['humidity'],
    'indoor_moisture': indoor['moisture'],
    'outdoor_temp': {
        'actual': outdoorTemp,
        'min': averageTemps['min_outdoor_temp'],
        'max': averageTemps['max_outdoor_temp'],
        'avg': averageTemps['avg_outdoor_temp'],
    },
    'outdoor_pressure': outdoor['pressure'],
    'outdoor_humidity': outdoor['humidity'],
    'cpu_temp': cpuTemp,
    'cpu_load': cpuLoad,
    'memory': memory,
    'updated': datetime
}

with open(config.ssh['local_path'] + 'data.json', 'w') as f:
    json.dump(data, f)

# upload it 
ssh = SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(config.ssh['host'], username=config.ssh['user'], password=config.ssh['password'])

with SCPClient(ssh.get_transport()) as scp:
    scp.put(config.ssh['local_path'] + 'data.json', config.ssh['remote_path'] + 'data.json')
    scp.put(config.ssh['local_path'] + 'outdoor.jpg', config.ssh['remote_path'] + 'outdoor.jpg')
    scp.put(config.ssh['local_path'] + 'indoor.jpg', config.ssh['remote_path'] + 'indoor.jpg')

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
from shutil import copyfile
import time

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

while True:
    # get date 
    now = datetime.now()
    datetimeStr = now.strftime("%d. %m. %Y %H:%M:%S")

    # get CPU temp
    cpuTemp = CPUTemperature().temperature
    print(cpuTemp)

    # get memory usage
    memory = psutil.virtual_memory().percent
    print(memory)

    # get CPU load
    cpuLoad = psutil.cpu_percent()
    print(cpuLoad)

    # get HDD usage 
    hdd = psutil.disk_usage('/')
    hddUsage = float(hdd.used) / float(hdd.total) * 100
    print(hddUsage)

    # uses Fswebcam to take picture
    os.system('fswebcam -r 640x480 -d ' + config.cameras['outdoor_cam'] + ' ' + config.webserver + '/outdoor.jpg') 
    os.system('fswebcam -r 640x480 -d ' + config.cameras['indoor_cam']  + ' ' + config.webserver + '/indoor.jpg')

    # get data from arduino outdoor sensor
    count = 0
    max_guesses_allowed = 10
    found = False
    while not found and count < max_guesses_allowed:
        outdoor = readLastLine(serial.Serial(config.android_devices['outdoor_dev'], 115200, timeout=3))
        if isJson(outdoor):
            outdoor = json.loads(outdoor)
            print(outdoor)
            found = True
        print("outdoor wrong")
        count += 1
    if found == False:
        exit()

    # get data from arduino indoor sensor
    count = 0
    found = False
    while not found and count < max_guesses_allowed:
        indoor = readLastLine(serial.Serial(config.android_devices['indoor_dev'], 115200, timeout=3))
        if isJson(indoor):
            indoor = json.loads(indoor)
            print(indoor)
            found = True
        print("indoor wrong")
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
        INSERT INTO log (indoor_temp, indoor_pressure, indoor_humidity, indoor_moisture, indoor_light, outdoor_temp, outdoor_pressure, outdoor_humidity, cpu_temp, cpu_load, memory, hdd) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (
        indoorTemp,
        indoor['pressure'],
        indoor['humidity'],
        indoor['moisture'],
        indoor['light'],
        outdoorTemp,
        outdoor['pressure'],
        outdoor['humidity'],
        cpuTemp,
        cpuLoad,
        memory,
        hddUsage
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
            AVG(outdoor_temp) AS avg_outdoor_temp,
            MIN(indoor_pressure) AS min_indoor_pressure, 
            MAX(indoor_pressure) AS max_indoor_pressure,
            AVG(indoor_pressure) AS avg_indoor_pressure,
            MIN(outdoor_pressure) AS min_outdoor_pressure, 
            MAX(outdoor_pressure) AS max_outdoor_pressure,
            AVG(outdoor_pressure) AS avg_outdoor_pressure
        FROM log 
        WHERE DATE(inserted_at) = DATE(NOW());
    """)
    averageToday = mycursor.fetchone()
    print(averageToday)

    # save to JSON 
    data = {
        'indoor_temp': {
            'actual': indoorTemp,
            'min': averageToday['min_indoor_temp'],
            'max': averageToday['max_indoor_temp'],
            'avg': averageToday['avg_indoor_temp'],
        },
        'indoor_pressure': {
            'actual': indoor['pressure'],
            'min': averageToday['min_indoor_pressure'],
            'max': averageToday['max_indoor_pressure'],
            'avg': averageToday['avg_indoor_pressure'],
        },
        'indoor_humidity': indoor['humidity'],
        'indoor_moisture': indoor['moisture'],
        'indoor_light': indoor['light'],
        'outdoor_temp': {
            'actual': outdoorTemp,
            'min': averageToday['min_outdoor_temp'],
            'max': averageToday['max_outdoor_temp'],
            'avg': averageToday['avg_outdoor_temp'],
        },
        'outdoor_pressure': {
            'actual': outdoor['pressure'],
            'min': averageToday['min_outdoor_pressure'],
            'max': averageToday['max_outdoor_pressure'],
            'avg': averageToday['avg_outdoor_pressure'],
        },
        'outdoor_humidity': outdoor['humidity'],
        'cpu_temp': cpuTemp,
        'cpu_load': cpuLoad,
        'memory': memory,
        'hdd': hddUsage,
        'updated': datetimeStr
    }

    with open(config.webserver + '/data.json', 'w') as f:
        json.dump(data, f)

    time.sleep(5)

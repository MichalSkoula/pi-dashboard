import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
while 1: 
    if(ser.in_waiting >0):
        line = ser.readline()
        print(line)
        break

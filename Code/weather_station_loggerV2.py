#!/usr/bin/python3

import serial, time, datetime, os.path, sys
from datetime import datetime

save_location = os.path.join(sys.path[0], 'weather_data.csv') # save weather data to the same folder this program executes from
print(save_location) # just in case you don't know already

serial_port_name = '/dev/ttyACM0' # on linux and linux-like stuff, determine the correct port by using the shell command "ls /dev/"
baud_rate = 115200 # match this to the Arduino's baud rate. Slower makes for more reliable transmissions on long cables.
ready = 0

def get_data():
	ser.write(b'?') #send a character to the arduino
	new_data = ser.readline()  # read a '\n' terminated line, as opposed to 1 or n bytes
	new_data = new_data.decode('UTF-8')
	return new_data[:-2] # return and cut off unnecessary CR and LF

def save_data(line_to_save):
	data_string = line_to_save
	data_string += ", "
	data_string += str(datetime.now().strftime("%D %H:%M:%S")) # yyyy-mm-dd hh:mm:ss
	
	file = open(save_location, "a")
	file.write(data_string)
	file.write("\n")
	file.close()

with serial.Serial(serial_port_name, baud_rate, timeout=0) as ser:
	line = get_data()
	print(line)
	line = get_data()
	print(line)
	line = get_data()
	print(line)
if __name__ == '__main__': #we will be importing a function and do not want to run the entire script when importing
	ser = serial.Serial(serial_port_name, baud_rate, timeout=1)
	while(1):
		line = get_data()
		print(line)
		save_data(line)
		time.sleep(2)
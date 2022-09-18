#Please usee demo.py instead




import time, serial, time, datetime
import threading, queue

from multiprocessing import Process, Value 
from flask import Flask, render_template
from weather_station_loggerV3 import serial_port_name, start, baud_rate, save_data, get_data
app = Flask(__name__)

ser = serial.Serial(serial_port_name, baud_rate, timeout=1)
q = queue.Queue()
rain_d = []
avg_wind_d = []
gust_d = []
adc_d = []
direction_d = []
temp_d = []
pressure_d = []
time_d = []
def data_line_to_queue(string):
	x = string.split(', ')
	q.put(x[0])
	q.put(x[1])
	q.put(x[2])
	q.put(x[3])
	q.put(x[4])
	q.put(x[5])
	q.put(x[6])

@app.route('/')
def render():
	while not q.empty():
		time_d.append(q.get())
		rain_d.append(q.get())
		avg_wind_d.append(q.get())
		gust_d.append(q.get())
		adc_d.append(q.get())
		direction_d.append(q.get))
		temp_d.append(q.get())
		pressure_d.append(q.get())

	return render_template('solartree.html', rain=rain_d, avg=avg_wind_d, gust=gust_d, adc=adc_d, direc=direction_d, temp=temp_d, pressure=pressure_d, time=time_d)

def infinite_data_loop():
	while(1):
		q.put(str(datetime.now().strftime("%D %H:%M:%S")))
		line = get_data()
		print(line)	
		save_data(line)
		data_line_to_queue(line)
 		time.sleep(2)

if __name__=='__main__':
	my_thread = threading.Thread(target=infinite_data_loop)
	my_thread.start()
	app.run(host='0.0.0.0', debug=True)

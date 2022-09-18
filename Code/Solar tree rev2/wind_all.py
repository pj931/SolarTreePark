from gpiozero import Button
import time
import math
import bme280
import ADC_wind
import statistics
import database



wind_count = 0
radius_cm = 9.0
wind_interval = 5
CM_to_KM = 100000.0
secs_to_hr = 3600
store_speeds = []
rain_sensor = Button(6)
rain_size = 0.2794
count = 0


def spin():
    
    global wind_count
    wind_count = wind_count + 1
    #print ("spin" + str(wind_count))
 
 
def calculate_speed(time_sec):
    global wind_count
    cir_cm = (2*math.pi)*radius_cm
    rotations = wind_count /2.0
    
    dist_km = (cir_cm * rotations)/CM_to_KM
    
    km_sec = dist_km/ time_sec
    km_hr = km_sec *secs_to_hr
    
    
    return km_hr * 1.18

def rain_bucket():
    global count
    count = count + 1
    print(count * rain_size)

def reset_rain():
    global count
    count = 0
    
def reset_wind():
    global wind_count
    wind_count = 0
    
    wind_sensor = Button(5)   
    wind_sensor.when_pressed = spin

    
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        wind_start_time = time.time()
        reset_wind()
        
    while time.time() - wind_start_time <= wind_interval:
            store_directions.append(ADC_Wind.get_value())
   
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed) 
    wind_average = ADC_Wind.get_average(store_directions)
    
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    print(wind_speed, wind_gust,wind_average)
    stpre_speeds = []
    store_directions = []


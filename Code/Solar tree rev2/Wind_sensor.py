from gpiozero import Button
import time
import math
import bme280_sensor
import ADC_Wind 
import statistics 

wind_count = 0
radius_cm = 9.0
wind_interval = 1
CM_to_KM = 100000.0
secs_to_hr = 3600
store_speeds = []

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

def reset_wind():
    global wind_count
    wind_count = 0 
    wind_Anm = Button(13)    
    wind_Anm.when_pressed = spin
    
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed) 
    
    
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    print(wind_speed, wind_gust)

    
    

    


from gpiozero import Button

rain_sensor = Button(6)
rain_size = 0.2794
count = 0

def rain_bucket():
    global count
    count = count + 1
    print(count * rain_size)

def reset_rain():
    global count
    count = 0
    
rain_sensor.when_pressed = rain_bucket
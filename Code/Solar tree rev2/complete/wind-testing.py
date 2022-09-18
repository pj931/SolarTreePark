from gpiozero import Button


wind_sensor = Button(5)
wind_count = 0
wind_anm = Button (13)
wind_anc = 0

def spinA():
    
    global wind_count
    wind_count = wind_count + 1
    print ("spin A:" + str(wind_count))
   
    
def spinB():  
    global wind_anc
    wind_anc = wind_anc + 1
    print ("spin B:" + str(wind_anc))
    
    
wind_anm.when_pressed = spinA
wind_sensor.when_pressed = spinB
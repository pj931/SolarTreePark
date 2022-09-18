import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40,GPIO.OUT)
pwm = GPIO.PWM(40,50)  ## sets PWM board pin at 40, duty cycle at 50%

dc = 0
pwm.start(dc)       ## sets pwm at 0% duty cycle
    
try:
    while True:
        
        for dc in range (0,100,1):  ##
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range (100,0,-1): ##
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
        
except KeyboardInterrupt:
        print("ctl C was pressed, ending program now")
        
        
pwm.stop()
GPIO.cleanup()


    
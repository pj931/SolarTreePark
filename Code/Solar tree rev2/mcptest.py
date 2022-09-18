from gpiozero import MCP3008,LED
import time

pin = LED(5)
adc = MCP3008(channel = 0)

while True:
    print(adc.value)
    time.sleep(1)
    pin.on()
    
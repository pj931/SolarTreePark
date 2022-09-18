from time import strftime
import bme280
import smbus2
import time 


port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)

Cel_to_Far = (format((data.temperature * 9.00/5.00) + 32.00,'.2f'))
Pas_to_Psi = (format(data.pressure/6895.00,".2f"))
Humidity = (format(data.humidity,".2f"))



print("Date:", data.timestamp)
print("Humidity:",Humidity, "%")
print("Degrees:",Cel_to_Far, "F")
print("Pressure:", Pas_to_Psi, "Psi")

#print(data)

    
#!/usr/bin/python3

import serial, time, datetime, os.path, sys, minimalmodbus
import solar_ctrl
from solar_ctrl import read_address, setup_modbus
from datetime import datetime, timedelta
from os.path import exists


#Input register addresses
PV_rated_voltage = 0x3000
PV_rated_current = 0x3001
PV_voltage = 0x3100
bat_soc = 0x311A
#!!!!!Check the datasheet of the different registers for more functionality!!!!!

serial_port_name = '/dev/ttyACM0' # on linux and linux-like stuff, determine the correct port by using the shell command "ls /dev/"
baud_rate = 115200 # match this to the Arduino's baud rate. Slower makes for more reliable transmissions on long cables.
ser = serial.Serial(serial_port_name, baud_rate, timeout=1)
t = 15 #use this variable to change the amount of time that is waited between data requests

#For the solar controller

#We set up the file for saving a certain date's data
def setup_datefile(returnDate = False):
    todays_date = datetime.today().strftime('%b-%d-%Y')
    #Here we have the option of simply extracting the current date instead of making the entire file
    if returnDate == True:
        return todays_date
    #Check if a file is more than 7 days old. If true, remove it (change to 'days=k-1' to remove files after the kth day)
    expired_date = (datetime.today() - timedelta(days=8)).strftime('%b-%d-%Y')
    expired_filename = "Data_" + str(expired_date) + ".csv"
    expired_file = os.path.join('/home/pi/Desktop/SolarTree/SolarData', expired_filename)
    if exists(expired_file):
        os.remove(expired_file)

    #Now we are creating a new data file named after the current date
    filename = "Data_" + str(todays_date) + ".csv"
    file = os.path.join('/home/pi/Desktop/SolarTree/SolarData', filename)
    f = open(file, 'w')
    #The next line is the single header. You will need to check with the rest of the team to see what data is important to show and modify it correctly.
    #The name is important for generating graphs in the streamlit.io application.
    
    f.write("rainfall (inches),avg wind speed (mph),gust wind speed (mph),wind direction,temperature (deg F),pressure (inHg),PV Voltage (V),PV Rated Voltage (V),PV Rated Current (A),Time\n")
    f.close()
    return file
    
#Mostly unmodified
def get_data():
    ser.write(b'?') #send a character to the arduino
    new_data = ser.readline()  # read a '\n' terminated line, as opposed to 1 or n bytes
    new_data = new_data.decode('UTF-8')
    new_data = new_data[:-2]
    return new_data[:-2] # return and cut off unnecessary CR and LF

#The if; else is just for .csv formatting purposes and worked best for me
def save_data(line_to_save, save_location, first_run):
    data_string = line_to_save
    if (first_run == 1):
        first_run = 0
    else:
        data_string += ","+ datetime.now().strftime("%H:%M:%S")# hh:mm:ss
    file = open(save_location, "a")
    file.write(data_string)
    file.write("\n")
    file.close()

#Add some code here that you want to run once on startup
def start():
    pass

if __name__ == '__main__':#we will be importing a function and do not want to run the entire script when importing
    first_run = 1
    start()
    controller = setup_modbus() #Setting up the Epever controller
    #Setting up the first run data file for the current date
    file = setup_datefile()
    date = setup_datefile(True)
    
    while(1):
        #This updates the current date once it is midnight 
        if date != setup_datefile(True):
            file = setup_datefile()
            date = setup_datefile(True)
        line = get_data() #Arduino dataa
        if first_run == 0:
            #reading from the Epever solar controller
            line += ', '+ str(read_address(controller, PV_voltage)) + ', ' + str(read_address(controller, PV_rated_voltage)) + ', ' + str(read_address(controller, PV_rated_current))
        #print(line)
        save_data(line, file, first_run)
        if first_run == 1:
            first_run = 0
        time.sleep(60*t) #time between data collection in seconds

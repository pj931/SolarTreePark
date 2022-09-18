#streamlit.io
#IMPORTANT DO NOT UPDATE PAST VERSION 0.62!!!!!!

import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import datetime
from os.path import exists


def read_csv(filename):
    full_path = "/home/pi/Desktop/SolarTree/SolarData/"+filename 
    if exists(full_path) == False:
        st.write("It seems there is not data for " + date +". Please choose another date.")
        quit()
    data = pd.read_csv(full_path)
    return data

selector = st.sidebar.selectbox(
        "What data would you like to view?",
        ("Today's data", "1 day ago", "2 days ago", "3 days ago", "4 days ago", "5 days ago", "6 days ago", "7 days ago")
)

if selector == "Today's data":
    delta = 0
elif selector == "1 day ago":
    delta = 1
elif selector == "2 days ago":
    delta = 2
elif selector == "3 days ago":
    delta = 3
elif selector == "4 days ago":
    delta = 4
elif selector == "5 days ago":
    delta = 5
elif selector == "6 days ago":
    delta = 6
elif selector == "7 days ago":
    delta = 7

date_formatter = datetime.datetime.today() - datetime.timedelta(days=delta)
date = str(date_formatter.strftime('%b-%d-%Y'))
my_file = 'Data_' + date + '.csv'

st.title('Welcome to the UConn Solar Tree dashboard!')
data = read_csv(my_file)
#the date formatter is not showing the day of the week, might be worth looking into
st.header('Displaying data from ' + str(date_formatter.weekday()) + ', ' + date + '...')

time = data['Time'].tolist()
rain = data['rainfall (inches)'].tolist()
wind_avg = data['avg wind speed (mph)'].tolist()
gust = data['gust wind speed (mph)'].tolist()
temp = data['temperature (deg F)'].tolist()
pressure = data['pressure (inHg)'].tolist()


chart_data_1 = pd.DataFrame(
    {'Time' : time, 'Temperature (deg F)' : temp})
chart_data_2 = pd.DataFrame(
    {'Time' : time, 'Rain' : rain}) 
chart_data_3 = pd.DataFrame(
    {'Time' : time, 'Avg wind speed (mph)' : wind_avg})
chart_data_4 = pd.DataFrame(
    {'Time': time, 'Avg gust speed (mph)' : gust}) 
chart_data_5 = pd.DataFrame(
    {'Time' : time, 'Pressure (inHg)' : pressure})


st.header('Temp Data')
st.line_chart(data = chart_data_1.set_index('Time'), width = 2000)
st.header('Rain Data')
st.line_chart(data = chart_data_2.set_index('Time'), width = 2000)
st.header('Avg Wind Data')
st.line_chart(data = chart_data_3.set_index('Time'), width = 2000)
st.header('Avg Gust Data')
st.line_chart(data = chart_data_4.set_index('Time'), width = 2000)
st.header('Pressure Data')
st.line_chart(data = chart_data_5.set_index('Time'), width = 2000)



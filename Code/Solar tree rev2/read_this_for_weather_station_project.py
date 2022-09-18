'Solar Tree with Raspberry PI 3B+'

This Design for the Solar Tree relies on just the Raspberry PI, ADC, and Sensors to
connect to the weather station.

During the testing process, the ADC chip 'MCP3008' was not working in lieu of programming
the wind vane. Once this portion of the project is situated. Then everything else shall work
accordingly. To make sure MCP3008 works, make sure to see if raspberry pi needs to be updated
and that all of the updates coincide with the weather station program itself. 

Other things to work on would be data storage from excel to the uconn server, touch pad,
relay connection and load, voltage, current sensor to be connected all from the Raspberry PI
to the MPPT controller. 

In this folder there are some codes already completed. You just need to import all of the codes
into one code and test each portion of that code to make sure it works.

'wind-testing.py' - this will test how many spins the anometer and wind vane turns.

'wind-direction-test.py' - this should be able to read the adc and give back a voltage reading,
this is where it gets stuck and does not read out the direction the wind vane goes

Complete folder is where the other portions of the project has been test and completed,
it is best to make sure it is working well. 

You can also check recent videos from past students to understand the concept of this project
it is very useful

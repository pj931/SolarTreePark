/*
 * This program collects weather data and transmits it upon request rather than on a fixed interval.
 * Transmission is sent as text over serial at 
 * It collects temperature, pressure, humidity, average and gust wind speeds, and rainfall.
 * I intended this to be used with Sparkfun's weather station and a BMP 388 sensor.
 * 
 * purchase the weather station here: https://www.sparkfun.com/products/15901
 * read about the weather station here: https://www.sparkfun.com/products/15901
 * 
 * purchase a BMP388 sensor here: https://www.dfrobot.com/product-1792.html
 * read about the BMP388 sensor here: https://wiki.dfrobot.com/Gravity_BMP280_Barometric_Pressure_Sensors_SKU_SEN0251
 * 
 */



#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"



#define SEALEVELPRESSURE_HPA (1013.25)

// hardware defines
#define BMP_CS 10  // chip select pin for the BMP sensor. Can be any digital output.
#define RAIN_PIN 2 // digital input used for the rain meter. Must have an interrupt!
#define WIND_PIN 3 // digital input used for the anemometer. Must have an interrupt!
#define WEATHERVANE A0 // analog input used for the weathervane. Must be an ADC input!

Adafruit_BMP3XX bmp; // create a BMP sensor object

unsigned long timer = 0;       // tracks elapsed time between data requests.
char incoming_character = "";  // stores characters received over serial. The exact character is currently not used for anything, but it needs to be stored anyway.
                               // used, but it must be stored somewhere for everythign to work properly.
unsigned int rain_counts = 0;  // Counts how many times the rain bucket has tipped back and forth. One count per tip in each direction.
float rainfall = 0.0;          // Rainfall in inches
float rain_constant = 0.011;   // This is the counts-to-inches conversion factor for Sparkfun's weather station. Different stations may need different constants.
unsigned int wind_counts = 0;  // One count per rotation of the anemometer. One count per second = 1.492 mph.
float wind_constant = 1.492;   // This is the counts-to-mph conversion factor for Sparkfun's weather station. Different stations may need different constants.
float avg_wind_speed = 0.0;    // Wind speed in mph, averaged over the time since data was last collected.
unsigned long gust_timer = 4294967295;  // Duration of the one fastest rotation of the anemometer (in milliseconds). Starts at the largest value possible (slowest gust possible)
unsigned long this_rotation_timer = 0; // Contains the time in ms of thenewest anemometer rotation/
float gust_wind_speed = 0.0;   // Gust wind speed in mph
int wind_ADC_counts = 0;       // The weathervane outputs one of 8 an analog voltages, corresponding to the cardinal and intercardinal
                               // directions. This stores the resulting ADC reading in "ADC counts" rather than volts because voltage isn't needed.
byte remapped_wind_counts = 0; // wind_ADC_counts has a range 0-1023. This will be remapped to the range 0-15 for choosing a direction from the wind_direction array.
                               // W corresponds to the lowest voltage, NW, contains the next higest, and so on up the list.
String wind_direction[] = {"ESE", "ENE", "E", "SSE", "SE", "SSW", "S", "NNE", "NE", "WSW", "SW", "NNW", "N", "WNW", "NW", "W"};



void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("weatherStation3.ino by kevin.2.knowles@uconn.edu/knowleskevina@gmail.com");
  Serial.println("Send any single character to request data");


  if (! bmp.begin_SPI(BMP_CS)) {  // Try to connect to the BMP sensor using hardware SPI
    Serial.println("No BMP sensor found!");
  }
  
  pinMode(RAIN_PIN, INPUT_PULLUP);
  pinMode(WIND_PIN, INPUT_PULLUP);
  // about interrupts: https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), incrementRainCounts, FALLING);
  attachInterrupt(digitalPinToInterrupt(WIND_PIN), incrementWindCounts, FALLING);
  
  // Set up BMP oversampling and filter initialization
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}



void loop() {
  if(Serial.available()){
    noInterrupts();           // Disable interrupts. This prevents errors in wind and rain related calculations.
    timer = millis() - timer; // Once this executes, timer contains the time in milliseconds since data was last collected.
    
    incoming_character = Serial.read(); // We don't actually need to use the incoming character for anything, we just need to read the serial buffer so that
                                        // it empties. This makes it so that Serial.available() is only true once per character.
    
    rainfall = rain_counts * rain_constant; // One count is about 0.011 inches of rain
    Serial.print(rainfall, 3);
    Serial.print(", ");
    rain_counts = 0;

    avg_wind_speed = 1000 * wind_constant * (float(wind_counts) / float(timer)); // Extra factor of 1000 needed because time is tracked in milliseconds, not seconds.
                                                          // One rotation per second (one count per second) is about 1.492 mph.
    Serial.print(avg_wind_speed, 3);
    Serial.print(", ");
    wind_counts = 0;

    gust_wind_speed = 1000 * (wind_constant / gust_timer);
    Serial.print(gust_wind_speed, 3);
    Serial.print(", ");
    gust_timer = 4294967295; // Reset to the slowest gust possible

    wind_ADC_counts = analogRead(WEATHERVANE);
    remapped_wind_counts = map(wind_ADC_counts, 66, 945, 0, 15); // about the map() function: https://www.arduino.cc/reference/en/language/functions/math/map/
    Serial.print(wind_direction[remapped_wind_counts]);
    Serial.print(", ");

    if (! bmp.performReading()) {
      // Attempt to read the BMP sensor. If it cannot be read, force it to output NaN (not a number) as a simple note that a problem occurred
      bmp.pressure = 0.0/0.0;
      bmp.temperature = 0.0/0.0;
    }
    
    Serial.print(bmp.temperature);
    Serial.print(", ");
    
    Serial.print(bmp.pressure);
    Serial.print(", ");
    
    Serial.println(timer);
    
    interrupts(); // reenable interrupts
    timer = millis(); // note the current time so that the next readings will be calculated over the correct time period
  }
}



void incrementRainCounts(){
  rain_counts++; // This will result in erroneous readings if more than 2^16 - 1 = 65,535 rain counts occur between requests
                 // for data. That's about 720 inches of rain, so you have more to worry about than bad data if this rolls over.
}



void incrementWindCounts(){
  wind_counts++; // This will also result in erroneous readings if more than 65,536 wind counts occur between requests for data.
                 // Again, you probably have bigger problems if this rolls over.
  
  this_rotation_timer = millis() - this_rotation_timer; // calculate the duration of the newest rotation
  if(this_rotation_timer < gust_timer){ // save this time if it's a new record fastest
    gust_timer = this_rotation_timer;
  }
  this_rotation_timer = millis(); // note the current time so that the next rotation will be calculated over the correct time period
}

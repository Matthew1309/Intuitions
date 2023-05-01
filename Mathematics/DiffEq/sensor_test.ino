/*
 * # sensor_test.ino
 * 
 * Purpose:
 * The purpose of this script is to test the functionality of 
 * the HTF3228LF thermistor and humidity sensor.
 */
#include <math.h>
#include <FreqCount.h>

// Setting the pins
const int pinTemp = 14;

// Humidity
float currentTemp;
const float voltageConversion = 5.0/1023.0;
float BTest = 4084;//3730.0;
float VccTest = 4.95;
float R1Test = 54000;
float RnTest = 16212;
// Humidity
unsigned long currentHumidity;

///////////////////////////////////////////////
// Helper functions
///////////////////////////////////////////////
 float readHumidityHTF3228LF() {
    // This function requires that the user
    // attach their frequency to pin 13 by 
    // default and requires no further input
    // USAGE: readHumidityHTF3228LF()
    // OUTPUT: unsigned long RH
    unsigned long frequencyH;
    //if(FreqCount.available()){
    frequencyH = FreqCount.read();
    //}
    Serial.println(String("freq: ") + frequencyH);
    return (-1*(frequencyH - 9595))/14.8;//relative humidity
    //return(frequencyH);
}

float readTempHTF3228LF(int pin, 
                        float vConvert = 0.0049,// analogRead units to volts
                        float B = 3730.0,
                        float Vcc = 5.0,//V, 
                        float R1 = 56000.0,//ohm, 
                        float Rn = 10000.0,//ohm,
                        float Tn = 298.0,//kelvin,  
                        float K = 273.0){//kelvin)
    // This function requires an input pin and will output
    // the predicted temperature in celcius. The optional
    // parameters are circuit specific and can be tweaked 
    // to get better temperature readings if need be.
    // USAGE: readTempHTF3228LF(10)
    // OUTPUT: float Celcius
                        
    // Read in voltage                    
    float Vt = analogRead(pin) * vConvert;
    // Calculate thermistor resistance                    
    float Rt = (((Vcc * R1) / (Vcc - Vt)) - R1); //ohm
    /*Serial.println(String("\nVt: ") + Vt + 
                   String("\nRt: ") + Rt +
                   String("\nTemp: " + String((Tn*B)/(Tn * log(Rt/Rn) + B) - K)));*/
    // Use datasheet formula to calculate temp in Celcius                    
    return (Tn*B)/(Tn * log(Rt/Rn) + B) - K; //C the 17 was my ratchet correction factor I'll use in a pinch
}
                        
void setup(){
  pinMode(pinTemp, INPUT);
  Serial.begin(9600);
  FreqCount.begin(1000);
}

void loop(){
  currentHumidity = readHumidityHTF3228LF();
  currentTemp = readTempHTF3228LF(pinTemp, voltageConversion, BTest, VccTest, R1Test, RnTest);
  Serial.println(String("Temp: ") + currentTemp +
                  " Humidity: " + currentHumidity + "\n");
  
  
}


                        

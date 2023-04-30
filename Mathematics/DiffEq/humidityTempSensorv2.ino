// In this project we will read in the raw
// analog input from the HTF3228LF board
// made by Humeriel.

//Imports
#include <math.h>
#include <sensorFunctions.h>

// Global constants
const int tempPin = 18;
const int humPin = 16;
const float vConvert = 0.0049; // analogRead units to volts

//Temperature variables
float temp;
// Humidity variables
float humidity;

void setup() {
  // put your setup code here, to run once:
  pinMode(tempPin, INPUT);
  pinMode(humPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // Read the temp pin
  temp = readTempHTF3228LF(tempPin) //C
  
  // Read the humid pin
  humidity = readHumidityHTF3228LF(humPin, smoothing=1); //RH

  // Printing the output
  Serial.println(String(temp) + " " + String(humidity));
}

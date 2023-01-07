// In this project we will read in the raw
// analog input from the HTF3228LF board
// made by Humeriel.

//Imports
#include <math.h>

// Pins used
const int tempPin = 18;
const int humPin = 16;

const float vConvert = 0.0049; // analogRead units to volts

//Temperature variables
float Vt;
float Rt;
float T;
const int Vcc = 5;//V
const int R1 = 56000;//ohm
const int K = 273;//kelvin
const int Tn = 298;//kelvin
const int B = 3730;
const int Rn = 10000;//ohm

// Humidity variables
float frequencyH;
float humidity;
int pulseHigh;
int pulseLow;
float pulseTotal;

void setup() {
  // put your setup code here, to run once:
  pinMode(tempPin, INPUT);
  pinMode(humPin, INPUT);
  Serial.begin(9600);
  //exit(0);
}

void loop() {
  // Read the temp pin
  Vt = analogRead(tempPin) * vConvert;
  Rt = (((Vcc * R1) / (Vcc - Vt)) - R1); //ohm
  T = (Tn*B)/(Tn * log(Rt/Rn) + B) - K; //C
  
  // Read the humid pin
  pulseHigh = pulseIn(humPin, HIGH);
  pulseLow = pulseIn(humPin, LOW);
  pulseTotal = pulseHigh + pulseLow;//time in us
  frequencyH = 1000000/pulseTotal;//freq in Hz
  humidity = (-1*(frequencyH - 9595))/14.8;//relative humidity

  // Printing the output

  Serial.println(String(T) + " " + String(humidity));
  // delay(500);
  
}

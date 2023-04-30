#include <math.h>

int len(int intArray){
    // Member function of len() group
    // given an input array of integers,
    // return the array length as an integer
    // USAGE: len(intArray)
    // OUTPUT: int
    return sizeof(intArray) / sizeof(intArray[0]);
}

int len(float floatArray){
    // Member function of len() group
    // given an input array of floats,
    // return the array length as an integer
    // USAGE: len(floatArray)
    // OUTPUT: int
    return sizeof(floatArray) / sizeof(floatArray[0]);
}

float mean(float floatArray){
    // Member function of mean() group
    // given an input array of floats,
    // return the mean as a float
    // USAGE: mean(floatArray)
    // OUTPUT: float
    float sum;
    int floatArrayLength = len(floatArray);
    for(int i = 0; i < floatArrayLength; i++){
        sum += floatArray[i];
    }
    return sum/floatArrayLength;    
}

float mean(int intArray){
    // Member function of mean() group
    // given an input array of integers,
    // return the mean as a float
    // USAGE: mean(intArray)
    // OUTPUT: float
    float sum;
    int intArrayLength = len(intArray);
    for(int i = 0; i < intArrayLength; i++){
        sum += intArray[i];
    }
    return sum/intArrayLength;    
}

float readHumidityHTF3228LF(int pin, int smoothing=1) {
    // This function requires an input pin and will output
    // the predicted humidity as RH (relative humidity). 
    // The optional parameter smoothing affects how variable
    // the output will be, and also how many cycles this function
    // will read and therefore run.
    // USAGE: readHumidityHTF3228LF(10)
    // OUTPUT: float RH
    
    // Set the variables
    float pulseTotalArray[smoothing];
    float pulseTotal;
    float pulseHigh;
    float pulseLow;
    float frequencyH;
        
    // Read the wavelength
    for(int i=0; i < smoothing;i++){
        pulseHigh = pulseIn(pin, HIGH);
        pulseLow = pulseIn(pin, LOW);
        pulseTotalArray[i] = pulseHigh + pulseLow;//time in us
    }
    
    // Calculate and return humidity 
    pulseTotal = mean(pulseTotalArray);
    frequencyH = 1000000/pulseTotal;//freq in Hz
    return (-1*(frequencyH - 9595))/14.8;//relative humidity
}

float readTempHTF3228LF(int pin, 
                        float vConvert = 0.0049// analogRead units to volts, 
                        float Vcc = 5//V, 
                        float R1 = 56000//ohm, 
                        float Tn = 298//kelvin, 
                        float B = 3730, 
                        float Rn = 10000//ohm, 
                        float K = 273//kelvin){
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
    // Use datasheet formula to calculate temp in Celcius                    
    return (Tn*B)/(Tn * log(Rt/Rn) + B) - K; //C
}
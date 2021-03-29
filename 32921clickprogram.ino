#include <Wire.h>
#include "Adafruit_DRV2605.h"
#include <math.h>

Adafruit_DRV2605 drv;

// do not re arrange as python takes in a particular way... if you do change make sure to change the assignment/splitpackets in each swarm code
const float LLC = A0;  //Lower load cell = LLC
const int Button = A1;  // Simple on/off Start button
const int LCP1 = A2;  // Load cell precision 1/2 = LCP1
const int analogOutPin = 9; // Analog output pin that the LED is attached to
float sensorValue = 0.;
int sensorValue1 = 0.;
int sensorValue2 = 0.;
int outputValue = 0.;
int increment = 150;

const int numReadings = 2;
int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average
int flag1 = 0;
int sval = 0;
int sval2 = 0;
const int calibfact = analogRead(LLC);
unsigned long previousMillis = 0;
const long interval = 1000; 

void setup() {
  Serial.begin(9600);
  drv.begin();
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}

void loop() {
  sensorValue = analogRead(LLC);
  if (sensorValue<0){
    sensorValue = 0;
  }
  sensorValue = map(sensorValue, calibfact, 1023, 0, 1023);
  sensorValue1 = analogRead(Button);
  sensorValue2 = analogRead(LCP1);

  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = sensorValue;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;
  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }
  // calculate the average:
  average = total / numReadings;

  outputValue = map(average, 0, 1023, 0, 25);
  analogWrite(analogOutPin, outputValue);
  unsigned long currentMillis = millis();


//  if (currentMillis - previousMillis > interval){
    Serial.print("average: ");
    Serial.print(average);
    Serial.print(",");
    Serial.print("Button: ");
    Serial.print(sensorValue1);
    Serial.print(",");
    Serial.print("force: ");
    Serial.print(outputValue);
    Serial.print(",");
    Serial.print("LC2: ");
    Serial.println(sensorValue2);
//  previousMillis = currentMillis;
//  }

  if(average%increment >= 0 && average%increment <= 20 && flag1 == 0){
    sval = float(average/increment);
    if(sval2 = sval){
      Serial.println("Triggered!!!!!!!");
      drv.setWaveform(0,8);
      drv.go();
      flag1 = 1;
    }
  }
  else{
    sval2=float(average/increment);
    Serial.print("Sval2:");
    Serial.print(sval2);
    Serial.print("Sval:");
    Serial.println(sval);
    if(sval2 != sval){
      flag1 = 0;
      Serial.println("sval2 != sval");
    }
  }
  delay(10);
}

#include <Wire.h>
#include "Adafruit_DRV2605.h"

Adafruit_DRV2605 drv;

// do not re arrange as python takes in a particular way... if you do change make sure to change the assignment/splitpackets in each swarm code
const int LLC = A0;  //Lower load cell = LLC
const int Start = A1;  // Simple on/off Start button
const int LCP1 = A2;  // Load cell precision 1/2 = LCP1
const int analogOutPin = 9; // Analog output pin that the LED is attached to
int sensorValue = 0;
int sensorValue1 = 0;
int sensorValue2 = 0;
int outputValue = 0;

void setup() {
  Serial.begin(115200);
  drv.begin();
  
}

void loop() {
  sensorValue = analogRead(LLC);
  sensorValue1 = analogRead(Start);
  sensorValue2 = analogRead(LCP1);
  outputValue = map(sensorValue, 0, 1023, 0, 25);
  analogWrite(analogOutPin, outputValue);
  Serial.print(sensorValue);
  Serial.print(",");
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.print(outputValue);
  Serial.print(",");
  Serial.println(sensorValue2);
  delay(250);

  if(sensorValue < 100) {
    drv.setWaveform(0, 13); 
    drv.go();
  }
  else if(sensorValue > 100 && sensorValue < 300) {
    drv.setWaveform(0,1);
    drv.go();
    
  }
  else if(sensorValue > 300) {
    drv.setWaveform(0,14);
    drv.go();
  }
  else{
    drv.setWaveform(0,1);
    drv.go();
  }
  }
}

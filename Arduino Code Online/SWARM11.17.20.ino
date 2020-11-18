/*
  Smoothing
  Reads repeatedly from an analog input, calculating a running average and
  printing it to the computer. Keeps ten readings in an array and continually
  averages them.
  The circuit:
  - analog sensor (potentiometer will do) attached to analog input 0
  created 22 Apr 2007
  by David A. Mellis  <dam@mellis.org>
  modified 9 Apr 2012
  by Tom Igoe
  This example code is in the public domain.
  http://www.arduino.cc/en/Tutorial/Smoothing
*/

// Define the number of samples to keep track of. The higher the number, the
// more the readings will be smoothed, but the slower the output will respond to
// the input. Using a constant rather than a normal variable lets us use this
// value to determine the size of the readings array.
#include <Servo.h>
const int numReadings = 10;
Servo myservo;  // create servo object to control a servo

int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average
int averageled = 0;
int intLC = 0;
int averageF1 = 0;
int FixedaverageF1 = 0;
int incomingByte;
int val;

int inputPin = A0;
int inputPin1 = A1;
const int ledPin = 5;
const int ledPin1 = 9;
const int buzzer = 2;


void setup() {
  // initialize serial communication with computer:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  intLC = analogRead(inputPin)-10;
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
  myservo.attach(3);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = analogRead(inputPin);
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
  // send it to the computer as ASCII digits
  averageled = map(average,intLC,1023,0,255);
  averageF1 = map(average,intLC,1023,0,25);
  FixedaverageF1 = map(averageF1,0,25,0,25);
  analogWrite(ledPin, averageled);
  //Serial.print("; Running Avg: ");
  Serial.print(average);
  Serial.print(",");
  
    // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == 'H') {
      digitalWrite(ledPin1, HIGH);
      tone(buzzer,831);
    }
    // if it's an L (ASCII 76) turn off the LED:
    if (incomingByte == 'L') {
      digitalWrite(ledPin1, LOW);
      noTone(buzzer);
    }
  }
  
    int range = map(average, 0, 1023, 0, 3);

  // do something different depending on the range value:
  switch (range) {
    case 0:    // your hand is on the sensor
     // Serial.println(" Dark");
      break;
    case 1:    // your hand is close to the sensor
    //  Serial.println(" Dim");
      break;
    case 2:    // your hand is a few inches from the sensor
    //  Serial.println(" Medium");
      break;
    case 3:    // your hand is nowhere near the sensor
     // Serial.println(" Bright");
      break;
  }
  
  val = map(average, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  myservo.write(val);                  // sets the servo position according to the scaled value
 // Serial.print("servo Angle: ");
  Serial.print(val);
  Serial.print(",");
  Serial.println(analogread(A7));
  
  delay(1);        // delay in between reads for stability
}

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h> // include i/o class header

hd44780_I2Cexp lcd; // declare lcd object: auto locate & config display for hd44780 chip
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

/* Returns the IMU data as both a euler angles and quaternions as the WebSerial
   3D Model viewer at https://adafruit-3dmodel-viewer.glitch.me/ expects.
 
   This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2020/JUN/01  - First release (Melissa LeBlanc-Williams)
*/

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(9600);
    // initialize LCD with number of columns and rows:
  lcd.begin(20, 4);

  // Print a message to the LCD
  lcd.print("MTR-SWARM-NPRL");
  Serial.println("WebSerial 3D Firmware"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
   
  delay(1000);

  /* Use external crystal for better accuracy */
  bno.setExtCrystalUse(true);
   
  /* Display some basic information on this sensor */
  displaySensorDetails();
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
    
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 0, 255);
  // change the analog out value:
  analogWrite(analogOutPin, outputValue);

  // print the results to the Serial Monitor:
  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);

  lcd.setCursor(16,0);
  lcd.print(sensorValue);
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Board layout:
         +----------+
         |         *| RST   PITCH  ROLL  HEADING
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+
  */

  /* The WebSerial 3D Model Viewer expects data as heading, pitch, roll */
  Serial.print(F("Orientation: "));
  Serial.print(360 - (float)event.orientation.x);
  Serial.print(F(", "));
  Serial.print((float)event.orientation.y);
  Serial.print(F(", "));
  Serial.print((float)event.orientation.z);
  Serial.println(F(""));

  lcd.setCursor(0, 1);
  lcd.print(360 - (float)event.orientation.x);
  lcd.setCursor(0, 2);
  lcd.print((float)event.orientation.y);
  lcd.setCursor(0, 3);
  lcd.print((float)event.orientation.z);
  

  /* The WebSerial 3D Model Viewer also expects data as roll, pitch, heading */
  imu::Quaternion quat = bno.getQuat();
  
  Serial.print(F("Quaternion: "));
  Serial.print((float)quat.w());
  Serial.print(F(", "));
  Serial.print((float)quat.x());
  Serial.print(F(", "));
  Serial.print((float)quat.y());
  Serial.print(F(", "));
  Serial.print((float)quat.z());
  Serial.println(F(""));

  /* Also send calibration data for each sensor. */
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(F("Calibration: "));
  Serial.print(sys, DEC);
  Serial.print(F(", "));
  Serial.print(gyro, DEC);
  Serial.print(F(", "));
  Serial.print(accel, DEC);
  Serial.print(F(", "));
  Serial.print(mag, DEC);
  Serial.println(F(""));

  delay(BNO055_SAMPLERATE_DELAY_MS);
}

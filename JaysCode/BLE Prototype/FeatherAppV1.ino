#include <HX711_ADC.h>
#include <bluefruit.h>

const int HX711_dout = 5; //mcu > HX711 dout pin
const int HX711_sck = 6; //mcu > HX711 sck pin

HX711_ADC LoadCell(HX711_dout, HX711_sck);
BLEDfu bledfu;
BLEUart bleuart;

const int calVal_eepromAdress = 0;
unsigned long t = 0;

void setup() {
  Serial.begin(57600);
  delay(10);
  Serial.println();
  Serial.println("Starting...");
  delay(10);
  Bluefruit.begin();
  Bluefruit.setTxPower(4); 
  Bluefruit.setName("Bluefruit52");
  bledfu.begin();
  bleuart.begin();
  startAdv();
  
  LoadCell.begin();
  float calibrationValue;
  calibrationValue = 696.0; //I'm autocalibrating

  unsigned long stabilizingtime = 2000;
  boolean _tare = true;
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue);
    Serial.println("Startup is complete");
  }

}

void startAdv(void)
{

  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  
  Bluefruit.Advertising.addService(bleuart);


  Bluefruit.ScanResponse.addName();

  // I'm copying some BLE guidelines for advertising for future reference :P
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);   
  Bluefruit.Advertising.setFastTimeout(30);      
  Bluefruit.Advertising.start(0);                
}


void loop() {
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //Changes serial print rate

  if (LoadCell.update()) newDataReady = true;

  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      Serial.print("Load_cell output val: ");
      Serial.println(i);
      bleuart.print(i);
      bleuart.println();
      newDataReady = 0;
      t = millis();
    }
  }

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay();
  }

  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }

}

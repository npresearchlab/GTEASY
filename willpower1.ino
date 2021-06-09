//Code by: Aswinth Raj Modified and adapted for MTR SWARM by Hyungjun Park
//Date adapted: 6-4-21 for SU21 Swarm

int data;
long randNumber;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //initialization of the Serial communcation at baud of 9600 bts
  pinMode(LED_BUILTIN,OUTPUT);//setting the usual integrated led on arduinos (pin 13s) as an output
  digitalWrite(LED_BUILTIN, LOW);
  randomSeed(analogRead(A0));
  Serial.println("Hi!, I am Arduino Nano");
}//end of setup segment

void loop() {
  while (Serial.available()){
    data = Serial.read();
    }// while loop closed
    if (data == '1'){
    digitalWrite(LED_BUILTIN,HIGH);
    }
    else if (data == '0'){
    digitalWrite(LED_BUILTIN,LOW);
    }
    randNumber = random(1,21); //prints a random numebr from 1 to 20
    Serial.print(analogRead(A1)); //send out data from a sensor
    Serial.print(','); //Input a delimiter for python to break down
    Serial.print(analogRead(A2)); //send out data from a sensor
    Serial.print(',');
    Serial.println(randNumber);
    Serial.flush();
    delay(100);
}//end of loop

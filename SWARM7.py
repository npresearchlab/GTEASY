import serial
import time
arduinoData=serial.Serial('com15',115200)
time.sleep(1)
while (1==1):
    while (arduinoData.inWaiting()==0):
        pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC=str(splitPacket[0])
    X=str(splitPacket[1])
    ledI=str(splitPacket[2])

    #print(dataPacket)

    print('LC=',LC,'X=',X,'Led Brightness=',ledI)
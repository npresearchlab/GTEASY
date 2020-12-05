import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 
import random 

finAvg = 25
analogThreshold = 1000

target_value_upper = (random.randrange(6,int(finAvg))) + 2
target_value_lower = target_value_upper - 4

if target_value_upper > 25:
    target_value_upper = 25
    target_value_lower = 21
print("Target Value: ", target_value_upper-2)

#pull in data
arduinoData=serial.Serial('COM15',115200)
time.sleep(1)
LC2 = 0
start_time_total = time.time()
start_time = time.time() 
timer = 0

def readArduino():
    global LC1, LC2, Force
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1]) # button -- analog read in interval: [0, 2^10)
    Force=int(splitPacket[2])

while True:
    readArduino()
    timer = 0
    started = False
    entered = False
    
    #Init Coundown
    if LC2 > analogThreshold:
        started = True
        #print("Loop if lc2 : ",Force, "Held Time: ",timer)

        while started:
            readArduino()
            #print("LC1:{} LC2:{} Force:{}".format(LC1, LC2, Force))
            
            if Force > target_value_lower and Force < target_value_upper:
                print("YAY")

                if not entered:
                    entered = True
                    timeEntered = time.time()
                    print("///////////////////////////: ",Force, "Held Time: ",timer)

                elif timer > 4:
                    current_time = time.time()
                    print("You passed! Time taken was ",(current_time - start_time_total))
                    break

                else:
                    current_time = time.time()
                    timer = current_time - timeEntered
                    print("Loop running current Force: ",Force, "Held Time: ",timer)
            else:
                print("OOF")
                timer = 0
    
    started = False

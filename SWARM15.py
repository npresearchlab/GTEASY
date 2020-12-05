import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 
import random

arduinoData=serial.Serial('COM11',115200)
time.sleep(1)
LC1 = 0
lst = []
lst2 = []
start_time = time.time()
seconds = 7  
kflag = 0
counter = 1
trialnum = 1

while True:
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1])
    Force=int(splitPacket[2])
    elapsed_time = 0
    start_time = time.time()
    flag = True
    if LC2 > 1000 and elapsed_time == 0 and kflag < 3:
        start_time = time.time()
        while flag:
            if elapsed_time > seconds:
                maxval = max(lst)
                print("////////////// Trial ",trialnum," ended with max force of: ", int(maxval)," lbs")
                flag = False
                kflag += 1
                elapsed_time = 0
                lst = []
                lst2.append(maxval)
                maxval = 0
                counter=1
                trialnum+=1

            else:
                dataPacket=arduinoData.readline()
                dataPacket=str(dataPacket,'utf-8')
                splitPacket=dataPacket.split(',')
                LC1=int(splitPacket[0])
                LC2=int(splitPacket[1])
                Force=int(splitPacket[2])
                #Time Grace Period = 7 seconds
                current_time = time.time()
                elapsed_time = current_time - start_time
                lst.append(Force)
                print("Trial ",trialnum," elapsed_time: ",elapsed_time)
                print('LbForce: ',Force) #'Led Brightness=',ledI   ##'X=',X

    else: 
        if kflag == 3:
            print("////////////// Calibrated Avg Force of 3 Trials: ", sum(lst2)/3, " lbs")
            #Run a def
        if counter == 1:
            print("////////////// Press START to begin calibration of trial ",trialnum,"/3",)
            counter+=1

#def(something)
baseline = finAvg
print(baseline)

i1 = int(0.20) * (baseline)
i2 = int(0.40) * (baseline)
i3 = int(0.60) * (baseline)
i4 = int(0.80) * (baseline)
i5 = baseline



t1test = random.randrange(int(i1),int(i5))
print(t1test)
t1value = int(input("Scale Reading: "))
bfvalue = t1test - t1value
print("Biofeedback: ", bfvalue)

if i1 < t1test < i2 and i1 < t1value < i2:
  print("Match! Go to next test.")
elif i2 < t1test < i3 and i2 < t1value < i3:
  print("Match! Go to next test.")
elif i3 < t1test < i4 and i3 < t1value < i4:
  print("Match! Go to next test.")
elif i4 < t1test < i5 and i4 < t1value < i5:
  print("Match! Go to next test.")
else:
  print("No match! Try again!")
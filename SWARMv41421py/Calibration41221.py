import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

arduinoData=serial.Serial('COM18', 9600, timeout=0)
time.sleep(1)


def calib():
    LC1 = 0
    lst = []
    lst2 = []
    start_time = time.time()
    seconds = 7
    counter = 1
    trialnum = 1
    kflag = 0
    while True:
        dataPacket=arduinoData.readline()
        dataPacket=str(dataPacket,'utf-8')
        splitPacket=dataPacket.split(',')
        LC1=int(splitPacket[3])
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
                    print("////////////// Trial ", trialnum, " ended with max force of: ", int(maxval), " lbs")
                    flag = False
                    kflag += 1
                    elapsed_time = 0
                    lst = []
                    lst2.append(maxval)
                    maxval = 0
                    counter = 1
                    trialnum += 1
                else:
                    dataPacket=arduinoData.readline()
                    dataPacket=str(dataPacket, 'utf-8')
                    splitPacket=dataPacket.split(',')
                    LC1=int(splitPacket[0])
                    LC2=int(splitPacket[1])
                    Force=int(splitPacket[2])
                    #Time Grace Period = 7 seconds
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    lst.append(Force)
                    print("Trial ", trialnum, " elapsed_time: ", elapsed_time)
                    print('LbForce: ', Force)  #'Led Brightness=',ledI   ##'X=',X
        else:
            if kflag == 3:
                print("////////////// Calibrated Avg Force of 3 Trials: ", sum(lst2)/3, " lbs")
                # serial.Serial.close(self=)
                arduinoData.close()
                return sum(lst2) / 3
            if counter == 1:
                print("////////////// Press START to begin calibration of trial ", trialnum, "/3")
                counter += 1


if __name__ == '__main__':
    calib()
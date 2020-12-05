import time
import serial
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
from matplotlib.animation import FuncAnimation
import numpy as np 
import random

arduinoData=serial.Serial('COM15',115200)

time.sleep(1)
LC1 = 0
lst = []
lst2 = []
start_time = time.time()
seconds = 7
kflag = 0

#this is for the target circle
plt.style.use('fivethirtyeight')
r1 = random.uniform(5,22)
th1 = np.linspace(0,2 * np.pi,num=100)
x1 = r1 * np.cos(th1)
y1 = r1 * np.sin(th1)
def animate(i):
    global lst
    th = np.linspace(0,2 * np.pi,num=100)
    r = lst[-1]
    x = r * np.cos(th)
    y = r * np.sin(th)
    plt.cla()
    plt.plot(x,y, label='Force')
    plt.plot(x1,y1, label='Target')
    plt.legend(loc ='upper left')

while (1==1):
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1])
    Force=int(splitPacket[2])
    elapsed_time = 0
    start_time = time.time()
    flag = True
    if LC2 > 600 and elapsed_time == 0 and kflag < 3:
        start_time = time.time()
        while flag:
            
            if elapsed_time > seconds:
                maxval = max(lst)
                print("Trial ended with max force of: " + str(int(maxval))  + " lbs")
                flag = False
                kflag += 1
                elapsed_time = 0
                lst = []
                lst2.append(maxval)
                maxval = 0

            else:
                print("SOMETHING IN WORDS")
                dataPacket=arduinoData.readline()
                dataPacket=str(dataPacket,'utf-8')
                splitPacket=dataPacket.split(',')
                LC1=int(splitPacket[0])
                LC2=int(splitPacket[1])
                Force=int(splitPacket[2])
                #Time Grace Period = 7 seconds
                current_time = time.time()
                elapsed_time = current_time - start_time
                print(elapsed_time)
                lst.append(Force)
                print('LC1: ',LC1,'startButton: ',LC2,'LbForce: ',Force) #'Led Brightness=',ledI   ##'X=',X
                #print(lst)
            
            
            ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
            plt.axis('equal')
            plt.tight_layout()
            plt.show()       
                

            print(elapsed_time)

    else: 

        print("Press start to begin calibration. ")
        if kflag == 3:
            print("Max Avg Force: ", sum(lst2)/3)
            break
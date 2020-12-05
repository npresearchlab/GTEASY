import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np 
import random 
import multiprocessing

finAvg = 25
analogThreshold = 1000

target_value = random.uniform(6,20)
target_value_upper = target_value + 2
target_value_lower = target_value - 2
#the circle to plot

# upper range
r_upper = target_value_upper
th = np.linspace(0,2 * np.pi, num=100)
x_upper = r_upper * np.cos(th)
y_upper = r_upper * np.sin(th)
# lower range
r_lower = target_value_lower
x_lower = r_lower * np.cos(th)
y_lower = r_lower * np.sin(th)



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


def readArduino():
    global LC1, LC2, Force
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1]) # button -- analog read in interval: [0, 2^10)
    Force=int(splitPacket[2])


timeE = []
count = 0
def animate(i):
    global timeE, count
    th = np.linspace(0,2 * np.pi,num=100)
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    r = int(splitPacket[2])
    x = r * np.cos(th)
    y = r * np.sin(th)
    plt.cla()
    plt.plot(x,y)
    plt.plot(x_upper,y_upper)
    plt.plot(x_lower,y_lower)
    plt.axis('equal')
    readArduino()
    started = False
    
            
    if Force > target_value_lower and Force < target_value_upper:
        
        print("YAY")

        if Force > target_value_lower and Force < target_value_upper:
            
            timeEntered = time.time()
            timeE = np.append(timeE,timeEntered)
            print("///////////////////////////: ",Force, "Held Time: ",count)
            count = count + 1
            if count == 15:
                print("You passed! Time taken was ",count)
                exit()

        elif timer > 4:
            current_time = time.time()
            print("You passed! Time taken was ",(count))
            exit()

        else:
            current_time = time.time()
            timer = current_time - timeE[1]
            print("Loop running current Force: ",Force, "Held Time: ",timer)
    else:
        print("OOF")
        timeE = []
        count = 0
        
    
ani = FuncAnimation(plt.gcf(), animate, interval=50)
plt.tight_layout()
plt.show() 

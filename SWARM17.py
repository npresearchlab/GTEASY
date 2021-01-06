import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np 
import random 
import multiprocessing

from typing import Tuple

finAvg = 25
analogThreshold = 1000


def get_target_values():
    target_value = random.uniform(6,20)
    target_value_upper = target_value + 2
    target_value_lower = target_value - 2
    #the circle to plot

    # upper range
    # r_upper = target_value_upper
    # th = np.linspace(0,2 * np.pi, num=100)
    # x_upper = r_upper * np.cos(th)
    # y_upper = r_upper * np.sin(th)
    # # lower range
    # r_lower = target_value_lower
    # x_lower = r_lower * np.cos(th)
    # y_lower = r_lower * np.sin(th)

    if target_value_upper > 25:
        target_value_upper = 25
        target_value_lower = 21
    print("Target Value: ", target_value_upper-2)

    return target_value_lower, target_value_upper


def get_circle_values(radius: int) -> Tuple[float, float]:
    th = np.linspace(0,2 * np.pi, num=100)
    return radius * np.cos(th), radius * np.sin(th)


#pull in data
arduinoData=serial.Serial('COM5',115200)
time.sleep(1)
# LC2 = 0
# start_time_total = time.time()
# start_time = time.time() 


def readArduino() -> Tuple[int, int, int]:
    # global LC1, LC2, Force
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=[int(x) for x in dataPacket.split(',')]
    return splitPacket[:3]  # LC1, LC2, Force
    # LC1=int(splitPacket[0])
    # LC2=int(splitPacket[1]) # button -- analog read in interval: [0, 2^10)
    # Force=int(splitPacket[2])


timeE = []
count = 0
target_value_lower, target_value_upper = None, None

def animate(i):
    global timeE, count, target_value_lower, target_value_upper
    th = np.linspace(0,2 * np.pi,num=100)
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    r = int(splitPacket[2])
    x = r * np.cos(th)
    y = r * np.sin(th)
    plt.cla()
    plt.plot(x,y)
    x_lower, y_lower = get_circle_values(target_value_lower)
    x_upper, y_upper = get_circle_values(target_value_upper)
    plt.plot(x_upper,y_upper)
    plt.plot(x_lower,y_lower)
    plt.axis('equal')
    LC1, LC2, Force = readArduino()

    if target_value_lower < Force < target_value_upper:        
        print("YAY")
        timeEntered = time.time()
        timeE = np.append(timeE,timeEntered)
        print("///////////////////////////: ",Force, "Held Time: ",count)
        count = count + 1
        if count == 15:
            print("You passed! Time taken was ",count)
            plt.close()
    else:
        print("OOF")
        timeE = []
        count = 0
        

def input_simulator():
    global count, target_value_lower, target_value_upper
    start_time = time.time()
    target_value_lower, target_value_upper = get_target_values()
    ani = FuncAnimation(plt.gcf(), animate, interval=50)
    plt.tight_layout()
    plt.show()
    end_time = time.time()
    return end_time - start_time
    # plt.show(block=False)
    # while count < 15:
    #     print(count)
    # plt.close()


if __name__ == '__main__':
    input_simulator()

import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from typing import Tuple

finAvg = 25
analogThreshold = 1024
# def get_calibrated():
# WORK ON TRANSFERING CALIBRATION OVER


def get_target_values():
    target_value = random.uniform(3, finAvg)
    target_value_upper = target_value + 2
    target_value_lower = target_value - 2
    if target_value_upper > 25:
        target_value_upper = 25
        target_value_lower = 21
   #print("Target Value: ", target_value_upper - 2)
    return target_value_lower, target_value_upper


def get_circle_values(radius: int) -> Tuple[float, float]:
    th = np.linspace(0, 2 * np.pi, num=100)
    return radius * np.cos(th), radius * np.sin(th)


# pull in data
arduinoData = serial.Serial('COM18', 9600)
time.sleep(1)


def readArduino() -> Tuple[int, int, int, int]:
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, 'utf-8')
    splitPacket = [int(x) for x in dataPacket.split(',')]
    return splitPacket[:4]  # LLC, Start, LbfForce, LCP1


Force = 0
c = 1
timeE = time.time()
timeEntered = []
target_value_lower, target_value_upper = None, None


def animate(i):
    global timeE, target_value_lower, target_value_upper, Force, c, timeEntered, end_time
    LLC, Start, Force, LCP1 = readArduino()
    th = np.linspace(0, 2 * np.pi, num=100)
    x = int(Force) * np.cos(th)
    y = int(Force) * np.sin(th)
    plt.cla()
    plt.title(str(Force))
    plt.plot(x, y)  # check out
    # plt.plot(1, i)
    x_lower, y_lower = get_circle_values(target_value_lower)
    x_upper, y_upper = get_circle_values(target_value_upper)
    plt.plot(x_upper, y_upper)
    plt.plot(x_lower, y_lower)
    plt.axis('equal')
    if target_value_lower < Force < target_value_upper:
        if c == 1:
            timeEntered = time.time()
            c = 0
        timeE = time.time()
        #print("GOOD", Force, timeE, timeEntered, timeE - timeEntered)
        if timeE-timeEntered >= 5:
            plt.close()
            end_time = time.time()
    else:
        #print("not in range", Force, timeE)
        c = 1


def input_simulator():
    global target_value_lower, target_value_upper, end_time
    start_time = time.time()
    target_value_lower, target_value_upper = get_target_values()
    ani = FuncAnimation(plt.gcf(), animate, frames=np.arange(0, 100, 1), interval=10)
    plt.tight_layout()
    plt.show()
    print("You passed! Time taken was ", str(end_time - start_time))
    return (end_time - start_time)


if __name__ == '__main__':
    input_simulator()
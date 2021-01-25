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
#WORK ON TRANSFERING CALIBRATION OVER

def get_target_values():
    target_value = random.uniform(6, 20)
    target_value_upper = target_value + 2
    target_value_lower = target_value - 2
    if target_value_upper > 25:
        target_value_upper = 25
        target_value_lower = 21
    print("Target Value: ", target_value_upper - 2)
    return target_value_lower, target_value_upper


def get_circle_values(radius: int) -> Tuple[float, float]:
    th = np.linspace(0, 2 * np.pi, num=100)
    return radius * np.cos(th), radius * np.sin(th)


# pull in data
arduinoData = serial.Serial('COM5', 9600)
time.sleep(1)


def readArduino() -> Tuple[int, int, int, int]:
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, 'utf-8')
    splitPacket = [int(x) for x in dataPacket.split(',')]
    return splitPacket[:4]  # LLC, Start, LbfForce, LCP1


timeE = []
count = 0
target_value_lower, target_value_upper = None, None


def animate(i):
    global timeE, count, target_value_lower, target_value_upper
    th = np.linspace(0, 2 * np.pi, num=100)
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, 'utf-8')
    splitPacket = dataPacket.split(',')
    r = int(splitPacket[2])
    x = r * np.cos(th)
    y = r * np.sin(th)
    plt.cla()
    plt.plot(x, y)
    x_lower, y_lower = get_circle_values(target_value_lower)
    x_upper, y_upper = get_circle_values(target_value_upper)
    plt.plot(x_upper, y_upper)
    plt.plot(x_lower, y_lower)
    plt.axis('equal')
    LLC, Start, Force, LCP1 = readArduino()

    if target_value_lower < Force < target_value_upper:
        print("YAY")
        timeEntered = time.time()
        timeE = np.append(timeE, timeEntered)
        print("///////////////////////////: ", Force, "Held Time: ", count)
        count = count + 1
        if count == 15:
            print("You passed! Time taken was ", count)
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


if __name__ == '__main__':
    input_simulator()

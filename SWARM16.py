import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np 
import random 
from drawnow import *

finAvg = 25
analogThreshold = 1000

# style.use('fivethirtyeight')
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     global Force, graph_data
#     graph_data = Force

#     ax1.clear()
#     ax1.plot(Force*np.cos(th),Force*np.sin(th))



target_value = random.uniform(6,16)
target_value_upper = target_value + 2
target_value_lower = target_value - 2
#the circle to plot
fig, ax = plt.subplots()
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
timer = 0
tickmark =0

def readArduino():
    global LC1, LC2, Force
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1]) # button -- analog read in interval: [0, 2^10)
    Force=int(splitPacket[2])

def makeFig():
    th = np.linspace(0,2 * np.pi,num=100)
    r = Force
    x = r * np.cos(th)
    y = r * np.sin(th)
    plt.cla()
    # plt.plot(Force*np.cos(th),Force*np.sin(th),'r')
    plt.plot(x_upper,y_upper,label='Upper Target')
    plt.plot(x_lower,y_lower,label='Lower Target')
    plt.plot(x,y, label='Current Force')
    plt.legend(loc ='upper left')
    plt.axis('equal')

# def animate(i):
#     th = np.linspace(0,2 * np.pi,num=100)
#     r = Force
#     x = r * np.cos(th)
#     y = r * np.sin(th)
#     plt.cla()
#     plt.plot(x_upper,y_upper,label='Upper Target')
#     plt.plot(x_lower,y_lower,label='Lower Target')
#     plt.plot(x,y, label='Current Force')
#     plt.legend(loc ='upper left')



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
            
            # drawnow(makeFig)
            # plt.pause(0.000001)
            if tickmark == 1:
                drawnow(makeFig)
                plt.pause(0.0000001)
                tickmark = 0
            else:
                tickmark +=1
            
            
            if Force > target_value_lower and Force < target_value_upper:
                # ani = animation.FuncAnimation(fig, animate, interval=1000)
                # plt.axis('equal')
                # plt.show()
                
                print("YAY",Force)

                if not entered:
                    entered = True
                    timeEntered = time.time()
                    print("///////////////////////////: ",Force, "Held Time: ",timer)

                elif timer > 15:
                    current_time = time.time()
                    print("You passed! Time taken was ",(current_time - start_time_total))
                    break

                else:
                    current_time = time.time()
                    timer = current_time - timeEntered
                    print("Loop running current Force: ",Force, "Held Time: ",timer)
            else:
                print("OOF",Force)
                timer = 0
    started = False

# importing required modules 
import serial
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 


arduinoData=serial.Serial('COM15',115200)
LC1 = 0


while True:
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1])
    i=int(splitPacket[2])
    # create a figure, axis and plot element 
    fig = plt.figure() 
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50)) 
    line, = ax.plot([], [], lw=2) 

    # initialization function 
    def init(): 
        # creating an empty plot/frame 
        line.set_data([], []) 
        return line, 

    # lists to store x and y axis points 
    xdata, ydata = [], [] 

    # animation function 
    def animate(i): 
        # t is a parameter 
        t = 0.1*i 
        
        # x, y values to be plotted 
        x = t*np.sin(t) 
        y = t*np.cos(t) 
        
        # appending new points to x, y axes points list 
        xdata.append(x) 
        ydata.append(y) 
        
        # set/update the x and y axes data 
        line.set_data(xdata, ydata) 
        
        # return line object 
        return line, 
        
    # setting a title for the plot 
    plt.title('A growing coil!') 
    # hiding the axis details 
    plt.axis('off')
    # show the plot 
    plt.show()
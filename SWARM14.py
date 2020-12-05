import serial
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 

arduinoData=serial.Serial('COM15',115200)
time.sleep(1)
LC1 = 0
lst = []
lst2 = []
start_time = time.time()
seconds = 7  
kflag = 0

while (1==1):
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(',')
    LC1=int(splitPacket[0])
    LC2=int(splitPacket[1])
    Force=int(splitPacket[2])
    elapsed_time = 0
    flag = True
    if LC2 > 600 and elapsed_time == 0 and kflag < 4:
            while flag:
                if elapsed_time > seconds:
                    maxval = max(lst)
                    print("Trial ended with max force of: " + str(int(maxval))  + " lbs")
                    flag = False
                    kflag = kflag + 1
                    elapsed_time = 0
                    start_time = time.time()
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
                print(elapsed_time)

    else: 
        print("Press start to begin calibration. ")
        print(elapsed_time)
        
        
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

# call the animator	 
anim = animation.FuncAnimation(fig, animate, init_func=init, 
							frames=500, interval=20, blit=True) 

# save the animation as mp4 video file 
anim.save('animated_coil.mp4', writer = 'ffmpeg', fps = 30) 

# show the plot 
plt.show() 
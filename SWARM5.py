import time
import csv
import pytz
import serial
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
from time import gmtime, strftime
from datetime import datetime
from pytz import timezone

est = timezone('EST')
ser = serial.Serial('COM15','115200')
ser.flushInput()

plot_window = 80
y_var = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(y_var)

while True:
    try:
        ser_bytes = ser.readline()
        try:
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            print(decoded_bytes)
        except:
            continue
        with open("RichyPyUse.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([datetime.now(est),decoded_bytes])
            y_var = np.append(y_var,decoded_bytes)
            y_var = y_var[1:plot_window+1]
            line.set_ydata(y_var)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
    except:
        print("Keyboard Interrupt")
        break
import serial
from matplotlib import pyplot, animation

WINDOW = 400
NSAMPLES = 400
REFRESH = 1

port = serial.Serial('COM15', 115200)
figure = pyplot.figure()
subplot = figure.add_subplot(1, 1, 1)
data = [0] * WINDOW

def draw(i, data):
    data.extend([
        int.from_bytes(port.read(2), byteorder='little', signed=True)
        for i in range(NSAMPLES)
    ])
    subplot.clear()
    subplot.plot(data[-WINDOW:])

ani = animation.FuncAnimation(figure, draw, fargs=(data,), interval=REFRESH)
pyplot.show()
import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200
ser.timeout = 1

tanTheta = 0.4434

fig = plt.figure()
data = np.full((2, 2), 113)
im = plt.imshow(data, cmap='magma', vmin=10, vmax=113)
plt.colorbar(fraction=0.1, pad=0.04)

nx = 2
ny = 2


def init():
    im.set_data(np.zeros((8, 8)))


def animate(i):
    xi = i // ny
    yi = i % ny

    ser.flushInput()
    ser.flushOutput()

    ser_bytes = ser.readline()
    ser_string = ser_bytes.decode("utf-8")
    ser_list = ser_string.split(",")

    try:
        if int(ser_list[0]) == 0:
            x1 = int(ser_list[1])
            if x1 > 113:
                x1 = 113
        else:
            x1 = 113

        if ser_list[2] == '0':
            x2 = int(ser_list[3])
            if x2 > 113:
                x2 = 113
        else:
            x2 = 113

        if ser_list[4] == '0':
            x3 = int(ser_list[5])
            if x3 > 113:
                x3 = 113
        else:
            x3 = 113

        if ser_list[6] == '0':
            x4 = int(ser_list[7])
            if x4 > 113:
                x4 = 113
        else:
            x4 = 113

        result = np.array([[x2, x1], [x4, x3]])
        data = result
        im.set_data(data)

    except:
        print("Error Read Data")


anim = animation.FuncAnimation(fig, animate, init_func=init)
plt.show()


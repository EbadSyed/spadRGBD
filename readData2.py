import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200
ser.timeout = 1

tanTheta = 0.4434

fig = plt.figure()
data = np.full((8, 8), 113)
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

        area1 = int((x1 * tanTheta) / 10)

        if area1 == 0:
            area1 = 1

        a1 = np.full((5, 5), 113)

        diff1 = int((5 - area1) / 2)

        for x in range(area1):
            for y in range(area1):
                a1[x + diff1, y + diff1] = x1

        area2 = int((x2 * tanTheta) / 10)

        if area2 == 0:
            area2 = 1

        a2 = np.full((5, 5), 113)

        diff2 = int((5 - area2) / 2)

        print("Area + Diff :" + str(area2) + " " + str(diff2))

        for x in range(area2):
            for y in range(area2):
                a2[x + diff2, y + diff2] = x2

        area3 = int((x3 * tanTheta) / 10)

        if area3 == 0:
            area3 = 1

        a3 = np.full((5, 5), 113)

        diff3 = int((5 - area3) / 2)

        for x in range(area3):
            for y in range(area3):
                a3[x + diff3, y + diff3] = x3

        area4 = int((x4 * tanTheta) / 10)

        if area4 == 0:
            area4 = 1

        a4 = np.full((5, 5), 113)

        diff4 = int((5 - area4) / 2)

        for x in range(area4):
            for y in range(area4):
                a4[x + diff4, y + diff4] = x4

        a1a2 = np.concatenate([a2, a1], axis=1)
        a3a4 = np.concatenate([a4, a3], axis=1)

        result = np.concatenate([a1a2, a3a4])
        result = np.delete(result, 0, 0)
        result = np.delete(result, 8, 0)
        result = np.delete(result, 0, 1)
        result = np.delete(result, 8, 1)

        data = result
        im.set_data(data)

    except:
        print("Error Read Data")


anim = animation.FuncAnimation(fig, animate, init_func=init)
plt.show()


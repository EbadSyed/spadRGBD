import serial
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from time import sleep

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate=115200
ser.timeout = 1

tanTheta = 0.4434

while True:
    ser.flushInput()
    ser.flushOutput()
    sleep(0.2)
    ser_bytes = ser.readline()
    ser_string = ser_bytes.decode("utf-8")
    ser_list = ser_string.split(",")

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

    area1 = int(x1 * tanTheta)
    a1 = np.full((50, 50), 113)

    if area1 % 2 != 0:
        area1 = area1 + 1

    diff1 = int((50 - area1) / 2)

    for x in range(area1):
        for y in range(area1):
            a1[x + diff1, y + diff1] = x1

    area2 = int(x2 * tanTheta)
    a2 = np.full((50, 50), 113)

    if area2 % 2 != 0:
        area2 = area2 + 1

    diff2 = int((50 - area2) / 2)

    for x in range(area2):
        for y in range(area2):
            a2[x + diff2, y + diff2] = x2

    area3 = int(x3 * tanTheta)
    a3 = np.full((50, 50), 113)

    if area3 % 2 != 0:
        area3 = area3 + 1

    diff3 = int((50 - area3) / 2)

    for x in range(area3):
        for y in range(area3):
            a3[x + diff3, y + diff3] = x3

    area4 = int(x4 * tanTheta)
    a4 = np.full((50, 50), 113)

    if area4 % 2 != 0:
        area4 = area4 + 1

    diff4 = int((50 - area4) / 2)

    for x in range(area4):
        for y in range(area4):
            a4[x + diff4, y + diff4] = x4

    # plt.subplot(221)
    # plt.imshow(a1)
    # plt.colorbar(fraction=0.1, pad=0.04)
    #
    # plt.subplot(222)
    # plt.imshow(a2)
    # plt.colorbar(fraction=0.1, pad=0.04)
    #
    # plt.subplot(223)
    # plt.imshow(a3)
    # plt.colorbar(fraction=0.1, pad=0.04)
    #
    # plt.subplot(224)
    # plt.imshow(a4)
    # plt.colorbar(fraction=0.1, pad=0.04)

    a1a2 = np.concatenate([a1, a2], axis=1)
    a3a4 = np.concatenate([a3, a4], axis=1)

    result = np.concatenate([a1a2,a3a4])

    plt.imshow(result,cmap='magma',vmin=10,vmax=113)
    plt.colorbar(fraction=0.1, pad=0.04)
    plt.waitforbuttonpress()
    plt.close()




import time
import sys
import signal

import VL53L1X

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Open and start the VL53L1X sensor.
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(3)

running = True


def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging()
    print()
    sys.exit(0)


# Attach a signal handler to catch SIGINT (Ctrl+C) and exit gracefully
signal.signal(signal.SIGINT, exit_handler)

roi = []

for y in range(4):
    for x in range(4):
        roi.append(VL53L1X.VL53L1xUserRoi(x*4, 15 - y*4, x*4+3, 15 - 3 - y*4))


fig = plt.figure()
data = np.zeros((4, 4))
im = plt.imshow(data,cmap='magma',vmin=0,vmax=2400)
plt.colorbar(fraction=0.1, pad=0.04)


def init():
    im.set_data(np.zeros((4, 4)))


def animate(iter):

    i = 0

    for x in range(4):
        for y in range(4):
            tof.set_user_roi(roi[i])
            tof.start_ranging(0)
            data[x,y] = tof.get_distance()
            tof.stop_ranging()
          
    im.set_data(data)


anim = animation.FuncAnimation(fig, animate, init_func=init)
plt.show()

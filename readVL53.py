import time
import sys
import signal

import qwiic_vl53l1x

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Open and start the VL53L1X sensor.
tof = qwiic_vl53l1x.QwiicVL53L1X()

if tof.sensor_init() is None:  # Begin returns 0 on a good init
    print("Sensor online!\n")


def exit_handler(signal, frame):
    tof.stop_ranging()
    print("Exiting Now")
    sys.exit(0)


# Attach a signal handler to catch SIGINT (Ctrl+C) and exit gracefully
signal.signal(signal.SIGINT, exit_handler)

# Sets Distance Mode Short=1 Long=2
tof.set_distance_mode(1)

data = np.zeros((1, 2), dtype=np.uint8 )

center = [167, 231]

fig = plt.figure()
im = plt.imshow(data, cmap='magma', vmin=0, vmax=2400)
plt.colorbar(fraction=0.1, pad=0.04)


def init():
     im.set_data(np.zeros((2, 2), dtype=np.uint8))


def animate(iter):

    for x in range(2):
        tof.set_roi_size(8, 16)
        time.sleep(.005)
        tof.set_roi_center(center[x])
        time.sleep(.005)
        tof.start_ranging()
        time.sleep(.005)
        data[0, x] = tof.get_distance()
        print(data[0, x])
        tof.stop_ranging()

    im.set_data(data)


anim = animation.FuncAnimation(fig, animate, init_func=init)
plt.show()

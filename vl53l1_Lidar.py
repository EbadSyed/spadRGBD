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

data = np.zeros((4, 4), dtype=np.uint16 )

center = np.array([(145, 177, 209, 241), (149, 181, 213, 245), (110, 78, 46, 14), (106, 74, 42, 10)])

#multiple = np.array([(0.85)]) 

print("Center ROI")
print(center)

tof.set_roi_size(4, 4)
# TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
tof.set_timing_budget_in_ms(50)
# Intermeasurement period must be >/= timing budget
tof.set_inter_measurement_in_ms(51)

# verify roi
# for ytest in range(4):
#     for xtest in range(4):
#         print(center[xtest, ytest])
#         print(tof.set_roi_center(center[xtest, ytest]))
#         time.sleep(0.3)


fig = plt.figure()
im = plt.imshow(data , vmin=0, vmax=1000)
plt.colorbar(fraction=0.1, pad=0.04)


def init():
     im.set_data(np.zeros((4, 4), dtype=np.uint16))


tof.start_ranging()

start_time = time.time()
dataReady = 0
# while True:
def animate(i):
    global start_time, dataReady

    for x in range(4):
        for y in range(4):
            tof.set_roi_center(center[x, y])
            #time.sleep(0.04)
            tof.start_ranging()
            while dataReady == 0:
                dataReady = tof.check_for_data_ready()
            dataReady = 0
            data[x, y] = tof.get_distance()
            tof.clear_interrupt()
            tof.stop_ranging()
    print("Execution Time : " + str(time.time()-start_time))
    start_time = time.time()
    print(data)
    im.set_data(data)

anim = animation.FuncAnimation(fig, animate, init_func=init)
plt.show()

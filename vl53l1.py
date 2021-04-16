import time
import sys
import signal

import qwiic_vl53l1x

import numpy as np

file1 = open("myfile.txt", "a")  
  

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

center = np.array([(145, 177, 209, 241), (149, 181, 213, 245), (110, 78, 46, 14), (106, 74, 42, 18)])

# tof.set_roi_center()

tof.set_roi_size(4, 4)
# TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
tof.set_timing_budget_in_ms(20)
# Intermeasurement period must be >/= timing budget
tof.set_inter_measurement_in_ms(22)

tof.start_ranging()


for d in range(200):
    for x in range(4):
            for y in range(4):
                tof.set_roi_center(center[x, y])
                time.sleep(0.005)
                dataReady = 0
                while dataReady == 0:
                    dataReady = tof.check_for_data_ready()
                data[x, y] = tof.get_distance()
                file1.write(str(data[x,y]))
                file1.write(",")
                tof.clear_interrupt()
    file1.write("\n")
    print(data)
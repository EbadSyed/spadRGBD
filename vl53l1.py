import time
import sys
import signal

import qwiic_vl53l1x

import numpy as np
import matplotlib.pyplot as plt
import math

from mpl_toolkits import mplot3d

import busio
from adafruit_pca9685 import PCA9685
from ServoKit import *
from board import *

# file1 = open("data400.txt", "a")  
  
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

servoKit = ServoKit(2)

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

# Create an empty array for data
data = np.zeros((4, 4),dtype=np.int32)
pcl = np.array([0,0,0])

# ROI Center Value
center = np.array([(145, 177, 209, 241), (149, 181, 213, 245), (110, 78, 46, 14), (106, 74, 42, 10)])

# Angle values for ROI
vert = np.array([(-22,-22,-22,-22),(-15,-15,-15,-15),(15,15,15,15),(22,22,22,22)])
horz = np.array([(-22,-15,15,22),(-22,-15,15,22),(-22,-15,15,22),(-22,-15,15,22)])

# Offset Values for ROI
offset = np.array([(17,26,23,27),(30,48,45,22),(29,45,40,19),(24,25,19,17)])

# phi = 90
# theta = 90

# tof.set_roi_center()

# Set ROI Size
tof.set_roi_size(4, 4)
# TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
tof.set_timing_budget_in_ms(50)
# Intermeasurement period must be >/= timing budget
tof.set_inter_measurement_in_ms(52)

# Initialize Plot
plt.imshow(data,vmin=0, vmax=600)
plt.colorbar(fraction=0.1, pad=0.04)

dataReady = 0

# Scan the values by setting values for Phi and Theta
for phi in range(60,125,15):
    for theta in range(65,135,15):
        servoKit.setAngle(0,theta)
        servoKit.setAngle(1,phi)
        time.sleep(1)
        # Scan the complete roi
        for x in range(4):
            for y in range(4):
                tof.set_roi_center(center[x, y])
                tof.start_ranging()
                while dataReady == 0:
                    dataReady = tof.check_for_data_ready()
                dataReady = 0
                p = tof.get_distance()
                # Get the actual angle
                actTheta = servoKit.getAngle(0)
                actPhi = servoKit.getAngle(1)
                # Convert to xyz coordinate
                y1 = int((p+offset[x,y])*math.sin(math.radians(vert[x,y]+actTheta))*math.sin(math.radians(horz[x,y]+actPhi))) 
                x1 = int((p+offset[x,y])*math.sin(math.radians(vert[x,y]+actTheta))*math.cos(math.radians(horz[x,y]+actPhi)))
                z1 = int((p+offset[x,y])*math.cos(math.radians(vert[x,y]+actTheta)))
                data[x, y] = y1
               
                pclB = np.array([x1,y1,z1])
                pcl = np.vstack((pcl,pclB))
                # file1.write(",")
                tof.clear_interrupt()
                tof.stop_ranging()
        # file1.write("\n")
        print(data)
        plt.imshow(data,vmin=0, vmax=600)
        plt.waitforbuttonpress(0.001)
                
plt.close()

ax = plt.axes(projection='3d')
ax.scatter(pcl[:,0], pcl[:,1], pcl[:,2],c='r', marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
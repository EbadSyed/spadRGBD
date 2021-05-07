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

file1 = open("dataPoints4.txt", "a")  
  
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

# Offset Values for ROI
#offset = np.array([(17,26,23,27),(30,48,45,22),(29,45,40,19),(24,25,19,17)])
offset = 40

# Set ROI Size
tof.set_roi_size(4, 4)
# TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
tof.set_timing_budget_in_ms(50)
# Intermeasurement period must be >/= timing budget
tof.set_inter_measurement_in_ms(52)


dataReady = 0

# Scan the values by setting values for Phi and Theta
for phi in range(60,125,5):
    for theta in range(80,135,5):
        servoKit.setAngle(0,theta)
        servoKit.setAngle(1,phi)
        time.sleep(1)
        # Scan the complete roi
        tof.start_ranging()
        while dataReady == 0:
            dataReady = tof.check_for_data_ready()
        dataReady = 0
        p = tof.get_distance()
        # Get the actual angle
        actTheta = servoKit.getAngle(0)
        actPhi = servoKit.getAngle(1)
        # Convert to xyz coordinate
        y1 = int((p+offset)*math.sin(math.radians(actTheta))*math.sin(math.radians(actPhi))) 
        x1 = int((p+offset)*math.sin(math.radians(actPhi))*math.cos(math.radians(actTheta)))
        z1 = int((p+offset)*math.cos(math.radians(actPhi)))
        
        print("Horz",actTheta,"Vert",actPhi)
        print("p1,x1,y1,z1",p+offset,x1,y1,z1)       
        pclB = np.array([x1,y1,z1])
        pcl = np.vstack((pcl,pclB))
        dataString = str(x1) + "," + str(y1) + "," + str(z1)
        file1.write(dataString)
        tof.clear_interrupt()
        tof.stop_ranging()
        file1.write("\n")
        
ax = plt.axes(projection='3d')
ax.scatter(pcl[:,0], pcl[:,1], pcl[:,2],c='r', marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
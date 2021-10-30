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

file1 = open("dataPoints7.txt", "a")  

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
data = np.zeros((13, 13))
pcl = np.array([0,0,0])


# ROI Center Value
center = np.array([(145, 153, 161, 169 , 177, 185, 193, 201, 209, 217, 225, 233,  241),(146,154,162,170,178,186,194,202,210,218,226,234,242),(147,155,163,171,179,187,195,203,211,219,227,235,243),(148,156,164,172,180,188,196,204,212,220,228,236,244), (149, 157, 165 , 173, 181, 189, 197, 205, 213, 221, 229, 237, 245),(150,158,166,174,182,190,198,206,214,222,230,238,246),(151,159,167,175,183,191,199,207,215,223,231,239,247),(111,103,95,87,79,71,63,55,47,39,31,23,15), (110, 102, 94, 86, 78, 70, 62, 54, 46, 38, 30, 22, 14),(109,101,93,85,77,69,61,53,45,37,29,21,13),(108,100,92,84,76,68,60,52,44,36,28,20,12),(107,99,91,83,75,67,59,51,43,35,27,19,11), (106, 98, 90, 82, 74, 66, 58, 50, 42, 34, 26, 18, 10)])

# Angle values for ROI
vert = np.array([(-22,-22,-22,-22,-22,-22,-22,-22,-22,-22,-22,-22,-22),(-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19),(-15,-15,-15,-15,-15,-15,-15,-15,-15,-15,-15,-15,-15),(-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11,-11),(-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8),( -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4),( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),( 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),(8,8,8,8,8,8,8,8,8,8,8,8,8),(11,11,11,11,11,11,11,11,11,11,11,11,11),(15,15,15,15,15,15,15,15,15,15,15,15,15),(19,19,19,19,19,19,19,19,19,19,19,19,19),(22,22,22,22,22,22,22,22,22,22,22,22,22)])
horz = np.array([(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22),(-22,-19,-15,-11,-8,-4,0,4,8,11,15,19,22)])

# Offset Values for ROI
offset = np.array([(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17),(17,20,23,25,28,29,30,29,28,25,23,20,17)])

# phi = 90
# theta = 90

# tof.set_roi_center()

# Set ROI Size
tof.set_roi_size(4, 4)
# TimingBudgetInMs: Predefined values = 15, 20, 33, 50, 100 (**default**), 200, 500.
tof.set_timing_budget_in_ms(50)
# Intermeasurement period must be >/= timing budget
tof.set_inter_measurement_in_ms(52)


dataReady = 0

# Scan the values by setting values for Phi and Theta
for phi in range(50,125,15):
    for theta in range(65,140,15):
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
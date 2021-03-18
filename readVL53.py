import time
import sys
import signal

import VL53L1X


print("""distance.py
Display the distance read from the sensor.
Uses the "Short Range" timing budget by default.
Press Ctrl+C to exit.
""")


# Open and start the VL53L1X sensor.
# If you've previously used change-address.py then you
# should use the new i2c address here.
# If you're using a software i2c bus (ie: HyperPixel4) then
# you should `ls /dev/i2c-*` and use the relevant bus number.
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()

running = True


def exit_handler(signal, frame):
    global running
    running = False
    tof.stop_ranging()
    print()
    sys.exit(0)


# Attach a signal handler to catch SIGINT (Ctrl+C) and exit gracefully
signal.signal(signal.SIGINT, exit_handler)

while running:
    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0, 0, 3, 3))
    tof.start_ranging(1)
    distance_in_mm1 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(4, 0, 7, 3))
    tof.start_ranging(1)
    distance_in_mm2 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(8, 0, 11, 3))
    tof.start_ranging(1)
    distance_in_mm3 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(12, 0, 15, 3))
    tof.start_ranging(1)
    distance_in_mm4 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0, 4, 3, 7))
    tof.start_ranging(1)
    distance_in_mm5 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(4, 4, 7, 7))
    tof.start_ranging(1)
    distance_in_mm6 = tof.get_distance()
    tof.stop_ranging()

    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(8, 4, 11, 7))
    tof.start_ranging(1)
    distance_in_mm7 = tof.get_distance()
    tof.stop_ranging()

    print(str(distance_in_mm1) + " " + str(distance_in_mm2)+ " " + str(distance_in_mm3)+ " " + str(distance_in_mm4)+ " " + str(distance_in_mm5))

    #print("Distance: {}mm".format(distance_in_mm))
    #time.sleep(0.1)
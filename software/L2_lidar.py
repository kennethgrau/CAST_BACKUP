# Initializes LIDAR object from L1 library and continuously converts the 
# information to readable and processable array where index of array is the
# is the theta from +x axis and value is the distance
# Last update 4/20/2022 - Kenneth Grau

# Import necessary libraries for LIDAR
import os
import sys
import time
import pigpio
import adafruit_rplidar as raslidar
from math import cos, sin, pi, floor
import numpy as np


# Initialize the RPLidar A1
PORT_NAME = '/dev/ttyUSB0'                              # Set port
lidar = raslidar.RPLidar(None, PORT_NAME, timeout=3)    # Initialize LIDAR at port

# Cleanup to prevent errors if improper shutdown occurs (Don't ask why, it just prevents a certain error)
lidar.stop_motor()
lidar.stop()
lidar.disconnect()
lidar = raslidar.RPLidar(None, PORT_NAME, timeout=3)

# Initialize pigpio
pi = pigpio.pi()

# Setup LED control output
pi.set_mode(4, pigpio.OUTPUT)

# Setup the data info for 360 degrees around the core of the Lidar
scan_data = [0] * 360

def controlLED(scanData):
    for x in range(180,182):
        if (scanData[x] > 800 and scanData[x] != 0):
            pi.write(4,0)
            break
        else:
            pi.write(4,1)
    print(scanData[180],scanData[181],scanData[182])
    time.sleep(0.01)
    

# Read LIDAR data and compile to readable array
def scan():
    for scan in lidar.iter_scans():                             # iterate through a set of buffered readings
        for (_, angle, distance) in scan:
            scan_data[int(min([359, angle]))] = round(distance) # convert buffered readings into list
        controlLED(scan_data)

def go():
    while (1):
        scan()

if __name__ == "__main__":
    go()

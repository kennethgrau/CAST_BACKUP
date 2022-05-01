# Initializes LIDAR object from L1 library and continuously converts the 
# information to readable and processable array where index of array is the
# is the theta from +x axis and value is the distance - see provided documentation for picture
# Last update 4/30/2022 - Kenneth Grau

# Noted Error - Running this code will sometimes throw a "Descriptor length mismatch error", cancelling and re-running code fizes it
# Wokring on a catch for that error currently

# Import external libraries
import os
import sys
import time
import pigpio
from math import cos, sin, pi, floor
import numpy as np

# Import internal libraries
import adafruit_rplidar as raslidar


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

# Processing function, keep anything done here short as it is called between each loading of new buffered data
# For controlling LED array in CAST system, because of LIDAR behavior it was done in the L2 code
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
    for scan in lidar.iter_scans():                             # Iterate through a set of buffered readings
        for (_, angle, distance) in scan:
            scan_data[int(min([359, angle]))] = round(distance) # Convert buffered readings into list where index = angle, value = distance reading
        controlLED(scan_data)

# Wrapper function for multithreading
def go():
    while (1):
        scan()

if __name__ == "__main__":
    go()

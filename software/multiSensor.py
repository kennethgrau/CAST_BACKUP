# Test code for multiple VL53L0X Time of Flight distance sensors with TCA9548A multiplexor
# Requires inclusion of adafruit_vl53l0x.py library and Adafruit CircuitPython
# Install with: sudo pip3 install adafruit-circuitpython-tca9548a
# 

import time
import board
import busio
import adafruit_vl53l0x
import adafruit_tca9548a

# Create I2C bus as normal 
i2c = busio.I2C(board.SCL, board.SDA)

# Create TCA9548A object
tca = adafruit_tca9548a.TCA9548A(i2c)

# Setup each sensor
vlx1 = adafruit_vl53l0x.VL53L0X(tca[0])
vlx2 = adafruit_vl53l0x.VL53L0X(tca[1])

while 1:
    print(vlx1.range,vlx2.range)
    time.sleep(0.1)
    
    


 
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
time.sleep(0.5)

# Create TCA9548A object
tca = adafruit_tca9548a.TCA9548A(i2c)
time.sleep(0.5)

# Setup each sensor
##green
#vlx1 = adafruit_vl53l0x.VL53L0X(tca[0])
## black
vlx2 = adafruit_vl53l0x.VL53L0X(tca[7])
print('black good')
##yellow

vlx3 = adafruit_vl53l0x.VL53L0X(tca[6])
print('green good')
# print('yellow good')

while 1:
    #print(vlx1.range)
    time.sleep(0.2)
    print(vlx3.range)
    time.sleep(0.2)
    print(vlx2.range)
    
    


 
# Test code for multiple VL53L0X Time of Flight distance sensors with TCA9548A multiplexor
# Requires inclusion of adafruit_vl53l0x.py library
# Requires inclusion of adafruit_tca9548a.py library
# Created to test functionality of ToF sensors with multiplexor before running multithreading code.
# Author: Kenneth Grau | Updated: 4/30/2022

# Import external libraries
import time
import board
import busio

# Import internal libraries
import L1_ToF as ToF
import L1_multiplexor as mult

# Create I2C bus as normal 
i2c = busio.I2C(board.SCL, board.SDA)
print('Initializing I2C bus...')
time.sleep(0.5)                             # Allow I2C bus to settle
print('Success!')

# Create TCA9548A object
tca = mult.TCA9548A(i2c)
print('Initializing multiplexor object...')
time.sleep(0.2)
print('Success!')

# Setup each sensor
# ToF connected to black marked cable
print('Initializing ToF sensor connected to Black marked cable...')
vlx2 = ToF.VL53L0X(tca[7])
print('Success!')

# ToF Connected to green marked cable
print('Initializing ToF sensor connected to Green marked cable...')
vlx3 = ToF.VL53L0X(tca[6])
print('Success!')

if __name__ == "__main__":
    while (1):
        time.sleep(0.2)
        print('Black Cable ToF: ' + str(vlx2.range))
        time.sleep(0.2)
        print('Green Cable ToF: ' + str(vlx3.range))
    
    


 

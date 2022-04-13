# Actuator and Time of Flight Distance sensor program for CAST Bot  runnning SCUTTLE RasPi image
# This code sends commands to NEMA 23 stepper motor on appropriate GPIO pins for ST-M5045 Driver and demonstrates response to distance sensor
# See wiring guide doncument for pin mapping
# Last update 02.28.2022 - Kenneth Grau


# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time
from time import sleep
import board
import busio
import L1_vl53l0x as ToF
import L1_multiplexor as mult
import L1_actuator as act

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# Create TCA9548A object
tca = mult.TCA9548A(i2c)

# Create sensor objects
vlx1 = ToF.VL53L0X(tca[0])
vlx2 = ToF.VL53L0X(tca[1])

#Move variable will output zero or one to communicate when the arm needs to move
Move = 0

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
vlx1.measurement_timing_budget = 20000
vlx2.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Main loop will read the range and print it every second.
checkPos = 0
ToF1 = 0
ToFHist = 600
ToF2 = 0

state = 1
while True:
    while state == 1:
        ToF1 = int(vlx1.range)
        print("Range: {0}mm".format(vlx1.range))
        if (ToF1 > 20 and ToF1 < 500):
            #Move variable will output zero or one to communicate when the arm needs to move
            #This is the variable that will be used in the linear actuator program
            move = 1
            act.move(0.01,0)
            print(move)
            ToFHist = ToF1
            checkPos = checkPos + 1
        if (ToF1 > 500 and ToFHist < 500):
            state = 2
            act.move(0.05,0)
            print(state)
    
    while state == 2:
        ToF2 = int(vlx2.range)
        print("Range: {0}mm".format(vlx2.range))
        if (ToF1 > 500 and ToF2 < 500):
            state = 3
    
    while state == 3: # add condition that there is another object at a lower level still
        ToF2 = int(vlx2.range)
        print("Range: {0}mm".format(vlx2.range))
        if (ToF1 > 500 and ToF2 > 500 and checkPos > 0):
            act.move(0.05,1)
            for x in range(checkPos):
                act.move(0.01,1)
            checkPos = 0
            state = 1
            ToFHist = 600
        
        
    
    
            

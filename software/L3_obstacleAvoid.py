# This program includes the obstacle avoidance protocols for CAST robot
# Includes the use of ToF sensors to check planes of arm for obstacles
# similar to how a garage door detects objects.
# This provides automatic control of the arm. Manual control is available in
# L3_gpControl.py
# Updated 4/20/2022 - Kenneth Grau

# Import needed libraries
import time
import board
import busio
import pigpio
import L1_actuator as act
import L1_distSensor as ToF
import L1_multiplexor as mult

pi = pigpio.pi()

botEndStop = 6

pi.set_mode(botEndStop, pigpio.INPUT)       # enable pin (active low)

# Create I2C bus as normal 
i2c = busio.I2C(board.SCL, board.SDA)
time.sleep(0.1)

# Create TCA9548A object
tca = mult.TCA9548A(i2c)
time.sleep(0.1)

# Initialize distance sesnor objects
botToF = ToF.VL53L0X(tca[0])
rightToF = ToF.VL53L0X(tca[1])
leftToF = ToF.VL53L0X(tca[2])

arm = 650

def go():
    while (1):
        print(botToF.range,rightToF.range,leftToF.range)
        if ((rightToF.range < arm) or (leftToF.range < arm)):
            # print('obstacle detected in path of arm')
            act.sendPWM(1,0.09)
            while ((rightToF.range < arm) or (leftToF.range < arm)):
                print("moving arm up, movement disabled")
                print(rightToF.range, botToF.range, leftToF.range)
                time.sleep(0.01)
            act.sendPWM(1,0)
        if botToF.range > arm:
            act.sendPWM(0,0.09)
        
        

if __name__ == "__main__":
    go()
        
    
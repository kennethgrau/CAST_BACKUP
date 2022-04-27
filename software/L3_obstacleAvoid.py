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
import L1_actuator as act
import L1_distSensor as ToF
import L1_multiplexor as mult

# Create I2C bus as normal 
i2c = busio.I2C(board.SCL, board.SDA)

# Create TCA9548A object
tca = mult.TCA9548A(i2c)

# Initialize distance sesnor objects
vlx1 = ToF.VL53L0X(tca[0])
vlx2 = ToF.VL53L0X(tca[1])
vlx3 = ToF.VL53L0X(tca[2])

def go():
    while (1):
        # print(vlx1.range,vlx2.range,vlx3.range)
        if ((vlx1.range < 500 and vlx1.range != 0) or (vlx3.range < 500 and vlx3.range != 0)):
            # print('obstacle detected in path of arm')
            act.sendPWM(1,0.09)
            while ((vlx1.range < 500 and vlx1.range != 0) or (vlx3.range < 500 and vlx3.range != 0)):
                print("moving arm up, movement disabled")
        if vlx2.range < 500 and vlx2.range != 0:
            while vlx2.range < 500 and vlx2.range != 0:
                print(vlx2.range)
                # print('found object below, move robot until false, disabled up/down control')
            # print('moved over object moving arm down, movement disabled')
            act.resetArm()
        print('driving around')
        act.sendPWM(1,0)
        
    
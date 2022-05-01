# This program is adapted from gpDemo.py from 
# https://github.com/scuttlerobot/SCUTTLE/blob/master/software/python/basics_pi/L3_gpDemo.py
# as developed by Author: David Malaway

# A demonstration program: drive with gamepad.
# This program grabs data from the onboard sensors and log data in files
# for NodeRed access and integrate into a custom "flow".
# Access nodered at your.ip.address:1880

# v2020.11.29 DPM

# Import External programs

# Adapted to include controls for peripherals for CAST robot 2022
# includes control for moving actuator arm up and down and
# toggling LED lights on and off
# Updated 4/30/2022 - Kenneth Grau

import numpy as np
import time
import pigpio

# Initialize pigpio object
pi = pigpio.pi()

# Setup for button GPIO connections
pi.set_mode(20, pigpio.OUTPUT) 
pi.set_mode(16, pigpio.OUTPUT)
pi.set_mode(21, pigpio.OUTPUT)


# Import Internal Programs
import L1_gamepad as gp
import L1_log as log
import L1_actuator as act
import L2_inverse_kinematics as inv
import L2_kinematics as kin
import L2_speed_control as sc

# Run the main loop
def gpControl():
    while(1):
        # # ACCELEROMETER SECTION
        # accel = mpu.getAccel()                          # call the function from within L1_mpu.py
        # (xAccel) = accel[0]                             # x axis is stored in the first element
        # (yAccel) = accel[1]                             # y axis is stored in the second element
        # #print("x axis:", xAccel, "\t y axis:", yAccel)     # print the two values
        # axes = np.array([xAccel, yAccel])               # store just 2 axes in an array
        # log.NodeRed2(axes)                              # send the data to txt files for NodeRed to access.
        
        # # DISPLAY BATTERY LEVEL
        # vb = adc.getDcJack()
        # log.tmpFile(vb,"vb.txt")
        
        # COLLECT GAMEPAD COMMANDS
        gp_data = gp.getGP()
        axis0 = gp_data[0] * -1
        axis1 = gp_data[1] * -1
        rthumb = gp_data[3]     # up/down axis of right thumb
        up = gp_data[4]         # "y" button
        down = gp_data[6]       # "a" button
        
        
        
        # HORN FUNCTION
        # the horn is connected by relay to port 1 pin 0 (relay 1 of 2)
        # print("horn button:", horn)
        # if horn:
        #     gpio.write(1, 0, 1) # write HIGH
        #     time.sleep(0.30) # actuate for just 0.2 seconds
        #     gpio.write(1, 0, 0) # write LOW
        # #print("rthumb axis:", rthumb)
        
        phiDots = kin.getPdCurrent()
        myString = str(round(phiDots[0],1)) + "," + str(round(phiDots[1],1))
        log.stringTmpFile(myString,"phidots.txt")
    
        myString = str(round(axis0*100,1)) + "," + str(round(axis1*100,1))
        log.stringTmpFile(myString,"uFile.txt")
        # print("Gamepad, xd: " ,axis1, " td: ", axis0) # print gamepad percents
        # print(gp_data[4],gp_data[6])
        
        # DRIVE IN OPEN LOOP
        chassisTargets = inv.map_speeds(np.array([axis1, axis0])) # generate xd, td
        pdTargets = inv.convert(chassisTargets) # pd means phi dot (rad/s)
        # phiString = str(pdTargets[0]) + "," + str(pdTargets[1])
        # print("pdTargets (rad/s): \t" + phiString)
        # log.stringTmpFile(phiString,"pdTargets.txt")
        
        #DRIVING
        sc.driveOpenLoop(pdTargets) #call driving function
        #servo.move1(rthumb) # control the servo for laser

        # Pin write to trigger callback functions for gamepad buttons
        pi.write(20,int(gp_data[4]))
        pi.write(16,int(gp_data[6]))
        pi.write(21,int(gp_data[5]))

        # Pin write to trigger callback functions for enstops
        # Issue: Callback functions wouldn't trigger directly on enstop pins
        # Temp Fix: Writing to auxilary pin and trigger callback on that seemed to work
        pi.write(12,int(pi.read(6)))
        pi.write(25,int(pi.read(5)))

        time.sleep(0.05)

# Callback function to move arm up on Y button press
def up(gpio, level, tick):
    act.sendPWM(1,0.09)

# Callback function to move arm down on A button press
def down(gpio, level, tick):
    act.sendPWM(0,0.09)

# Callback function to stop arm down on button release
def stop(gpio, level, tick):
    act.sendPWM(0,0)

# Callback function to toggle LED arrays on B button press
def toggle(gpio, level, tick):
    x = pi.read(4)
    pi.write(4,not(x))

# Create callbacks for above cases
cb1 = pi.callback(20,0,up)              # Go up on rising edge of Y button
cb2 = pi.callback(20,1,stop)            # Stop on falling edge of Y button
cb3 = pi.callback(16,0,down)            # Go up on rising edge of A button
cb4 = pi.callback(16,1,stop)            # Stop on falling edge of A button
cb5 = pi.callback(21,0,toggle)          # Toggle LEDs on rising edge of B button
cb6 = pi.callback(12,1,stop)            # Stop on falling edge of top enstop (they are active low)
cb7 = pi.callback(25,1,stop)            # Stop on falling edge of top enstop (they are active low)

# Wrap for multithreading
def go():
    gpControl()

if __name__ == "__main__":
    gpControl()
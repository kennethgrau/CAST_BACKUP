# L1 program for CAST Bot actuator runnning SCUTTLE RasPi image
# This code sends signals to ST-M5045 motor driver/NEMA 23 stepper motor on appropriate GPIO pins
# See wiring guide doncument for pin mapping
# Last update 04.20.2022 - Kenneth Grau

# Import external libraries

# note pigpio uses BROADCOM numbers for labeling
import pigpio

# sleep is used for precision stepping as timing has a resolution of 1ms
import time
from time import sleep

# Initialize pigpio
pi = pigpio.pi()

# Label signal pins                 USES BROADCOM NUMBERING
puls = 13                           # Pulse output signal pin
dir = 19                            # Direction output signal pin
en = 26                             # Enable output signal ping

# Label endstop pins
topEndStop = 5
botEndStop = 6

# Initialize mode for GPIO pins
pi.set_mode(puls, pigpio.OUTPUT)            # pulse/signal generation
pi.set_mode(dir, pigpio.OUTPUT)             # direction pin
pi.set_mode(en, pigpio.OUTPUT)              # enable pin (active low)
pi.set_mode(topEndStop, pigpio.INPUT)       # enable pin (active low)
pi.set_mode(botEndStop, pigpio.INPUT)       # enable pin (active low)


# Set of parameters preset by user determined by actuator and driver
LDPR = 0.00508                  # Linear distance per revolution of lead screwt (m)
SPR = 800                       # steps per revolution set by driver
MPS = 0.00635                   # max linear speed (m/s) achievable precision stepping
maxSpeed = 0.0925               # max linear speed (m/s) achievable with pwm driving

def calculateStepDelay( speed ):
    if speed > MPS:
        x = 1/(MPS/LDPR*SPR)/2              # Calculate delay for max speed
    else:
        x = 1/(speed/LDPR*SPR)/2            # Calculate delay for desired speed

# Move arm in a specified direct at specified speed with precision stepping
def step( dirs, speed = MPS):
    
    pi.write(en,0)                          # Enable 
    pi.write(dir,dirs)                      # Set direction signal
    pi.set_mode(puls, pigpio.OUTPUT)        # Ensure pin is in correct mode and setup enable
    delay = calculateStepDelay(speed)
    
    pi.write(puls,0)                        # Create square pulse by turning
    sleep(delay)                            # on and off GPIO with delay    
    pi.write(puls,1)
    sleep(delay)

    pi.write(en,1)
    
# Calculate frequency for desired speed
def calculatePWM( speed ):
    if speed > maxSpeed:
        x = maxSpeed/LDPR*SPR           # Calculate frequency for max speed
    else:
        x = speed/LDPR*SPR              # Calculate frequency for desired speed 
    return(x)
    
# Move the arm in direction with specified speed (less precise but much faster)
def sendPWM( dirs, speed ):
    
    pi.write(en,1)                      # Reset enable pin to prevent motor locking
    sleep(0.05)                         # Give the motor a slight break
    pi.write(en,0)                      # Enable stepper driver (active low)
    pi.write(dir,dirs)                  # Set direction signal
    x = 0                               # To be used in ramping
    freq = round(calculatePWM(speed))   # Function to compute required frequency for speed
    print(freq)
    if (dirs == 1 and pi.read(topEndStop) == 0 and speed !=0):
        print('Error: Top ensdtop triggered, cannot move up.')
    elif (dirs == 0 and pi.read(botEndStop) == 0 and speed !=0):
        print('Error: Bottom endstop triggered, cannot move down.')
    else:
        while(x <= freq):                   # Ramp toward target speed
            pi.hardware_PWM(puls,x,500000)  # Set frequency to x
            sleep(0.001)                    # Slight delay
            x = x + 250                     # Increment x to target frequency for speed
    
# Reset arm to bottom position
def resetArm():
    
    pi.write(en,0)                      # Enable driver
    sendPWM(0,maxSpeed)                 # Move arm down at max speed
    while(pi.read(botEndStop) == 1):    # Check for endstop
        time.sleep(0.01)                # Wait for Botom endstop to be pressed
        print('moving')
    sendPWM( 0, 0)                      # Kill PWM signal once botEndStop pressed

if __name__ == "__main__":
    
    sendPWM(0,0.0)

    sleep(2)
    sendPWM(1,0)
    
    

    


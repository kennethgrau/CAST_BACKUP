# Problems with motor - test cases

import L1_actuator as act
import time
from time import sleep


if __name__ == "__main__":

    try:
        speed = 0.03
        
        while speed <= 0.09:
            print('speed: '+ str(speed*100) + 'cm/s')
            act.sendPWM(1,speed)
            sleep(2)
            act.sendPWM(0,speed)
            sleep(2)
            act.sendPWM(1,0)
            sleep(3)
            speed = speed + 0.01

        while (1):
            sleep(1)
    except KeyboardInterrupt:
        act.sendPWM(1,0)
    

    
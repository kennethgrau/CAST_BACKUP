# Control protocol for automatic LED control through LIDAR
# Turns on LEDS when rebot believes the arm is over a surface that
# can be sanitized by the arm.
# Updated 4/20/2022 - Kenneth Grau

import L2_lidar as lid

def go():
    while (1):
        print(lid.scan())
        
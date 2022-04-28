# This will be a minimal example of demonstrating multithreading for SCUTTLE.

# IMPORT EXTERNAL ITEMS
import time
import threading # only used for threading functions

# IMPORT INTERNAL ITEMS
import L3_gpControl as drive
import L3_obstacleAvoid as obst
import L2_lidar as led

# CREATE A THREAD FOR PRINTING TEST
def loop_obst( ID ):
    obst.go()  # command the full program to run
        
# CREATE A THREAD FOR DRIVING
def loop_drive( ID ):
    drive.go() # command the full program to run
    
def loop_led( ID ):
    led.go() # command the full program to run

# ALL THREADS ARE CALLED TO RUN IN THE MAIN FUNCTION
if __name__ == "__main__":
    print("starting the main fcn")
    threads = []  # create an object for threads

    t2 = threading.Thread( target=loop_drive, args=(2,) ) # make 2nd thread object
    threads.append(t2) # add this function to the thread object
    t2.start() # start executing
    print("started thread2, for driving")
    
    t3 = threading.Thread( target=loop_led, args=(3,) ) # make 2nd thread object
    threads.append(t3) # add this function to the thread object
    t3.start() # start executing
    print("started thread2, for led control")
    
    t = threading.Thread( target=loop_obst, args=(1,) ) # make 1st thread object
    threads.append(t) # add this function to the thread object
    t.start() # start executing
    print("started thread1, for obstacle ovoidance")

    # the join commands manipulate the way the program concludes multithreading.
    t.join()
    t2.join()
    t3.join()

# EXECUTE THE MAIN FUNCTION

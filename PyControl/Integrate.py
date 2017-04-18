'''
Wait for Long Pulse --> update Retra State
'''

import RetraControl # driver
import time
import RPi.GPIO as GPIO
import scipy as sp



def integrate(fn):

    # read the file of intensities
    intensities = sp.load(fn)

    # initialize the driver:
    rc = RetraControl('/dev/ttyUSB0')
    rc.red_on()
    rc.set_intensity(0)

    # initialize comm on pin 4:
    # Broadcom pin numbering
    GPIO.setmode(GPIO.BCM)
    # set BCM 4 as input
    GPIO.setup(4, GPIO.IN)

    # control loop:
    t0 = time.time()
    state = 0
    ind = 0
    while(True):
        if(GPIO.input(4)):
        if(state == 0):
            t0 = time.time()
                state = 1
        else:
            if(state == 1):
                t1 = time.time()
                print(t1-t0)
                if((t1-t0) > .0001):
                    rc.set_intensity(intensities[ind])
                    ind += 1          
                t0 = t1
                state = 0


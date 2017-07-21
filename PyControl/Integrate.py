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

    print(intensities) 

    # initialize the driver:
    rc = RetraControl.RetraControl('/dev/ttyUSB0')
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
                if((t1-t0) > .001):
                    print(intensities[ind])
                    rc.set_intensity(intensities[ind])
                    ind += 1          
                t0 = t1
                state = 0


if(__name__ == '__main__'):
    #fn = 'two_pattern_poly_80.npy' 
    #fn = 'two_pattern_poly.npy'
    #fn = 'sinp1.npy'
    fn = 'sparse_pattern.npy'
    integrate(fn)




'''
Read signals coming out of SPIM 
Look for long pulses (new stack starting)


TODO: Let's try gpio first 


TODO: serial communication is probably better for our sleep res
Serial Compatability with RasPi 3: disable bluetooth map UART0 back to serial com
-> updating
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo rpi-update
-> remapping:
sudo vim /boot/config.txt
dtoverlay=pi3-disable-bt
-> stop bluetooth from trying to use UART
sudo systemctl disable hciuart
-> reboot and test serial coms:
sudo minicom -D /dev/ttyAMA0 -b38400
-> disable serial console
sudo nano /boot/cmdline.txt
remove console=ttyAMA0,115200


TODO: put this shit in OO


TODO: we will probably have timing issues --> try using wiringpi

'''

# with serial comm enabled --> use pyserial
#import serial
import time
import RPi.GPIO as GPIO


'''
# looks like upper limit is 10s of microseconds...we care about milliseconds 
t0 = time.time()
# test time resolution:
while(True):
    t1 = time.time()
    print(t1 - t0)
    t0 = t1   
'''


'''
ser = serial.Serial('/dev/ttyAMA0') # 9600 is standard
lasttime = time.clock()

while(True):
    # read buffer:
    while(ser.in_waiting):
        print(ser.read())   
        t = time.clock()
        print(t = lasttime)
        lasttime = time.clock()  
'''


# GPIO stuff:
# Broadcom pin numbering
GPIO.setmode(GPIO.BCM)
# set BCM 4 as input
GPIO.setup(4, GPIO.IN)


# Q? use twisted framework??? 

# look for rising edge:
t0 = time.time()
def rise_fall():
    # check current value:
    if(GPIO.input(4)): # rising
        t0 = time.time()
        t1 = t0
    else: # falling 
        t1 = time.time()
        print(t1 - t0)
        #if((t1 - t0) > .001):
        #    update = 1 
        t0 = t1     


GPIO.add_event_detect(4, GPIO.BOTH, callback=rise_fall)


'''
My Idea: master thread launches rise and fall threads
--> looks for large t1 - t0 --> yells at retra controller 
'''







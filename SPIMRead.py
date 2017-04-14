'''
Read signals coming out of SPIM 
Look for long pulses (new stack starting)


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
import serial
import time

ser = serial.Serial('/dev/ttyAMA0') # 9600 is standard
lasttime = time.clock()

while(True):
    # read buffer:
    while(ser.in_waiting):
        print(ser.read())   
        t = time.clock()
        print(t = lasttime)
        lasttime = time.clock()  



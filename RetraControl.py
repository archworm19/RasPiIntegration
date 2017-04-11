'''

Communicate Serial to Retra

'''
import serial
import time


class RetraControl:

    # initialize port and useful commands 
    def __init__(self, port_str):
        # initialize port:
        this.port = serial.Serial(port_str) # 8N1 standard

        # initialize communication:
        i1 = bytearray([87, 2, 170, 80])
        i2 = bytearray([87, 3, 170, 80])
        this.port.write(str(i1))
        this.port.write(str(i2))

        # initialize useful strings:
        this.red_on_str = str(bytearray([79, 254, 80]))
        this.red_off_str = str(bytearray([79, 255, 80]))

        # TODO: intensity command prefix and postfix:
        this.prefix_str = str(bytearray([83, 24, 3, 8]))
        this.cur_byte = 240
        this.postfix_str = str(bytearray([80]))


    def red_on(self):
        this.port.write(this.red_on_str)


    def red_off(self):
        this.port.write(this.red_off_str)


    # set intensity
    # Takes in integer intensity value
    # max = 4095
    def set_intensity(self, intense):
        # 1st: invert
        inv_intense = 4095 - intense 

        # translate inverse intensity value into two bytes
        large_byte = int(inv_intense / 255)
        little_byte = int(inv_intense - (255 * large_byte))

        write_intense = str(byte_array([large_byte, little_byte]))

        this.port.write(this.prefix_str)
        this.port.write(write_intense)
        this.port.write(this.postfix_str)


# testing:
if(__name__ == '__main__'):
    rc = RetraControl('/dev/ttyUSB0')
    rc.red_on()
    time.sleep(1)
    rc.set_intensity(200)
    time.sleep(1)
    rc.set_intensity(800)
    time.sleep(1)
    rc.red_off() 



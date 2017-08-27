'''

Communicate Serial to Retra

'''
import serial
import time


class RetraControl:

    # initialize port and useful commands 
    def __init__(self, port_str):
        # initialize port:
        self.port = serial.Serial(port_str) # 8N1 standard

        # initialize communication:
        i1 = bytearray([87, 2, 170, 80])
        i2 = bytearray([87, 3, 170, 80])
        self.port.write(str(i1))
        self.port.write(str(i2))

        # initialize useful strings:
        self.red_on_str = str(bytearray([79, 254, 80]))
        self.red_off_str = str(bytearray([79, 255, 80]))

        # TODO: intensity command prefix and postfix:
        self.prefix_byte = bytearray([83, 24, 3, 7])
        self.postfix_byte = bytearray([80])

        self.state = 0


    def red_on(self):
        self.port.write(self.red_on_str)


    def red_off(self):
        self.port.write(self.red_off_str)


    # set intensity
    # Takes in integer intensity value
    # intensity range = 0...100 
    def set_intensity(self, intense):
        if(intense <= .9):
            self.red_off()
            self.state = 0
            return
        if(self.state == 0):
            self.red_on()
            self.state = 1

        # scale
        full_intense = intense * (255.0/100.0)
    
        # 1st: invert
        inv_intense = 255.0 - full_intense

        # translate inverse intensity value into two bytes
        large_byte = int(inv_intense / 16)
        little_byte = int(inv_intense - (16 * large_byte))

        write_intense = bytearray([240+large_byte, little_byte*16])

        write_str = str(self.prefix_byte + write_intense + self.postfix_byte)
        
        self.port.write(write_str)
        

# testing:
if(__name__ == '__main__'):
    rc = RetraControl('/dev/ttyUSB0')
    rc.red_on()
    time.sleep(2)
    rc.set_intensity(0)
    time.sleep(2)
    rc.set_intensity(200)
    time.sleep(2)
    rc.set_intensity(1000)
    time.sleep(2)
    rc.red_off() 



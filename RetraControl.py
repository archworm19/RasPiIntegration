'''

Communicate Serial to Retra

'''
import serial


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
        this.cur_byte = bytearray([240, 0]) 
        this.postfix_str = str(bytearray([80]))


    def red_on(self):
        this.port.write(this.red_on_str)


    def red_off(self):
        this.port.write(this.red_off_str)


    # TODO: set intensity
    # Takes in 2 bytes for intensity 
    def set_intensity(self, intense):
 


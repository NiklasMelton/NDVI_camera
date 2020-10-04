import smbus
import RPi.GPIO as gpio
import os

i2c_ch = 1
i2c_address = 0x70

class MultiCamera:
    def __init__(self):
        self.bus = smbus.SMBus(i2c_ch)
        gpio.setmode(gpio.BOARD)
        gpio.setup(17, gpio.OUT)
        gpio.setup(4, gpio.OUT)
        gpio.output(4, 0)
        gpio.output(17, 0)

    def select_camera_A(self):
        gpio.output(4, 0)
        self.bus.write_i2c_block_data(i2c_address, 0x00, 0x01)

    def select_camera_B(self):
        gpio.output(4, 1)
        self.bus.write_i2c_block_data(i2c_address, 0x00, 0x02)

    def capture(self,name):
        cmd = "raspistill -o {}.jpg",format(name)
        os.system(cmd)

import RPi.GPIO as gpio
import os
import picamera

i2c_ch = 1
i2c_address = 0x70

class MultiCamera:
    def __init__(self):
        # self.bus = smbus.SMBus(i2c_ch)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920,1088)
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.OUT)
        gpio.setup(4, gpio.OUT)
        gpio.output(4, 0)
        gpio.output(17, 0)

    def select_camera_A(self):
        gpio.output(4, 0)
        # self.bus.write_i2c_block_data(i2c_address, 0x00, 0x01)
        os.system('i2cset -y 1 0x70 0x00 0x01')
    def select_camera_B(self):
        gpio.output(4, 1)
        # self.bus.write_i2c_block_data(i2c_address, 0x00, 0x02)
        os.system('i2cset -y 1 0x70 0x00 0x02')

    def capture(self,filename,ext='rgb'):
        # cmd = "raspistill -o {}.jpg".format(name)
        # os.system(cmd)
        self.camera.capture(filename+'.'+ext, ext)

    def double_capture(self,filename):
        self.select_camera_A()
        self.capture(filename+'_CamA')
        self.select_camera_B()
        self.capture(filename+'_CamB')

if __name__ == '__main__':
    mc = MultiCamera()
    mc.select_camera_A()
    print('A')
    mc.capture('camera1')
    mc.select_camera_B()
    print('B')
    mc.capture('camera2')
    print('complete')
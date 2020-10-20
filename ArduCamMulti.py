
import RPi.GPIO as gpio
import os
import picamera
import time

i2c_ch = 1
i2c_address = 0x70

class MultiCamera:
    def __init__(self,**kwargs):
        # self.bus = smbus.SMBus(i2c_ch)
        # self.camera = picamera.PiCamera()
        self.w = 1920
        self.h = 1088
        if 'shutter' in kwargs:
            self.ss = kwargs['shutter']
        else:
            self.ss = 200000
        if 'iso' in kwargs:
            self.iso = kwargs['iso']
        else:
            self.iso = 100

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

    def capture(self,filename,ext='png'):
        cmd = "raspistill -ISO {} -ss {} -w {} -h {} -o {}".format(self.iso, self.ss, self.w, self.h,filename+'.'+ext)
        os.system(cmd)
        # self.camera.capture(filename+'.'+ext, ext)

    def double_capture(self,filename):
        self.select_camera_A()
        self.capture(filename+'_CamA')
        time.sleep(3)
        self.select_camera_B()
        self.capture(filename+'_CamB')
        time.sleep(3)

if __name__ == '__main__':
    mc = MultiCamera()
    mc.select_camera_A()
    print('A')
    mc.capture('camera1')
    mc.select_camera_B()
    print('B')
    mc.capture('camera2')
    print('complete')
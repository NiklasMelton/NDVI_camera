import tm1637
import datetime
import ArduCamMulti
import time
import RPi.GPIO as gpio
import os

SHUTTER_FREQ = 300
BUTTON_CHANNEL = 18
DATA_PATH = '/home/pi/NDVI_data/'
IMAGE_COUNTER_FILE = DATA_PATH+'image_counter.txt'
os.makedirs(DATA_PATH,exist_ok=True)

class Display:
    def __init__(self):
        self.display = tm1637.TM1637(23,24, brightness=1.0)
        self.display.Clear()

    def show_int(self,int):
        self.display.Clear()
        self.display.ShowDoublepoint(False)
        self.display.ShowInt(int)

    def show_time(self,today=None):
        if today is None:
            today = datetime.datetime.today()
        t = today.time()
        h = str(t.hour)
        m = str(t.minute)
        if len(m) < 2:
            m = '0'+m
        self.display.Clear()
        self.display.ShowDoublepoint(True)
        self.display.ShowInt(int(h+m))

    def show_null(self):
        self.display.Clear()
        self.display.ShowDoublepoint(False)
        self.display.Show([-1,-1,-1,-1])

def get_image_counter():
    return int(open(IMAGE_COUNTER_FILE,'r').read())

def gen_filename(today=None):
    if today is None:
        today = datetime.datetime.today()
    inc = get_image_counter()+1
    filename = 'image_date_{}_{}_{}_time_{}_{}_count_{}'.format(today.year,today.month,today.day,today.hour,today.minute,inc)
    return filename

def increment_image_counter():
    inc = get_image_counter()+1
    open(IMAGE_COUNTER_FILE,'w').write(str(inc))
    return inc

def initialize_image_counter():
    if not os.path.exists('image_counter.txt'):
        open(IMAGE_COUNTER_FILE, 'w').write(str(0))
        return 0
    else:
        return get_image_counter()


class camera_box:
    def __init__(self):
        self.camera = ArduCamMulti.MultiCamera()
        self.display = Display()

        self.DMUTEX = False
        self.IMAGE_COUNT = initialize_image_counter()

        gpio.setup(BUTTON_CHANNEL, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(BUTTON_CHANNEL, gpio.FALLING, callback=self.shutter(),bouncetime=200)

    def shutter(self,today=None):
        filename = DATA_PATH+gen_filename(today)
        self.DMUTEX = True
        self.display.show_null()
        self.camera.double_capture(filename)
        self.IMAGE_COUNT = increment_image_counter()
        self.display.show_int(self.IMAGE_COUNT)
        time.sleep(3)
        self.DMUTEX = False


if __name__ == '__main__':
    cb = camera_box()
    state_bit = 0
    today = datetime.datetime.today()
    last_display_time = today
    last_shutter_time = today
    cb.shutter(today)
    cb.display.show_time(today)
    while True:

        today = datetime.datetime.today()
        while cb.DMUTEX or (today - last_display_time).seconds < 5:
            time.sleep(1)
            today = datetime.datetime.today()
        if state_bit < 2:
            cb.display.show_time(today)
        else:
            cb.display.show_int(cb.IMAGE_COUNT)
        last_display_time = today
        state_bit = (state_bit+1)%3
        if (today-last_shutter_time).seconds > SHUTTER_FREQ:
            cb.shutter(today)
            last_shutter_time = today
        time.sleep(1)




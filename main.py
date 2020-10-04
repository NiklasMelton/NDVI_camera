import tm1637
import datetime
import ArduCamMulti
import time

class display:
    def __init__(self):
        self.display = tm1637.TM1637(23,24, brightness=1.0)
        self.display.Clear()

    def show_int(self,int):
        self.display.Clear()
        self.display.ShowDoublepoint(False)
        self.display.ShowInt(int)

    def show_time(self):
        t = datetime.datetime.today().time()
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

if __name__ == '__main__':
    d = display()
    while True:
        d.show_time()
        time.sleep(10)

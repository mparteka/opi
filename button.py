import threading
from pyA20.gpio  import gpio
import time

# todo add support for long press
class Button(threading.Thread):
    def __init__(self, pin, callback):
        threading.Thread.__init__(self)
        self.is_running = True
        self.pin = pin
        gpio.setcfg(pin, gpio.INPUT)
        gpio.pullup(pin, gpio.PULLUP)
        self.callback = callback

    def run(self):
        while self.is_running:
            status = gpio.input(self.pin)
            if not status:
                time.sleep(0.06)
                status = gpio.input(self.pin)
                if not status:
                    self.callback()

   
    def stop(self):
        self.is_running = False

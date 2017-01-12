"""
Entry point
"""

from pyA20.gpio import gpio
from pyA20.gpio import port
import threading as thread
import time
from button import Button

gpio.init()

led = port.PD14
gpio.setcfg(led, gpio.OUTPUT)
gpio.output(led, 0)

def pressbutton():
    light = gpio.input(led)
    print(light)
    if not light:
        gpio.output(led, 1)
    else:
        gpio.output(led, 0)



btn_config = {
    Button.CONFIG_BOUNCING_TIME: 0,
    Button.CONFIG_PULLUP: gpio.PULLUP
}

btn = Button(port.PC4, pressbutton, btn_config)
btn.start()

time.sleep(10)
btn.stop()
gpio.output(led, 0)
print("finish")





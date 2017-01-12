
"""
"""
import threading
import time
from pyA20.gpio import gpio

class Button(threading.Thread):
    """
    Class to handle interrupts on processor's pin.
    TODO: Add support for long press
    """

    CONFIG_BOUNCING_TIME = "bouncing"
    CONFIG_PULLUP = "pullup"

    __configuration = {
        CONFIG_BOUNCING_TIME: 0.06,
        CONFIG_PULLUP: gpio.PULLUP
    }

    __pin = None
    __callback = None
    __active = threading.Event()

    def __init__(self, pin, callback, config):
        threading.Thread.__init__(self)
        self.__configuration = self.__configuration.udpate(config)
        self.__pin = pin
        self.__callback = callback

        gpio.setcfg(self.__pin, gpio.INPUT)
        gpio.pullup(self.__pin, self.__getConfig(self.CONFIG_PULLUP))

        self.start()

    def run(self):
        self.__active.set()
        while self.__active.is_set():
            pin_state = self.__get_pin_state()

            if pin_state:
                time.sleep(self.__getConfig(self.CONFIG_BOUNCING_TIME))
                pin_state = self.__get_pin_state()
                if pin_state:
                    self.__callback()
        return

    def stop(self):
        self.__active.clear()

    def __getConfig(self, key):
        try:
            return self.__configuration[key]
        except NameError:
            return None

    def __get_pin_state(self):
        """
        Returns current state of the pin. 1 - pin is involved, 0 - otherwise
        """
        pin_state = gpio.input(self.__pin)
         # if PULLUP then we have to must revert the logic
        if self.__getConfig(self.CONFIG_PULLUP) == gpio.PULLUP:
            pin_state = not pin_state

        return pin_state
 
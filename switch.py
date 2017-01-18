from pyA20.gpio import gpio

class Switch:
    __state = 0
    __pin = None
    __listener = None
    def __init__(self, pin, listener = None):
        self.__pin = pin
        gpio.setcfg(pin, gpio.OUTPUT)
        self.__state = gpio.input(pin)
        self.__listener = listener

    def on(self):
        self.__state = 1
        gpio.output(self.__pin, self.__state)
        self.__notify()
    
    def off(self):
        self.__state = 0
        gpio.output(self.__pin, self.__state)
        self.__notify()
    
    def switch(self):
        self.__state = not gpio.input(self.__pin)
        gpio.output(self.__pin, self.__state)
        self.__notify()

    def __notify(self):
        if self.__listener is not None:
            self.__listener(self.__pin)

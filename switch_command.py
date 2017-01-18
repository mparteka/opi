from pyA20.gpio import gpio

class SwitchCommand:
    def __init__(self, args, listener = None ):
        (action, pin, value) = args.split()
        self.__pin = int(pin)
        self.__action = str(action)
        try:
            self.__value = int(value)
        except ValueError:
            pass
        self.__listener = listener

    def set_listener(self, listener):
        self.__listener = listener

    def execute(self):
        if self.__action == 'SET':
            gpio.output(self.__pin, int(self.__value))
            self.__notify()
        elif self.__action == 'SWITCH':
            status = not gpio.input(self.__pin)
            gpio.output(self.__pin, int(status))
            self.__notify()

    def __notify(self):
        if self.__listener is not None:
            self.__listener(self.__pin)

    @staticmethod
    def get_command_string(action, pin, value = None):
        result = action + " " + str(pin) + " "
        if value is not None:
            result += str(value)
        else:
            result += "NULL"
        return result

from os import listdir
from os.path import isfile, join
import re

class TemperatureSensorController:

    __devices_path = '/sys/bus/w1/devices'
    __devices = ['28-80000004920e']

    def __init__(self):
        self.__register_devices()

    def __register_devices(self):
        self.__devices_list = [d for d in listdir(self.__devices_path) if not isfile(join(self.__devices_path, d)) and d in self.__devices]

    def read_temperature(self):
        temperatures = {}
        for device in self.__devices_list:
            input = open('/sys/bus/w1/devices/'+device+'/w1_slave').read()
            result = re.search('t=(\d{5})', input).group(1)
            temperatures[device] = "%.2f" % (int(result)/1000)
        return temperatures


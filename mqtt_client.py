import paho.mqtt.client as mqtt
import time
import re
import sys

class MqttClient:

    class __MqttClient:
        
        __client = None
        __broker = '192.168.0.13'
        __port = 8000
        __qos = 2
        __keepalive = 60
        __listeners = []
        __connected = False
        __on_connect_callback = None

        def __init__(self, client_id, on_connect_callback):
            print('Initialising Client with id=' + client_id)
            self.__client = mqtt.Client(client_id, True, None, mqtt.MQTTv31)
            self.__on_connect_callback = on_connect_callback
            self.__client.on_publish = self.__on_publish
            self.__client.on_disconnect = self.__on_disconnect
            
            while not self.__connected:
                try:
                    self.__client.connect(self.__broker, self.__port, self.__keepalive)
                except OSError:
                    pass
            self.__client.loop_start()
            self.__client.loop_read()
            self.__client.on_message = self.__on_message

        def __on_connect(self, client, userdata, flags, rc):
            print('Connected with result code: ' + str(rc))
            self.__client.subscribe("command", 2)
            self.__connected = True
            if self.__on_connect_callback is not None:
                self.__on_connect_callback(client, userdata, flags, rc)

        def __on_message(self, client, userdata, msg):
            for clb in self.__listeners:
                clb(msg.topic, msg.payload)

        def __on_publish(self, client, userdata, mid):
            pass

        def __on_disconnect(self, client, userdata, rc):
            if rc != 0:
                print("Unexpected disconnection")

        def publish(self, topic, message):
            self.__client.publish(topic, message)
            self.__client.loop_write()

        def add_msg_listener(self, callback):
            self.__listeners.append(callback)



    __instance = None

    @staticmethod
    def get_instance():
        if not MqttClient.__instance:
            raise ResourceWarning("Client is not initialized yet.")
        return MqttClient.__instance
    
    @staticmethod
    def init(on_connect_callback):
         MqttClient.__instance = MqttClient.__MqttClient(MqttClient.__get_client_id(), on_connect_callback)

    @staticmethod
    def __get_client_id():
        try:
            cpuinfo = open('/proc/cpuinfo', 'r').read()
            result = re.search('Serial.*: (.*)', cpuinfo)
            return result.group(1)
        except:
            print(sys.exc_info()[0])
            return "cannot found serial"



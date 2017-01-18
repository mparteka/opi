import time
from button import Button
from command_factory import CommandFactory
from switch_command import SwitchCommand
from mqtt_client import MqttClient
from pyA20.gpio import gpio
from pyA20.gpio import port
import re
import threading
from temperature import TemperatureSensorDriver

gpio.init()
gpio.setcfg(port.PA14, gpio.OUTPUT)
gpio.setcfg(port.PA13, gpio.OUTPUT)

    
def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))
    client.subscribe("command", 2)
    send_temperature()


MqttClient.init(on_connect)
client = MqttClient.get_instance()

temp_driver = TemperatureSensorDriver()
def send_temperature():
    temperatures = temp_driver.read_temperature()
    for (dev, temp) in temperatures.items():
        client.publish('TEMPERATURE', dev + " " + temp)
    threading.Timer(10, send_temperature).start()



def pin_state_listener(pin):
    client.publish("PIN_STATUS", str(pin) + " " + str(gpio.input(pin) ))

switch_command = SwitchCommand(SwitchCommand.get_command_string("SWITCH", port.PA13), pin_state_listener)
button = Button(port.PD14, switch_command)

   
def msg_listener(topic, msg):
    if topic == "command":
        msg = msg.decode('UTF-8')
        command = CommandFactory.get_command(msg)
        command.set_listener(pin_state_listener)
        command.execute()

client.add_msg_listener(msg_listener)

while True:
    time.sleep(1)


import paho.mqtt.client as mqtt
import time
import re
import threading

topic = 'message'
broker = '192.168.0.12'
port = 8000
qos = 2

client_id = 'OPi'
client = mqtt.Client("Opi", True, None, mqtt.MQTTv31)

def publish_temp():
    input = open("/sys/bus/w1/devices/28-80000004920e/w1_slave").read()
    result = re.search('t=(\d{5})', input).group(1)
    client.publish('Opi',  int(result)/1000, qos)
    print("Published")


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    threading.Timer(3, publish_temp).start()



client.on_connect = on_connect
print("Connecting...")
client.connect(broker, port, 60)
print('After...')
client.loop_forever()
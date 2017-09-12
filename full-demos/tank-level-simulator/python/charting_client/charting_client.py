""" Tank Level Simulation Charting Client

This script demonstrates the following:
- Subscribe to sensor data via MQTT
- Display sensor data in a web page
"""

import time

from flask import Flask, render_template
import paho.mqtt.client as mqtt

MOSQUITTO_ADDRESS = '127.0.0.1'
MOSQUITTO_PORT = 1883

app = Flask(__name__)

level_received = ""
level_collection = []

def on_connect(client, userdata, rc, x):
    print("Connected with result code", str(rc))
    client.subscribe("demo/sensors")

def on_message(client, userdata, msg):
    global level_received
    print (msg.topic + " " + str(msg.payload))
    level_received = str(msg.payload)
    print "This is level received: ", level_received
    level_collection.append(level_received)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

''' connecting and disconnecting to get the latest
    data point '''
################ CHANGE IP ADDRESS BELOW ###############
def get_level():
    client.connect(MOSQUITTO_ADDRESS, MOSQUITTO_PORT, 60)
    client.loop_start()
    time.sleep(0.1)
    client.loop_stop()

@app.route('/')
def index():
    return render_template('charting_client_website.html')

''' /updater is an API endpoint to retrieve the latest
    data point for our JS handler '''
@app.route('/updater')
def updater():
    get_level()
    return str(level_collection[-1])

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')

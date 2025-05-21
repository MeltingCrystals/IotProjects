#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import os
import sys
import requests
import json
import paho.mqtt.client as mqtt

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)  # LED connected to GPIO pin 11

# MQTT Broker settings
MQTTHOST = "192.168.5.20"
CLIENT_NAME = "IoTXY"
PORT = 1883
KEEPALIVE = 600
QOS_LEVEL = 0

# MQTT Topics
MQTT_SUBSCRIBE_TOPIC = "pi/20/actuators/led/set"  # Only listen to pi/20
MQTT_PUBLISH_TOPIC = "pi/20/actuators/led/get"
MQTT_LED_STATE_ON = "On"
MQTT_LED_STATE_OFF = "Off"


# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    print("Connection successful, subscribing to topic...")
    client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=QOS_LEVEL)
	

# Callback function for receiving MQTT messages
def on_message(client, userdata, message):
    print("Message received:    " + str(message.payload.decode("utf-8")))
    print("Message topic:       " + message.topic)

    try:
        decodedMessage = json.loads(str(message.payload.decode("utf-8")))

        # Check if the message contains the 'Led' key
        if 'Led' in decodedMessage:
            print("Decoding message...")
            if decodedMessage['Led'] == "On":
                GPIO.output(11, GPIO.HIGH)  # Turn the LED on
                print("LED is ON")
                # Acknowledge by publishing the state to the topic
                MQTT_PUBLISH_PAYLOAD = json.dumps({'Led': MQTT_LED_STATE_ON})
                client.publish(MQTT_PUBLISH_TOPIC, MQTT_PUBLISH_PAYLOAD, qos=QOS_LEVEL)
            
            elif decodedMessage['Led'] == "Off":
                GPIO.output(11, GPIO.LOW)  # Turn the LED off
                print("LED is OFF")
                # Acknowledge by publishing the state to the topic
                MQTT_PUBLISH_PAYLOAD = json.dumps({'Led': MQTT_LED_STATE_OFF})
                client.publish(MQTT_PUBLISH_TOPIC, MQTT_PUBLISH_PAYLOAD, qos=QOS_LEVEL)
        else:
            print("No 'Led' key in message.")
    
    except json.JSONDecodeError:
        print("Error decoding JSON message")

# Callback function for MQTT log messages
def on_log(client, userdata, level, buf):
    print("Log: " + buf)

try:
    # Initialize MQTT client
    client = mqtt.Client(CLIENT_NAME)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log

    # Set username and password for MQTT broker if required
    # client.username_pw_set("username", "password")

    # Connect to MQTT Broker
    print("Connecting to MQTT broker...")
    client.connect(MQTTHOST, PORT, KEEPALIVE)

    # Start the MQTT client loop to handle incoming messages
    print("Connected and ready to listen...")
    client.loop_forever()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
    sys.exit(0)

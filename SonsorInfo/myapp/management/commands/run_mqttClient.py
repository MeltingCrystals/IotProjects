from django.core.management.base import BaseCommand
from myapp.models import *

import os
import sys
import django
import json
import paho.mqtt.client as mqtt

class Command(BaseCommand):
    help = 'Invokes the mqtt client and subscribes to the thingspeak server'

    def handle(self, *args, **options):

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected successfully")
                for topic in MQTT_TOPICS:
                    client.subscribe(topic)
            else:
                print("Connection failed with code " + str(rc))

        def on_message(client, userdata, msg):
            print("message topic: " + msg.topic)
            print("message received: " + str(msg.payload.decode("utf-8")))
            data = json.loads(str(msg.payload.decode("utf-8")))

            channel = data['channel_id']
            creationDate = data['created_at']
            entryNumber = data['entry_id']
            humidity = data['field1']
            temperature = data['field2']
            accelx = data['field3']
            accely = data['field4']
            accelz = data['field5']
            latitude = data['field6']
            longitude = data['field7']

            # Create a new database entry
            entry = TemperatureAndHumidityData(
                temperature=temperature,
                humidity=humidity,
                lat=latitude,
                lon=longitude,
                accelx=accelx,
                accely=accely,
                accelz=accelz,
                timestamp=creationDate
            )
            entry.save()

        def on_log(client, userdata, level, buf):
            print("log: " + buf)

        # ThingSpeak MQTT Broker: do not change
        THINGS_DEVICE_MQTTSERV = "mqtt3.thingspeak.com"

        # Channel ID: Enter your channel id!
        CHANNELID = "2753016"

        # ThingSpeak Device user name: Enter your personal user name!
        THINGS_DEVICE_USERNAME = "OSAaIBMMET0fEw0YISYZCTI"

        # ThingSpeak Device password: Enter your password!
        THINGS_DEVICE_PASSWORD = "TdCV9HxQCaOoDN+FEXLWj7gi"

        # ThingSpeak Device client id: Enter the client id!
        CLIENT_NAME = "OSAaIBMMET0fEw0YISYZCTI"

        # ThingSpeaks standard MQTT port number: do not change
        PORT = 1883

        # Some additional parameters: leave these values unchanged
        KEEPALIVE = 600
        QOS_LEVEL = 0

        MQTT_BROKER = "mqtt.thingspeak.com"
        MQTT_PORT = PORT
        MQTT_CHANNEL_ID = CHANNELID
        MQTT_API_KEY = "LPDJO898WDDCR3JR"
        MQTT_TOPICS = [
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field1",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field2",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field3",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field4",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field5",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field6",
            f"channels/{MQTT_CHANNEL_ID}/subscribe/fields/field7"
        ]

        client = mqtt.Client()
        client.username_pw_set(THINGS_DEVICE_USERNAME, MQTT_API_KEY)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(MQTT_BROKER, MQTT_PORT, KEEPALIVE)
        client.loop_forever()

#!/usr/bin/env python

import os
import requests
import json
import paho.mqtt.publish as publish	# Update Channel via MQTT publish messages


# Use Paho MQTT client; three MQTT connection methods exist:
# - conventional TCP socket on port 1882: useUnsecuredTCP=True 
#   (uses the least amount of system ressources) 
# - WebSockets (useful when default MQTT port in blocked on local network, 
#   uses port 80): useUnsecuredWebsockets=True
# - SSL (if encryption is required, uses port 443): useSSLWebsockets=True
useUnsecuredTCP=False
useUnsecuredWebsockets=False
useSSLWebsockets=True

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 80

# Define ThingSpeak Write API Key
THINGSWRITEKEY = "LPDJO898WDDCR3JR"

# Define ThingSpeak Read API Key
THINGSREADKEY = "KU6FVPMGNQHGCQOT"

# Define ThingSpeak Channel ID
CHANNELID = "2753016"

# ThingSpeak Server: DNS Name
MQTTHOST = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "HAg6Og4KNiE9ChUkHQkJJCI"
mqtt_username  = "HAg6Og4KNiE9ChUkHQkJJCI"
mqtt_password  = "TwaN8q4VemaRIOKb4oXSDXH2"

# -------------------------------------------------------------
#print "\nUpdate a channel via HTTP/REST interface"

#tPayload = {'api_key' : THINGSWRITEKEY }
#i = 1
#with os.popen("~/IoT/TempAndHumidity/th02.py") as handle:
#	for line in handle:
#		lineContend = line.split(' ')
#		ind = lineContend.index(":")
#		value = float(lineContend[ind+1])
#		field = "field{0}".format(i)
#		tPayload[field] = value
#		i +=1 
#print tPayload

#url_get = 'https://api.thingspeak.com/update'
#r = requests.get(url_get, data=tPayload)
#if r.status_code !=200:
#	print(r.text)

# -------------------------------------------------------------

print "\nBegin------>"
# Create the topic string (MQTT)
# and attempt to publish data to the topic 
# using the MQTT client via websockets
print "\nUpdate a channel via an MQTT client and websockets:"

topic = "channels/" + CHANNELID + "/publish"
print topic

i = 1
tPayloadMQTT = ""
with os.popen("~/IoT/TempAndHumidity/th02.py") as handle:
	for line in handle:
		if i>1:
			tPayloadMQTT += "&"
		lineContend = line.split(' ')
		ind = lineContend.index(":")
		value = float(lineContend[ind+1])
		field = "field{0}={1}".format(i,value)
		tPayloadMQTT += field
		i +=1 
print tPayloadMQTT

try:
	publish.single(topic, payload=tPayloadMQTT, hostname=MQTTHOST, transport=tTransport, port=tPort, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
except:
	print("There was an error while publishing the data!")

print "\n------>"

# -------------------------------------------------------------

print "\nGet a channel feed via HTTP/REST interface:"

tPayload_get = {'api_key' : THINGSREADKEY , 'results' : '1' }
url_get = 'https://api.thingspeak.com/channels/' + CHANNELID + '/feeds.json'
r = requests.get(url_get, data=tPayload_get)
print r.status_code
print r.text
text = json.loads(r.text)
feed = text['feeds'][0]
channel = text['channel']
print "\nattributes--->"
print "Sensor name: %s" % (channel['name'])
print "Creation time: %s" % (feed['created_at'])
print "Entry number: %s" % (feed['entry_id'])
print "Temperature: %s" % (feed['field2'])
print "Humidity: %s" % (feed['field1'])
print "Latitude: %s" % (channel['latitude'])
print "Longitude: %s" % (channel['longitude'])
print "AccelX: %s" % (feed['field3'])
print "AccelY: %s" % (feed['field4'])
print "AccelZ: %s" % (feed['field5'])
print "<---attributes"
print "\n------>End"

#url_get = 'https://api.thingspeak.com/channels/' + CHANNELID + 'status.json'
#r = requests.get(url_get)
#print r.status_code
#print r.text

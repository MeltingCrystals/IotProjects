import os
import requests
import json
import paho.mqtt.publish as publish
import ssl  # we want to use secured web sockets

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from myapp.models import TemperatureAndHumidityData

def index(request):
    # Get the most actual database entry
    tempData = TemperatureAndHumidityData.objects.order_by('-id').first()

    # Check if we have data in the database
    if tempData:
        temperature = tempData.temperature
        humidity = tempData.humidity
        lat = tempData.lat
        lon = tempData.lon
        accelx = tempData.accelx
        accely = tempData.accely
        accelz = tempData.accelz
        timestamp = tempData.timestamp
    else:
        # Default values if there's no data
        temperature = None
        humidity = None
        lat = None
        lon = None
        accelx = None
        accely = None
        accelz = None
        timestamp = None

    template = loader.get_template("myapp/index.html")
    context = {
        'temperature': temperature,
        'humidity': humidity,
        'lat': lat,
        'lon': lon,
        'accelx': accelx,
        'accely': accely,
        'accelz': accelz,
        'timestamp': timestamp,
    }
    return HttpResponse(template.render(context, request))
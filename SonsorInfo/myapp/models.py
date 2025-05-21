from django.db import models
    
class TemperatureAndHumidityData(models.Model):
    timestamp = models.CharField(max_length=26)
    temperature = models.CharField(max_length=5)
    humidity = models.CharField(max_length=5)
    lat = models.CharField(max_length=10)
    lon = models.CharField(max_length=10)
    #this was added to print the accel
    accelx = models.CharField(max_length=7)
    accely = models.CharField(max_length=7)
    accelz = models.CharField(max_length=7)
    def __unicode__(self):
        return self.timestamp 

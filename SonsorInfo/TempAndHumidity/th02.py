#!/usr/bin/env python

# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TH02
# This code is designed to work with the TH02_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

import math


# Register addresses
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Get I2C bus
bus = smbus.SMBus(1)

# TH02 address, 0x40(64)
# Select configuration register, 0x03(03)
#		0x11(11)	Normal mode enabled, Temperature
bus.write_byte_data(0x40, 0x03, 0x11)

time.sleep(0.5)

# TH02 address, 0x40(64)
# Read data back from 0x00(00), 3 bytes
# Status register, cTemp MSB, cTemp LSB

repeat_temp = True
while repeat_temp:
	try:
		data = bus.read_i2c_block_data(0x40, 0x00, 3)
		repeat_temp = False
	except:
		repeat_temp = True

# Convert the data to 14-bits
cTemp = ((data[1] * 256 + (data[2] & 0xFC))/ 4.0) / 32.0 - 50.0
fTemp = cTemp * 1.8 + 32

# TH02 address, 0x40(64)
# Select configuration register, 0x03(03)
#		0x01(01)	Normal mode enabled, Relative humidity
bus.write_byte_data(0x40, 0x03, 0x01)

time.sleep(0.5)

# TH02 address, 0x40(64)
# Read data back from 0x00(00), 3 bytes
# Status register, humidity MSB, humidity LSB

repeat_humid = True
while repeat_humid:
	try:
		data = bus.read_i2c_block_data(0x40, 0x00, 3)
		repeat_humid = False
	except:
		repeat_humid = True

# Convert the data to 12-bits
humidity = ((data[1] * 256 + (data[2] & 0xF0)) / 16.0) / 16.0 - 24.0
humidity = humidity - (((humidity * humidity) * (-0.00393)) + (humidity * 0.4008) - 4.7844)
humidity = humidity + (cTemp - 30) * (humidity * 0.00237 + 0.1973)

# Output data to screen
print "Relative Humidity : %.2f %%" %humidity
print "Temperature in Celsius : %.2f C" %cTemp
#print "Temperature in Fahrenheit : %.2f F" %fTemp

#Convert two 8-bit numbers to a 16-bit number
def dataConv(data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for revision 1
address = 0x68       # via i2cdetect
 
# Activate module
bus.write_byte_data(address, power_mgmt_1, 0)
time.sleep(0.5)


repeat_accel = True
while repeat_accel:
	try:
		data = bus.read_i2c_block_data(0x68, 0x3b, 6)
		repeat_accel = False
	except:
	    	repeat_accel = True
 
acceleration_xout = dataConv(data[1], data[0])
acceleration_yout = dataConv(data[3], data[2])
acceleration_zout = dataConv(data[5], data[4])
 
# Output data to screen
print "AccelX : %.2f " %acceleration_xout
print "AccelY : %.2f " %acceleration_yout
print "AccelZ : %.2f " %acceleration_zout


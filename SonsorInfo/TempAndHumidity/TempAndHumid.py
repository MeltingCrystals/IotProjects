# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TH02
# This code is designed to work with the TH02_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# TH02 address, 0x40(64)
# Select configuration register, 0x03(03)
#		0x11(11)	Normal mode enabled, Temperature
bus.write_byte_data(0x40, 0x03, 0x11)
time.sleep(0.5)

print "--------------------------"
print " TempSensor initialized  :"
print "--------------------------"
print

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

print "--------------------------"
print " HumidSensor initialized :"
print "--------------------------"
print

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
print "Relative Humidity [Percent]: %.2f %%" %humidity
print "Temperature [Celsius]      : %.2f C" %cTemp
print "Temperature [Fahrenheit]   : %.2f F" %fTemp

#!/usr/bin/python

import smbus
import math
import time
 
# Register addresses
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Convert two 8-bit numbers to a 16-bit number
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
print "---------------------"
print "Module activated    :"
print "---------------------"
print

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
print "acceleration_zout: ", ("%6d" % acceleration_zout), " normalized: ", acceleration_zout_normalized
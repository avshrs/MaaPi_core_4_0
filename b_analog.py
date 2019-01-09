#!/usr/bin/python
import math
import smbus
import time
 
bus = smbus.SMBus(1)

def read():
   data_=[0,0,0,0]
   bus.write_byte(0x48,0x00)
   time.sleep(0.001)
   for i in range(0,100):
	data_ = bus.read_byte_data(0x48,0x00)
	print data_


read()


#!/usr/bin/python
import math
import smbus
import time
 
bus = smbus.SMBus(1)


def read():
   #data_=[0,0,0,0]
   data = [[],[],[],[]] 
   inter = 100
#   bus.write_byte(0x48,0x00)
#   time.sleep(0.001)

   for i in range(0,4):	
      bus.write_byte(0x48,i)
      time.sleep(0.002)
      for ii in range(0,inter):
         data[i].append(bus.read_byte(0x48))
	 time.sleep(0.0009)
   return data

def toV(data):
   out = [0,0,0,0]
   vcc = 2.25
   ratio = vcc / 256
   for i in range(0,4): 
      out[i] = max(data[i])*ratio
      if i == 0: 
         out[i]*=190
   return out

def toA(data):
   print type(data)
   out = [0,0,0,0]
   ratio = 1/30
   for i in range(1,4):
      out[i] = max(data[i]) * ratio
   return out 

def toW(data):
   out = [0,0,0,0]
   ratio = 234
   for i in range(1,4):
      out[i] = max(data[i])*ratio
   return out

readings = read()
volts = toV(readings)
ampers = toA(volts)
wats = toW(ampers)

for i in wats:
  print i


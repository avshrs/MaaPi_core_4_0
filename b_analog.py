#!/usr/bin/python
import math
from smbus2 import SMBus, i2c_msg
import time
 
bus = SMBus(1)
sens = (0,1,2,3)

def read():
   data = [[],[],[],[]] 
   inter = 100
   for i in sens:	

      #bus.write_byte(0x48,i)
      write = i2c_msg.write(0x48, [i])
      read = i2c_msg.read(0x48,1)      
      for ii in range(0,inter):
         data[i].append(bus.i2c_rdwr(write,read))
   print data
   return data

def toV(data):
   out = [0,0,0,0]
   vcc = 2.25
   ratio = vcc / 256
   for i in range(0,4): 
      out[i] = max(data[i])*ratio
   return out

def toA(data):
   for i in range(1,4):
      if data[i] > 0 and data[i]<1.3:
         data[i] = data[i] / 0.0333333
   return data

def toW(data):
   ratio = 234
   for i in range(1,4):
      data[i]*=ratio
   return data

def toVolts(data): 
   ratio = 190
   data[0]*=190
   return data


readings = read()
volts = toV(readings)
ampers = toA(volts)
wats = toW(ampers)
out = toVolts(wats)

for i in sens:
   if i != 0:
      print ("{0}\t max_read= {1}\t volts= {2:.1f} \tampers= {3:.1f} \twats= {4:.1f} ".format(i,max(readings[i]),volts[i],ampers[i],wats[i]))
   else:
      print "{0}\t max_read= {1} \t\t\t\t\tsieci ={2:.2f}".format(i,max(readings[i]),out[i])


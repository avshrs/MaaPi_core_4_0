#!/usr/bin/python
import math
from smbus2 import SMBus, i2c_msg
import time
import datetime as dt
import os
bus = SMBus(1)
sens = (0,1,2,3)
start =dt.datetime.now()
inter = 3

pause = 0.001


def read(sensor):
   counter = 3
   accuracy = 50
   bus.write_byte(0x48,0x04)
   counter = inter
   out = []
   for ix in range(0,accuracy):
      data = bus.read_i2c_block_data(0x48,int(sensor),32)[1:]
      if  data[1] > 1 and data[2] > 1:
         for dat in data:
             out.append(dat)
         counter -= 1
         if counter < 1:
            break
   return out

def avg(data):
    data_ = 0.0
    for i in data:
        data_+= float(i)
    return data_/(len(data))

def toV(data):
   out = [0,0,0,0]
   vcc = 2.29
   ratio = vcc / 256.0
   for i in range(0,4): 
      out[i] = avg(data[i])*ratio
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

pause = 0.001
data=[[],[],[],[]]
for x in range(0,4):
    readings = read(x)
  
   
print data
volts = toV(data)
print volts
ampers = toA(volts)
print ampers
wats = toW(ampers)
print wats
out = toVolts(wats)
print out

stop =dt.datetime.now()
print stop - start
for i in sens:
    if i != 0:
        print ("{0}\t max_read= {1}\t volts= {2:.1f} \tampers= {3:.1f} \twats= {4:.1f} ".format(i,volts[i],volts[i],ampers[i],wats[i]))
    else:
        print "{0}\t max_read= {1} \t\t\t\t\tsieci ={2:.2f}".format(i,volts[i],out[i])


    

 

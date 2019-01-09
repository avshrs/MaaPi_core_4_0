#!/usr/bin/python
import math
from smbus2 import SMBus, i2c_msg
import time
import os
bus = SMBus(1)
sens = (0,1,2,3)

def read():
    data = [[],[],[],[]] 
    out = [[],[],[],[]] 
    it = 10
    data_ =[]
    bus.read_i2c_block_data(0x48,0,1)
    for i in range(0,it):
        for ii in range(0,4):
            data[ii].append(bus.read_i2c_block_data(0x48,ii,31)[10::10])
            time.sleep(0.001)

    
    d=0
    for dii in data:
        for ii in dii:
            for i in ii:
               
                out[d].append(i) 
        d+=1
	
    return out

def toV(data):
   out = [0,0,0,0]
   vcc = 2.28
   ratio = vcc / 256
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

data=[[0],[0],[0],[0]]
for x in range(0,9):
    readings = read()
    for c in range(0,4):
          data[c].append(max(readings[c]))
        
    time.sleep(0.1)
print data
volts = toV(data)
ampers = toA(volts)
wats = toW(ampers)
out = toVolts(wats)

for i in sens:
    if i != 0:
        print ("{0}\t max_read= {1}\t volts= {2:.1f} \tampers= {3:.1f} \twats= {4:.1f} ".format(i,max(data[i]),volts[i],ampers[i],wats[i]))
    else:
        print "{0}\t max_read= {1} \t\t\t\t\tsieci ={2:.2f}".format(i,max(data[i]),out[i])


    

 

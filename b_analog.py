#!/usr/bin/python
import math
import smbus
import time
#import curses
 
bus = smbus.SMBus(1)

def toV(input): 
   vcc  = 3.3
   ra = vcc/256
   print input
   return input * ra


def read(sens):
   aout=[]
   bus.write_byte(0x48,sens)
   time.sleep(0.001)
   data_ = bus.read_i2c_block_data(0x48,0)
#   data_ = bus.read_byte(0x48)
   data_da = 0 
   for da in data_:
     # if data_da < da:
         data_da += da
   return  data_da / len(data_)

def toA(val):
    return val/0.033333333333

def toW(val):
    return val*235

volts=[0,0,0,0]
sens=(0,1,2,3)
rr=10

for a in range(0,rr):
  for i in sens:
    int_ = read(i)
    volt = toV(int_)
    if volt > 0 or volts <1.3:
        if volts[i] < volt :
             volts[i] = volt 
  



for i in sens:
   v= volts[i]
   ampers = toA(v)
   wats  = toW(ampers)
   if i == 1:
      print "{0}:\t\t\tvolts={1:.4f} V Volts={2:.4f} V".format(i,v, v*190)  
   else:
       print "{0}:volts={1:.4f}  235V * {2:.2f}A\t = {3:.2f}W ".format(i,v,ampers, wats)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

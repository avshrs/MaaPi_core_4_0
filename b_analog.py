#!/usr/bin/python
import math
import smbus
import time
#import curses
 
bus = smbus.SMBus(1)

def toV(input): 
   vcc  = 2.21
   range = vcc/256
   return input * range

#220ko
#1,2ko
#230 = 1.248

#   range = ((VCC)/256)
#   return ((range)*input)-VGND

def read(sens):
   bus.write_byte(0x48,sens) 
#   time.sleep(0.002)
   return  bus.read_byte(0x48)

def toA(val):
    return val/0.033333333333

def toW(val):
    return val*235

volts=[0,0,0,0]

rr=500

for a in range(0,rr):
  for i in range(0,4):
    int_ = read(i)
    volt = toV(int_)
    if volt < 0 or volt >1.4:
       continue 
    if volts[i] < volt:    
       volts[i] = volt	
  time.sleep(0.001)



for i in range(0,4):
   v= volts[i]

   ampers = toA(v)
   wats  = toW(ampers)
   if i==1:
      print "{0}:                               volts={1:.4f}v ".format(i,v*190)  
   else:
      print "{0}:volts={1:.4f}  235V * {2:.2f}A\t = {3:.2f}W ".format(i,v,ampers, wats)


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

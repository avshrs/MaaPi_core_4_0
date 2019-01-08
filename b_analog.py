#!/usr/bin/python
import math
import smbus
import time
#import curses
 
bus = smbus.SMBus(1)

def toV(input): 
   vcc  = 3.3
   vgnd = vcc/2
   range = (vcc)/256
   return (input* range) - vgnd

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

rr=1000
for a in range(0,rr):
  for i in range(0,4):
    ints = read(i)
    volt = toV(ints)
    if volt < -1 or volt > 1:
       continue
       
    if volt < 0:
       volt *= (-1)
    volts[i]+=volt*volt




for i in range(0,4):
   v= math.sqrt(volts[i]/rr)
   ampers = toA(v)
   wats  = toW(ampers)
   print "{0}:volts={1:.4f}  235V * {2:.2f}A\t = {3:.2f}W ".format(i,v,ampers, wats)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

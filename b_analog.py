#!/usr/bin/python
import math
import smbus
import time
import curses
 
bus = smbus.SMBus(1)

def toV(input): 
   VCC  = 3.28 
   VGND = 1.63
   range = ((VCC - VGND)/128)
   return ((range)*input)-VGND

def read(sens):
   bus.write_byte(0x48,sens) 
   time.sleep(0.002)
   return  bus.read_byte(0x48)

def toA(val):
    return val/0.033

def toW(val):
    return val*235

for i in range(0,4):
    ints = read(i)
    volts = toV(ints)
    if volts < -1.6:
       continue 
    ampers = toA(volts)
    wats  = toW(ampers)
    print "{0}:ints={1:.2f} \tvolts={2:.2f}\t  235V * {3:.2f}A\t = {4:.2f}W ".format(i,ints,volts,ampers,wats)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

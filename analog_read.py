#!/usr/bin/python

import smbus
import time
import curses
 
bus = smbus.SMBus(1)

aout = 0

def convert(input):
   return input*(16.5/256)
   


for a in range(0,4):
   addr = 0x40 | a
   bus.write_byte(0x48,a)
   time.sleep(0.01)
   reading = bus.read_byte(0x48)

   conV = convert(reading)
   conA = conV/0.033333
   conW = conA*235
   print "{0}: 235V - {1}A = {2}W".format(a,conA, conW)
      
#xtime.sleep(0.1)

 
#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

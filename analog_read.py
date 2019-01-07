#!/usr/bin/python

import smbus
import time
import curses
 
bus = smbus.SMBus(1)

aout = 0

for a in range(0,4):
      aout = aout + 1
      bus.write_byte(0x48,a)
      v = bus.read_byte(0x48)
      #hashes = v / 4
      #spaces = 64 - hashes
      print  str(v)
      
time.sleep(0.1)

 

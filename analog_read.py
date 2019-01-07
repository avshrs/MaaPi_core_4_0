#!/usr/bin/python

import smbus
import time
import curses
 
bus = smbus.SMBus(1)

aout = 0

def convert(input):
   return input*(16.5/256)
v1 =0
v2=0
v3=0
v4=0
val0=0
val1=0
val2=0
val3=0
for i in range(0,100):
      bus.write_byte(0x48,0)
      time.sleep(0.001)
      v0 = bus.read_byte(0x48)
      if val0 > v0:
         val0 = v0
      bus.write_byte(0x48,1)
      time.sleep(0.001)
      v1 = bus.read_byte(0x48)
      if val1 > v1:
         val1 = v1  
      bus.write_byte(0x48,2)
      time.sleep(0.001)
      v2 = bus.read_byte(0x48)
      if val2 > v2:
         val2 = v2 
      bus.write_byte(0x48,3)
      time.sleep(0.001)
      v3 = bus.read_byte(0x48)
      if val3 > v3:
         val3 = v3   

conV0 = convert(val0)
conA0 = conV0/0.3333333
conW0 = conA0*235
print "{0}: 235V - {1}A = {2}W".format(0,conA0, conW0)
conV1 = convert(val1)
conA1 = conV1/0.3333333
conW1 = conA1*235
print "{0}: 235V - {1}A = {2}W".format(1,conA1, conW1)  
conV2 = convert(val2)
conA2 = conV2/0.3333333 
conW2 = conA2*235
print "{0}: 235V - {1}A = {2}W".format(2,conA2, conW2)   
conV3 = convert(val3)
conA3 = conV3/0.3333333
conW3 = conA3*235
print "{0}: 235V - {1}A = {2}W".format(3,conA3, conW3)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

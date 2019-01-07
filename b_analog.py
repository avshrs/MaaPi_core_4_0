#!/usr/bin/python
import math
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
a=1

for i in range(0,a):
      bus.write_byte(0x48,0)
      
      v0 = bus.read_byte(0x48)
      val0 += v0*v0

      bus.write_byte(0x48,1)
      
      v1 = bus.read_byte(0x48)
      val1 += v1*v1  

      bus.write_byte(0x48,2)
      
      v2 = bus.read_byte(0x48)
      val2 += v2 * v2

      bus.write_byte(0x48,3)
      time.sleep(0.001)
      v3 = bus.read_byte(0x48)

      val3 += v3 * v3   
      time.sleep(0.001)

conV0 = convert(math.sqrt(val0/a))
conA0 = conV0/0.03333333
conW0 = conA0*235
print "{0}:{3} 235V - {1}A = {2}W \t {4}".format(0,conA0, conW0,val0, v0)
conV1 = convert(math.sqrt(val1/a))
conA1 = conV1/0.03333333
conW1 = conA1*235
print "{0}:{3} 235V - {1}A = {2}W \t {4}".format(1,conA1, conW1,val1, v1)  
conV2 = convert(math.sqrt(val2/a))
conA2 = conV2/0.03333333 
conW2 = conA2*235
print "{0}:{3} 235V - {1}A = {2}W \t {4}".format(2,conA2, conW2,val2, v2)   
conV3 = convert(math.sqrt(val3/a))
conA3 = conV3/0.03333333
conW3 = conA3*235
print "{0}:{3} 235V - {1}A = {2}W \t {4}".format(3,conA3, conW3,val3, v3)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

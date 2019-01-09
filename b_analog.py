#!/usr/bin/python
import math
import smbus
import time
#import curses
 
bus = smbus.SMBus(1)
def toV(input): 
   vcc  = 3.3
   ra = vcc/256
   out=[0,0,0,0]
   for i in range(0,3):
#      print out[i]
      out[i]= input[i]*ra
   return out


def read():
   data_=[0,0,0,0]
   bus.write_byte(0x48,0x44)
   time.sleep(0.002)
   data_ = bus.read_i2c_block_data(0x48,0)
   print data_
   data_ = bus.read_block_data(0x48,3)
   print data_

#   for i in range(0,3):
#      data_[i] = bus.read_byte(0x48)
#   data_da = 0 
#   for da in data_:
     # if data_da < da:
#         data_da += da
   return  data_

def toA(val):
   out=[0,0,0,0]
   for i in range(0,3):
#      print val[i]
      out[i]= val[i]*0.0333333
   return out

def toW(val):
   out=[0,0,0,0]
   for i in range(0,3):
#      print val[i]
      out[i]= val[i]*235
   return out

volts=[0,0,0,0]
sens=(0,1,2,3)
rr=5

for a in range(0,rr):
  print "\n"
  int_ = read()
  volt = toV(int_)
  for i in sens:
#    int_ = read()
#    volt = toV(int_)
    if volt > 0 or volts[i] < 1.3:
        if volts[i] < volt :
             volts[i] = volt 
  



for i in sens:
   v= volts[i]
   ampers = toA(v)
   wats  = toW(ampers)
#   if i == 1:
#      print "{0}:\t\t\tvolts={1:.4f} V Volts={2:.4f} V".format(i,v, v*190)  
#   else:
 #      print "{0}:volts={1:.4f}  235V * {2:.2f}A\t = {3:.2f}W ".format(i,v,ampers, wats)  


#7 6 5 4 3 2 1 0
#0 A B B 0 C D D 

#0 0 0 0 0

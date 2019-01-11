#!/usr/bin/python
import math
from statistics import median, stdev
from smbus2 import SMBus, i2c_msg
import time
import datetime as dt
import os


class pcfxxxxi2(object):
   bus = SMBus(1)
    
   def avg(self,data):
        data_ = 0
        for i in data:
            data_+= i
        return data_/(len(data))
                                       

   def read(self,sensor):
      counter = 10
      accuracy = 200
      add=0x4c

      self.bus.write_byte(add,0x00)
      out = []
      for ix in range(0,accuracy):
        data = self.bus.read_i2c_block_data(add,sensor,32)

        if  data[12] > 0 and data[12] < 254 and data[26] < 240 and data[0] < 240:
            for da in data:
                out.append(da)
            counter -= 1
            if counter < 1:
               break
      return out

   def convert(self,data,type_):
        volts=[]
        ampers=0
        wats=0
        volt=0
        factor = 2.29 / 256.0  
        for di in data:
            idd = (di * (factor) - 0.57) * 190
            volts.append(idd)
         

            
       
        volt = max(volts)
        print volt 
        ampers = min(volts)
        print ampers
        print "\n"
        return volt,ampers,wats


   def __init__(self,args):
      for iii in range(0,3):
         data = self.read(iii)
         volt, amper, wat = self.convert(data,iii)
         print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.1f} ".format(iii,volt,amper,wat))


start = dt.datetime.now()
read = pcfxxxxi2(1) 

stop = dt.datetime.now()
print stop-start

      

   

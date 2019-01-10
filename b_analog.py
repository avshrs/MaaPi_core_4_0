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
      counter = 20
      accuracy = 50

      self.bus.write_byte(0x48,0x04)
      out = []
      for ix in range(0,accuracy):
         data = self.bus.read_i2c_block_data(0x48,int(sensor),32)[5:]
#	 print data
         if  data[12] > 0 :
            print data
	    time.sleep(0.002)
            out.append(max(data))
            counter -= 1
            if counter < 1:
               break
      out2 = []
      if len(out) < 1:
           out = [0,0,0]
      else:
           std=stdev(out)
           avgg=self.avg(out)
           for o in out:
               if o > (avgg - std) and o < (avgg + std):
                  out2.append(o)            




      print out
      print out2      
      return out2

   def avg(self,data):
      data_ = 0
      for i in data:
         data_+= i
      return data_/(len(data))

   def convert(self,data,type_):
      factor = 2.29 / 256.0  # pfc factor

      if len(data) > 1 and data[0] !=0:
	  dataAvg = median(data)
      else: 
          dataAvg = 0
      print dataAvg
      if type_ != 0:
         volts  = dataAvg * factor 
         ampers = volts / 0.0333333
         wats   = ampers * 235.0
         volts  = 0
      else: 
         volts  = (dataAvg * factor )*190
         ampers = 0
         wats   = 0
      return volts,ampers,wats


   def __init__(self,args):
      for iii in range(1,2):
         data = self.read(iii)
         volt, amper, wat = self.convert(data,iii)
         print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.1f} ".format(iii,volt,amper,wat))


start = dt.datetime.now()
read = pcfxxxxi2(1) 

stop = dt.datetime.now()
print stop-start

      

   

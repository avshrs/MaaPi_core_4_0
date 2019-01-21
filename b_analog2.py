	#!/usr/bin/python
import math
from smbus2 import SMBus, i2c_msg
from statistics import median, stdev, mean
import time
import datetime as dt
import os


class pcfxxxxi2(object):
   
    bus = SMBus(1)

    @classmethod
    def listIsZero(self,data):
	for i in data:
	    if i > 0:
		return True
	return False   

    @classmethod
    def toVolts(self, data, Vmultip,vcc, vccAdjust,reference):
        factor = vcc / 256.0
        out = []
        for di in data:
              volts = (((abs(di-reference) * factor) ) * Vmultip)
              out.append(volts)
        return out

    @classmethod
    def filter_gtavg(self,data,percent):
        data_len = int(len(data)*percent)
        data_avg = mean(data[data_len:])
        data_out = []
        for data_ in data:
            if data_ >= data_avg:
                data_out.append(data_)
        return data_out
    
    @classmethod
    def filter_stdCh(self,data,ChauvenetC,STDdirection):
        out=[]
        avg = mean(data)
        std_ = stdev(data)
        std = std_ * ChauvenetC
        if std != 0:
            for do in data:
                if STDdirection == "all":
                    if do < (avg + std) and do > (avg - std):
                        out.append(do)
                elif STDdirection == "up" :
                    if do < (avg + std):
                        out.append(do)
                elif STDdirection == "down" :
                    if do > (avg - std):
                        out.append(do)
        else:
            out = data
        return out


    @classmethod

    def readFromI2C(self,sensor, address, accuracy):
	#while True:
        self.bus.write_byte(address,sensor)
        read = self.bus.read_i2c_block_data32(address,sensor,accuracy)
	print read        
#  else:
        return read

    @classmethod
    def toAmper(self,data):
        out=[]
        div = 1/30.0
        for i in data:
            if i > 0:
                out.append(i/div)
            else:
                out.append(i)
        return out
    @classmethod
    def toWat(self,data):
        out=[]
        for i in data:
                out.append(i*233)
        return out
    
    @classmethod
    def getSensorConf(self,sensor,address,kind):
        if kind == "W" and address == 0x48:
            Vmultip = 1
            STDfilter = False
            ChauvenetC = 1
            avgToCut     =  0.2
            accuracy = 10
            STDdirection ="all"
            vcc= 3.27
            vccAdjust = vcc/1.96225
            reference    = 127.0
            toAmper = False
            toAmperToWat = True
        elif kind == "A" and address == 0x48:
            Vmultip      = 1
            STDfilter    = True
            ChauvenetC    = 1
            avgToCut     =  0.5
            accuracy     = 60
            STDdirection ="all"
            vcc          = 1.68
            reference    = 0
            vccAdjust    = vcc/1.96225
            toAmper = True
            toAmperToWat = False  
        elif kind == "V" and address == 0x4c and sensor != 3 :
            Vmultip      = 195
            STDfilter    = True
            ChauvenetC   = 1
            avgToCut     =  0.5
            accuracy     = 35
            STDdirection = "all"
            vcc          = 2.2
            vccAdjust    = 0
            reference    = 0
            toAmper = False
            toAmperToWat = False       
        elif kind == "V" and sensor == 3 and address == 0x4c:
            Vmultip      = 1.09
            STDfilter    = True
            ChauvenetC    = 1
            avgToCut     =  0.5
            accuracy     = 10
            STDdirection="all"
            vcc          = 3.3
            vccAdjust    = 0
            reference    = 0
            toAmper = False
            toAmperToWat = False
        
        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc, vccAdjust, toAmper, toAmperToWat, avgToCut, reference
        

    @classmethod
    def getdata(self,sensor,address,kind):
        
        Vmultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc, vccAdjust, toAmper, toAmperToWat, avgToCut , reference = self.getSensorConf(sensor,address,kind)
        
        data = self.readFromI2C(sensor, address, accuracy)
  #      if STDfilter:
        data = self.filter_stdCh(data,ChauvenetC,STDdirection)    


        data = self.toVolts(data, Vmultip, vcc, vccAdjust, reference)
        self.filter_gtavg(data,0.5)
            
#        if STDfilter:
 #           data = self.filter_stdCh(data,ChauvenetC,STDdirection)
       
        if toAmper or toAmperToWat :
            data = self.toAmper(data)
        
        if toAmperToWat:
            data = self.toWat(data)
 #      
        print "min= {0}, \tmax= {1}, \tavg={2}".format(min(data),max(data) ,mean(data))        

        return  max(data)

    def __init__(self,args):
        for i in range(0,1):
            start1 = dt.datetime.now()
            volt  = 0
            amper = 0 
            wat   = self.getdata(i,0x48,"W") 
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.3f} ".format(i,volt,amper,wat))
 
            stop1 = dt.datetime.now()
            print stop1-start1



















start = dt.datetime.now() 
read = pcfxxxxi2(1)
stop = dt.datetime.now() 
print stop-start
      

   

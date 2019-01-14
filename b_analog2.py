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
    def toVolts(self, data, Vmultip,vcc, vccAdjust):
        factor = vcc / 256.0
        out = []
        for di in data:
           if di < 254:
              volts = (((di * factor) - (vccAdjust)) * Vmultip)
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
        data_avg = mean(data)
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
        self.bus.write_byte(address,int(sensor))
        out = []
        for i in range(0,accuracy):
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            out.append(data)
        return out
    @classmethod
    def getSensorConf(self,sensor,address,kind):
        if kind == "W" and address == 0x48:
            Vmultip = 1
            STDfilter = True
            ChauvenetC = 1
            accuracy = 60
            STDdirection ="all"
            vcc= 1.68
            vccAdjust = vcc/1.96225

        elif kind == "A" and address == 0x48:
            Vmultip      = 1
            STDfilter    = True
            ChauvenetC    = 1
            accuracy     = 60
            STDdirection ="all"
            vcc          = 1.68
            vccAdjust    = vcc/1.96225  
        elif kind == "V" and address == 0x4c:
            Vmultip      = 195
            STDfilter    = True
            ChauvenetC   = 1
            accuracy     = 40
            STDdirection = "all"
            vcc          = 2.2
            vccAdjust    = 0
        elif kind == "V" and sensor == 3 and address == 0x4c:
            Vmultip      = 1
            STDfilter    = True
            ChauvenetC    = 0.5
            accuracy     = 2
            STDdirection="all"
            vcc          = 1.68
            vccAdjust    = vcc/2
        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc, vccAdjust
        

    @classmethod
    def getdata(self,sensor,address,kind):
        vMultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc, vccAdjust = self.getSensorConf(sensor,address,kind)
        data_readed = self.readFromI2C(sensor, address, accuracy)
        data_temp = []
        print len(data_readed)
        for dr in data_readed:
            
            if dr[0] > 254:
                if dr[0] == dr[1]:
                    continue
            data_temp.append(dr)
            
        print len(data_temp)


       # filter_gtavg
       # filter_stdCh
        #toVolts
   
        return  max(data_readed)

    def __init__(self,args):
        for iii in range(0,3):
            start1 = dt.datetime.now()
            volt  = 0
            amper = 0 
            wat   = self.getdata(iii,0x48,"W") 
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.3f} ".format(iii,volt,amper,wat))

            stop1 = dt.datetime.now()
            print stop1-start1


        print "\n\n"
	"""
        for iii in range(0,3):
            start2 = dt.datetime.now()
            volt = 0
            amper = 0
            wat = self.getValue(iii,0x4c,"V")
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.3f} ".format(iii,volt,amper,wat))
            stop2 = dt.datetime.now()
            print stop2 - start2                                                                                                                                                                                              
	"""



















start = dt.datetime.now() 
read = pcfxxxxi2(1)
stop = dt.datetime.now() 
print stop-start
      

   

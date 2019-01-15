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
    def toVolts(self, data, Vmultip,vcc, vccAdjust):
        factor = vcc / 256.0
        out = []
        for di in data:
           if di < 254:
              volts = (((di * factor) - (vccAdjust)) * Vmultip)
              out.append(abs(volts))
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
	sensor=0b00000001
	accuracy = 1
	address = 0x4c
	self.bus.write_byte(address,sensor)

        out = []
        for i in range(0,accuracy):
            data = self.bus.read_i2c_block_data32(address,sensor,20)
	    print data
	    print max(data)
        return out

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
            STDfilter = True
            ChauvenetC = 1
            avgToCut     =  0.2
            accuracy = 35
            STDdirection ="all"
            vcc= 1.68
            vccAdjust = vcc/1.96225
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
            toAmper = False
            toAmperToWat = False

        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc, vccAdjust, toAmper, toAmperToWat, avgToCut
        

    @classmethod
    def getdata(self,sensor,address,kind):
        vMultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc, vccAdjust, toAmper, toAmperToWat, avgToCut = self.getSensorConf(sensor,address,kind)
        data_bin_readed = self.readFromI2C(sensor, address, accuracy)
        data_bin_temp = []
        print ("---DEBUG: Data Readed from i2c \t\t| sampels {0}".format(len(data_bin_readed)*32))
#        print data_bin_readed
        for dr in data_bin_readed:
            if dr[0] > 254:
                if dr[0] == dr[1]:
                    continue
            data_bin_temp+=self.filter_gtavg(dr,avgToCut)
        #convert section
        print ("---DEBUG: Data filtered > avg \t\t| sampels {0}".format(len(data_bin_temp)))
        
        data = self.toVolts(data_bin_temp,vMultip,vcc,vccAdjust)
        # filter section 
        if STDfilter:
            data = self.filter_stdCh(data,ChauvenetC,STDdirection)
            print ("---DEBUG: Data filtered STD DIV \t| sampels {0}".format(len(data)))

        if toAmper or toAmperToWat :
            data = self.toAmper(data)
        if toAmperToWat:
            data = self.toWat(data)
        print ("---DEBUG: Data before send to max \t| sampels {0}".format(len(data)))

        return  max(data)

    def __init__(self,args):
        for i in range(0,3):
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
      

   

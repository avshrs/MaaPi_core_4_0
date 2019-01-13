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
        out    = []
        for di in data:
            if di:
                volts = abs(((di * factor) - (vccAdjust)) * Vmultip)
            else: volts = 0
            if volts > 0:
                out.append(volts)
    

        return out
            

    @classmethod
    def readFromI2C(self,sensor, address, Vmultip, accuracy,vcc, vccAdjust):
        self.bus.write_byte(address,int(sensor))
        out = []
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            #print data[5:-2]
            out.append(self.toVolts(data,Vmultip,vcc, vccAdjust))
        return out


    @classmethod
    def dataAnalize(self,sensor, address, readRetray, Vmultip, STDfilter, STDchaver, STDdirection, accuracy ,removeSmallVal,removeHighVal , vcc, vccAdjust):
        data_out = []
        out = []

        if STDfilter :
            for ret in range(0,readRetray):
                data_readed = self.readFromI2C(sensor, address, Vmultip, accuracy,vcc, vccAdjust)
                for dr in data_readed: 
                    for d in dr:
                        data_out.append(d)

            data_out.sort(reverse=True)
            avg  = mean(data_out)
            std_ = stdev(data_out)
            std  = std_ * STDchaver 
            
            if std != 0:
                rsv = int(len(data_out)*removeSmallVal)
                print rsv
                rhv = int(len(data_out)*removeHighVal)
                print rhv
                for do in data_out[int(rhv):(int(rsv)*(-1))]:
                    if STDdirection == "up" or STDdirection == "all":
                        if do < (avg + std):
                            out.append(do)
                    if STDdirection == "down" or STDdirection == "all":
                        if do > (avg - std):
                            out.append(do)
                
            else: 
                out = data_out
        else:
            out = data_out

        return out

            

    @classmethod
    def getValue(self,sensor,address,kind):
        if kind == "W":
            Vmultip = 1
            STDfilter = True
            STDchaver = 0.7
            accuracy = 5       # how many times loop read from sensor 
            readRetray  = 5
            STDdirection="up"
            avgRetry = 6
            dataAvg = []
            removeSmallVal = 0.2
            removeHighVal = 0.1
            vcc = 1.68
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy, removeSmallVal,removeHighVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            wats = ampers * 234.0
            out = wats

        elif kind == "A":
            Vmultip = 1
            STDfilter = True
            STDchaver = 1
            accuracy = 2
            readRetray  = 2
            STDdirection="all"
            avgRetry = 4
            removeSmallVal = 0.2
            removeHighVal = 0.1
            dataAvg = []
            vcc = 1.68
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,removeHighVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out = ampers

        elif kind == "V":
            Vmultip = 195
            STDfilter = True
            STDchaver = 0.5
            accuracy = 5
            readRetray  = 5
            STDdirection="all"
            avgRetry = 2
            removeSmallVal = 0.1
            removeHighVal = 0.1
            dataAvg = []
            vcc = 2.2
            vccAdjust = 0
            for i in range(0,avgRetry):
                dat =self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,removeHighVal,vcc, vccAdjust)
               # print dat
                dataAvg.append(max(dat))
            volts = mean(dataAvg)
            out = volts
        elif kind == "V" and sensor == 3:
            Vmultip = 2.08 
            STDfilter = True
            STDchaver = 0.5
            accuracy = 2  
            readRetray  = 2
            STDdirection="all"
            avgRetry = 2
            removeSmallVal = 0.4
            removeHighVal = 0.1
            dataAvg = []
            vcc = 1.68
            vccAdjust = 0
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,removeHighVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            out = volts
        return out


   

    

    def __init__(self,args):
        for iii in range(0,3):
            volt  = 0
            amper = 0 
            wat   = self.getValue(iii,0x4c,"V") 
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.3f} ".format(iii,volt,amper,wat))



start = dt.datetime.now()
read = pcfxxxxi2(1) 

stop = dt.datetime.now()
print stop-start

      

   

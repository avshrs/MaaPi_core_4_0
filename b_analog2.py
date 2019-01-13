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
    
        print out
        return out
            

    @classmethod
    def readFromI2C(self,sensor, address, Vmultip, accuracy,vcc, vccAdjust):
        self.bus.write_byte(address,int(sensor))
        out = []
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            out.append(self.toVolts(data,Vmultip,vcc, vccAdjust))
        
        return out


    @classmethod
    def dataAnalize(self,sensor, address, readRetray, Vmultip, STDfilter, STDchaver, STDdirection, accuracy ,removeSmallVal, vcc, vccAdjust):
        data_out = []
        out = []
        for ret in range(0,readRetray):
            data_readed = self.readFromI2C(sensor, address, Vmultip, accuracy,vcc, vccAdjust)
            data_temp   = []
            for da in data_readed:
                if da:
                    data_temp.append(max(da))
            data_out.append(max(data_temp))

        if STDfilter :
            avg = mean(data_out)
            std = (stdev(data_out)*STDchaver)
            data_out.sort(reverse=True)
            if std != 0:
                rsv = int(len(data_out)*removeSmallVal)*(-1)
                for do in data_out[:int(rsv)]:
                    if STDdirection == "up" or STDdirection == "all":
                        if do < (avg + std):
                            out.append(do)
                    if STDdirection == "down" or STDdirection == "all":
                        if do > (avg - std):
                            out.append(do)
                
                if out:
                    #self._debug(1, "\tParameter STDchaver {0} is goood data len {1}".format(STDchaver, len(out)))
                    pass
                else:
                    #self._debug(1, "\tParameter STDchaver {0} is bad multiplaying   data len {1}".format(STDchaver, len(out)))
                    std = (stdev(data_out)*(STDchaver*2))
                    for do in data_out[:int(rsv)]:
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
            STDchaver = 0.8
            accuracy = 5       # how many times loop read from sensor 
            readRetray  = 6
            STDdirection="up"
            avgRetry = 4
            dataAvg = []
            removeSmallVal = 0.2
            vcc = 2.9
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy, removeSmallVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            wats = ampers * 234.0
            out = wats

        if kind == "A":
            Vmultip = 1
            STDfilter = True
            STDchaver = 1
            accuracy = 2
            readRetray  = 2
            STDdirection="all"
            avgRetry = 4
            removeSmallVal = 0.2
            dataAvg = []
            vcc = 2.9
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out = ampers

        if kind == "V":
            Vmultip = 205
            STDfilter = True
            STDchaver = 0.8
            accuracy = 6
            readRetray  = 6
            STDdirection="down"
            avgRetry = 2
            removeSmallVal = 0.4
            dataAvg = []
            vcc = 2.9
            vccAdjust = 0
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            out = volts
        return out


    

    def __init__(self,args):
        for iii in range(0,3):
            volt  = 0
            amper = 0
            wat   = self.getValue(iii,0x48,"W") 
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.1f} ".format(iii,volt,amper,wat))



start = dt.datetime.now()
read = pcfxxxxi2(1) 

stop = dt.datetime.now()
print stop-start

      

   

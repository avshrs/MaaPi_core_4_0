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
            volts = abs(((di * factor) - (vccAdjust)) * Vmultip)
            if volts > 0:
                out.append(volts)
        return out
            

    @classmethod
    def readFromI2C(self,sensor, address, Vmultip, accuracy,vcc, vccAdjust):
        self.bus.write_byte(address,int(sensor))
        out = []
        data_out = []
        for ix in range(0,accuracy):
            
            data = self.bus.read_i2c_block_data(address,int(sensor),32)[5:-2]
            data.sort(reverse=True)
            data_len = int(len(data)*0.1)
            leed_avg = mean(data[data_len:])
            for dto in data:
                if dto > leed_avg:
                    data_out.append(dto)
            out.append(self.toVolts(data_out,Vmultip,vcc, vccAdjust)) 
            time.sleep(0.01)
        return out


    @classmethod
    def dataAnalize(self,sensor, address, Vmultip, STDfilter, STDchaver, STDdirection, accuracy , vcc, vccAdjust):
        data_out = []
        data_tmp = []
        out = []

        data_readed = self.readFromI2C(sensor, address, Vmultip, accuracy, vcc, vccAdjust)
        for dad_ in data_readed:
            try:
                data_tmp.append(max(dad_))
            except:
                print data_readed
                raise
        
        data_tmp.sort(reverse=True)
        data_len = int(len(data_tmp)*0.2)
        leed_avg = mean(data_tmp[data_len:])

        for dto in data_tmp:

            if dto > leed_avg:
                data_out.append(dto)
        print data_out
        if STDfilter :
            avg  = mean(data_out)
            std_ = stdev(data_out)
            std  = std_ * STDchaver 
            if std != 0:                
                for do in data_out:
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
                out = data_out
        else:
            out = data_out

        return out

            

    @classmethod
    def getValue(self,sensor,address,kind):
        if kind == "W":
            Vmultip = 1
            STDfilter = True
            STDchaver = 1
            accuracy = 5       # how many times loop read from sensor 
            STDdirection="all"
            avgRetry = 5
            dataAvg = []
            removeSmallVal = 0.2
            vcc = 1.68
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address,  Vmultip, STDfilter,STDchaver, STDdirection, accuracy, vcc, vccAdjust)))
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
            dataAvg = []
            vcc = 1.68
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address,  Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out = ampers

        elif kind == "V":
            Vmultip = 195
            STDfilter = True
            STDchaver = 0.8
            accuracy = 50
            STDdirection="all"
            avgRetry = 2
            
            dataAvg = []
            vcc = 2.2
            vccAdjust = 0
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address,  Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust)))
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
            dataAvg = []
            vcc = 1.68
            vccAdjust = 0
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address,  Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust)))
            volts = mean(dataAvg)
            out = volts
        return out


   

    

    def __init__(self,args):
        for iii in range(0,3):
            start1 = dt.datetime.now()
            volt  = 0
            amper = 0 
            wat   = self.getValue(iii,0x4c,"V") 
            print ("{0}\t volts= {1:.1f} \tampers= {2:.1f} \twats= {3:.3f} ".format(iii,volt,amper,wat))

            stop1 = dt.datetime.now()
            print stop1-start1

start = dt.datetime.now()
read = pcfxxxxi2(1) 

stop = dt.datetime.now()
print stop-start

      

   

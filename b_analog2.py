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
    def toVolts(self, data, Vmultip):
            vcc    = 2.29
            factor = vcc / 256.0
            out    = []
            for di in data:
                volts = abs(((di * factor) - (vcc/2)) * Vmultip)
                if volts > 0:
                    out.append(volts)
           # print ("toVolts {0}".format(out))
            return out
            

    @classmethod
    def readFromI2C(self,sensor, address, Vmultip, accuracy):
        self.bus.write_byte(address,int(sensor))
        out = []
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            out.append(self.toVolts(data,Vmultip))
        
        return out


    @classmethod
    def dataAnalize(self,sensor, address, readRetray, Vmultip, STDfilter, STDchaver, STDdirection, accuracy ):
        data_out = []
        out = []
        for ret in range(0,readRetray):
            data_readed = self.readFromI2C(sensor, address, Vmultip, accuracy)
            data_temp   = []
            for da in data_readed:
                if da:
                    data_temp.append(max(da))
            data_out.append(max(data_temp))

        if STDfilter :
            avg = mean(data_out)
            std = (stdev(data_out)*STDchaver)
            data_out.sort(reverse=True)
            for do in data_out[:-2]:
                if STDdirection == "up" or STDdirection == "all":
                    if do < (avg + std):
                        out.append(do)
                if STDdirection == "down" or STDdirection == "all":
                    if do > (avg - std):
                        out.append(do)
            if  out:
                pass
                #print("filter pass")
            else:
                print("filter error")
                out.append(max(data_out))
            

        return out

            

    @classmethod
    def getValue(self,sensor,address,kind):
        allData = []
        readRetray  = 10
        out     = []

        if kind == "W":
            Vmultip = 1
            STDfilter = True
            STDchaver = 1
            accuracy = 10
            STDdirection="up"
            volts  = max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy))
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out.append(ampers * 234.0)
            
        return max(out)


    

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

      

   

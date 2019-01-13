#!/usr/bin/python

import sys
from statistics import median, stdev, mean
from datetime import datetime as dt
import lib.MaaPi_DB_connection as maapidb
from smbus2 import SMBus, i2c_msg
import time
import logging

logging.basicConfig(
    filename='/home/pi/MaaPi110/bin/logs/Maapi_Selector.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S')

class class_get_values(object):
    debug = 1
    
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            logging.debug("lib_maapi_pcf8591_i2c - {0}".format(msg))

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
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            if data[10] > 0 and data[10]<250 and data[20] > 0 and data[20]<250 :
                out.append(self.toVolts(data[5:-2],Vmultip,vcc, vccAdjust))
            if out:
                out.append((0,0))
        
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
                else: continue

            data_out.append(max(data_temp))

        if STDfilter :
            avg  = mean(data_out)
            std_ = stdev(data_out)
            std  = std_ * STDchaver 
            data_out.sort(reverse=True)
            if std != 0:
                rsv = int(len(data_out)*removeSmallVal)*(-1)
                
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
                
                if out:
                    self._debug(1, "\tParameter STDchaver {0} is goood data len {1}".format(STDchaver, len(out)))
                else:
                    self._debug(1, "\tParameter STDchaver {0} is bad multiplaying   data len {1}".format(STDchaver, len(out)))
                    std  = std_ * STDchaver 
                    for do in data_out[:int(rsv)]:
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
            readRetray  = 5
            STDdirection="all"
            avgRetry = 6
            dataAvg = []
            removeSmallVal = 0.2
            vcc = 1.68
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
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out = ampers

        elif kind == "V":
            Vmultip = 195
            STDfilter = True
            STDchaver = 1
            accuracy = 5
            readRetray  = 5
            STDdirection="all"
            avgRetry = 4
            removeSmallVal = 0.2
            dataAvg = []
            vcc = 2.2
            vccAdjust = 0
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,vcc, vccAdjust)))
            volts = median(dataAvg)
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
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal,vcc, vccAdjust)))
            volts = mean(dataAvg)
            out = volts
        return out


   
    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            #try:
                start = dt.now()
                nr = int(arg[1][-2],10)
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]

                value = self.getValue(nr, addr, str(kind))
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                stop = dt.now()
                self._debug(1, "\tReading values from Analog device : {0} - time of exec {1}".format(arg[1],stop-start))
            #except:
             #   self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
             #   self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg))
             #   maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)

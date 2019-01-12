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
    def toVolts(self, data, Vmultip):
        vcc    = 2.29
        factor = vcc / 256.0
        out    = []
        for di in data:
            if di:
                volts = abs(((di * factor) - (vcc/2)) * Vmultip)
            else: volts = 0
            if volts > 0:
                out.append(volts)
    

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
    def dataAnalize(self,sensor, address, readRetray, Vmultip, STDfilter, STDchaver, STDdirection, accuracy ,removeSmallVal):
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
                    self._debug(1, "\tParameter STDchaver {0} is goood data len {1}".format(STDchaver, len(out)))
                else:
                    self._debug(1, "\tParameter STDchaver {0} is bad multiplaying   data len {1}".format(STDchaver, len(out)))
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
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy, removeSmallVal)))
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
            
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal)))
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
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, readRetray, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,removeSmallVal)))
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
            
            #    self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
             #   self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg))
             #   maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)

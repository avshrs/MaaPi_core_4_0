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
        out = []

        for di in data:
           if di < 254:
              volts = abs(((di * factor) - (vccAdjust)) * Vmultip)
              out.append(volts)
        return out



    @classmethod
    def readFromI2C(self,sensor, address, Vmultip, accuracy,vcc, vccAdjust):
        self.bus.write_byte(address,int(sensor))
        out = []
        data_out = []
        con0=0
        con255=0
        counter = 0
        while True:
            if counter > accuracy:
                break
            data = self.bus.read_i2c_block_data(address,int(sensor),32)[5:-2]
	    
            counter+=1
	    if data[10] > 0 and data[10] < 254 and data[20] > 0 and data[20] < 254:
                
	       data.sort(reverse=True)
               data_len = int(len(data)*0.2)
               leed_avg = mean(data[data_len:])

               for dto in data:
                  if dto >= leed_avg:
                     data_out.append(dto)
               out.append(self.toVolts(data_out,Vmultip,vcc, vccAdjust))
        return out
    @classmethod
    def dataAnalize(self,sensor, address, Vmultip, STDfilter, STDchaver, STDdirection, accuracy , vcc, vccAdjust):
        data_out = []
        data_tmp = []
        out = []
        data_readed = self.readFromI2C(sensor, address, Vmultip, accuracy, vcc, vccAdjust)
                                                                                                                                                                                              
        for dad_ in data_readed:
            data_tmp.append(max(dad_))
        data_tmp.sort(reverse=True)
                                                                                                                                                                                              
        data_len = int(len(data_tmp)*0.7)
        leed_avg = mean(data_tmp[data_len:])

        for dto in data_tmp:
            if dto >= leed_avg:
                data_out.append(dto)
                                                                                                                                                                                   
                                                                                                                                                                                             
        if STDfilter :
            avg = mean(data_out)
            std_ = stdev(data_out)
            std = std_ * STDchaver
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
            accuracy = 60
            STDdirection="all"
            vcc = 1.68
            vccAdjust = vcc/1.96225
            volts = max(self.dataAnalize(sensor, address, Vmultip, STDfilter,STDchaver, STDdirection, accuracy, vcc, vccAdjust))

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
            readRetray = 2
            STDdirection="all"
            avgRetry = 4
            removeSmallVal = 0.2
            vcc = 1.68
            vccAdjust = vcc/1.96225
            volts = max(self.dataAnalize(sensor, address, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust))
            if volts and volts != 0:
                ampers = volts / 0.0333333
            else:
                ampers = 0
            out = ampers
                                                                                                                                                                                              
        elif kind == "V":
            Vmultip   = 195
            STDfilter = True
            STDchaver = 1
            accuracy  = 40
            STDdirection = "all"
            avgRetry  = 1
            dataAvg   = []
            vcc       = 2.2
            vccAdjust = 0
#            dataAvg.append(max(self.dataAnalize(sensor, address, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust)))
            volts     = max(self.dataAnalize(sensor, address, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust))
            out       = volts
                                                                                                                                                                                              
        elif kind == "V" and sensor == 3:
            Vmultip = 1
            STDfilter = True
            STDchaver = 0.5
            accuracy = 2
            readRetray = 2
            STDdirection="all"
            avgRetry = 2
            removeSmallVal = 0.4
            dataAvg = []
            vcc = 1.68
            vccAdjust = vcc/2
            for i in range(0,avgRetry):
                dataAvg.append(max(self.dataAnalize(sensor, address, Vmultip, STDfilter,STDchaver, STDdirection, accuracy,vcc, vccAdjust)))
            volts = mean(dataAvg)
            out = volts
        return out                                 



    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
#            try:
                start = dt.now()
                nr = int(arg[1][-2],10)
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]
                value = self.getValue(nr, addr, str(kind))
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                stop = dt.now()
                self._debug(1, "\tReading values from Analog device : {0} - time of exec {1}".format(arg[1],stop-start))
		print stop - start
 #           except:
  #              self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
   #             self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg)) 
    #            maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)

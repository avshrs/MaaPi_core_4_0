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
            if data_ >= data_avg and data_ != 0:
                data_out.append(data_)

        return data_out
    
    @classmethod
    def filter_stdCh(self,data,ChauvenetC,STDdirection):
        out=[]
  
        if len(data)>2:
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
        else:
            out = [0,0]
        return out


    @classmethod
    def readFromI2C(self,sensor, address, accuracy):
        self.bus.write_byte(address,int(sensor))
        data = self.bus.read_i2c_block_data32(address,int(sensor),accuracy)
        return data

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
            Vmultip         = 1
            STDfilter       = True
            ChauvenetC      = 1
            avgToCut        =  0.2
            accuracy        = 30

            STDdirection    ="all"
            vcc             = 1.68
            vccAdjust       = vcc/1.96225
            toAmper         = False
            toAmperToWat    = True
        elif kind == "A" and address == 0x48:
            Vmultip      = 1
            STDfilter    = True
            ChauvenetC    = 1
            avgToCut     =  0.2
            accuracy     = 30
            STDdirection ="all"
            vcc          = 1.68
            vccAdjust    = vcc/1.96225
            toAmper = True
            toAmperToWat = False  
        elif kind == "V" and address == 0x4c and sensor !=1 and sensor != 3:
            Vmultip      = 255
            STDfilter    = True
            ChauvenetC   = 1
            avgToCut     =  0.2
            accuracy     = 30
            STDdirection = "all"
            vcc          = 1.68
            vccAdjust    = 0
            toAmper = False
            toAmperToWat = False       
        elif kind == "V" and address == 0x4c and sensor == 1 and sensor != 3:
            Vmultip      = 327
            STDfilter    = True
            ChauvenetC   = 1
            avgToCut     =  0.2
            accuracy     = 30
            STDdirection = "all"
            vcc          = 1.68
            vccAdjust    = 0
            toAmper = False
            toAmperToWat = False       
        elif kind == "V" and sensor == 3 and address == 0x4c:
            Vmultip      = 1.08
            STDfilter    = True
            ChauvenetC    = 1
            avgToCut     =  0.2
            accuracy     = 10
            STDdirection="all"
            vcc          = 3.3
            vccAdjust    = 0
            toAmper = False
            toAmperToWat = False

        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc, vccAdjust, toAmper, toAmperToWat, avgToCut
        

    @classmethod
    def getValue(self,sensor,address,kind):

        vMultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc, vccAdjust, toAmper, toAmperToWat, avgToCut = self.getSensorConf(sensor,address,kind)

        data_bin_readed = self.readFromI2C(sensor, address, accuracy)
        data_bin_temp =(self.filter_gtavg(data_bin_readed,avgToCut))
        data=(self.toVolts(data_bin_temp,vMultip,vcc,vccAdjust))
        if toAmper or toAmperToWat :
           data = self.toAmper(data)
        if toAmperToWat:
           data = self.toWat(data)

        return  mean(data)


    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
 #           try:
                start = dt.now() 
                nr = int(arg[1][-2],10)
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]
                value = self.getValue(nr, addr, str(kind))
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                stop = dt.now()
 #             self._debug(1, "\tReading values from Analog device : {0} - time of exec {1}".format(arg[1],stop-start))
                print stop - start
#            except:
 #               self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
#                self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg)) 
 #               maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)
#

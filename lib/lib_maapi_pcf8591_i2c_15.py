#!/usr/bin/python
import sys
from threading import Lock
import numpy as np
from scipy import signal
from statistics import median, stdev, mean
from datetime import datetime as dt
import lib.MaaPi_DB_connection as maapidb
from PythonSmbus2 import SMBus
from lib.PythonSmbus2 import SMBus
import time
import logging

logging.basicConfig(
    filename='/home/pi/MaaPi110/bin/logs/Maapi_Selector.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S')

class class_get_values(object):
    debug = 0
    
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            logging.debug("lib_maapi_pcf8591_i2c_15 \t- {0}".format(msg))

    bus = SMBus(1)

    @classmethod 
    def listIsZero(self,data): 
        for i in data: 
            if i > 0: 
                return True 
        return False

    @classmethod
    def toVolts(self, data, Vmultip,vcc, reference):
        factor = vcc / 256.0
        out = []
        for di in data:
            if di < 240:
                volts = (((abs(di-reference) * factor) ) * Vmultip)
                out.append(volts) 
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
    def readFromI2C(self,sensor, address, accuracy, loops):
        self.bus.write_byte(address,int(sensor))
        data = []
        for i in range(0,loops):
            data.append(self.bus.read_i2c_block_data32(address,int(sensor),accuracy))
        return data

    @classmethod
    def toAmper(self,data):
        out=[]
        div = 1/30.0
        for i in data:
            if i > 0.0:
                out.append(i/div)
            else:
                out.append(0)
        return out


    @classmethod
    def toWat(self,data):
        out=[]
        for i in data:
                out.append(i*233)
        return out
    

    @classmethod
    def getSensorConf(self,sensor,address,kind): 
        Vmultip = 1
        STDfilter = False
        ChauvenetC = 1
        avgToCut = 0.5
        accuracy = 30
        STDdirection ="no"
        vcc = 1.68
        vccAdjust = 0
        toAmper = False
        toAmperToWat    = False
        reference = 0
        sinf=True
        loops=1
        if kind == "W" and address == 0x48:
            STDfilter       = True
            accuracy        = 50
            STDdirection    ="all"
            reference       = 126.9
            toAmperToWat    = True
            sinf            = True
            loops           = 1
            vcc             = 3.27
	    
        elif kind == "V" and address == 0x48:
            Vmultip      = 12
            STDfilter    = True
            avgToCut     =  0.5
            accuracy     = 10
            vccAdjust    = vcc/2
            STDdirection = "all"

        elif kind == "A" and address == 0x48:
            toAmper = True

        elif kind == "V" and address == 0x4c and sensor != 0 :
            Vmultip      = 255
            STDfilter    = True
            accuracy     = 30
            STDdirection = "all"

        elif kind == "V" and sensor == 0 and address == 0x4c:
            Vmultip      = 130
            STDfilter    = True
            ChauvenetC   = 1 
            avgToCut     =  0.3
            accuracy     = 25
            STDdirection="all"
            vcc          = 3.27
           # reference       = 1
            sinf 	     = False

        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc,  toAmper, toAmperToWat, avgToCut, sinf, reference, loops


    @classmethod
    def sinFilter(self, data):
        value = np.array(data)
        out = []
        b, a = signal.butter(1, 0.05)
        out = signal.filtfilt(b, a, value)

        return out


    @classmethod
    def getValue(self,sensor,address,kind):
        vMultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc,  toAmper, toAmperToWat, avgToCut , sinf , reference, loops= self.getSensorConf(sensor,address,kind)
        out = []
        data_tmp =[]
        data = self.readFromI2C(sensor, address, accuracy,loops)
        for i in data:
            data_tmp=(self.toVolts(i, vMultip, vcc, reference))

            if STDfilter:
                data_tmp = self.filter_stdCh(data_tmp, ChauvenetC, STDdirection) 
            
            if sinf:
                data_tmp = self.sinFilter(data_tmp)

            if toAmper or toAmperToWat :
                data_tmp = self.toAmper(data_tmp)

            if toAmperToWat:
                data_tmp = self.toWat(data_tmp)
            out.append(max(data_tmp))
        return  mean(out)


    #read data from sensor
    @classmethod
    def __init__(self, *args):
	for arg in args:
 #           try:
                start = dt.now() 
                nr = int(arg[1][-2],10)
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]
                mutex = Lock()
                mutex.acquire()
                value = self.getValue(nr, addr, str(kind))             
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                stop = dt.now()
                self._debug(1, "\tReading values from Analog device : {0} - time of exec {1}".format(arg[1],stop-start))
#                print stop - start
#            except Exception as e:
#                self._debug(1, "\tERROR reading values from dev: {0}".format(e))
#                self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg)) 
#                maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)


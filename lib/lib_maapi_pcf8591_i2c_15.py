#!/usr/bin/python
import sys
from threading import Lock
import numpy as np
from scipy import signal
from statistics import median, stdev, mean
from datetime import datetime as dt
import lib.MaaPi_DB_connection as maapidb

from lib.lib_maapi_i2c_pi import I2C_MaaPi

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
            logging.debug("lib_maapi_pcf8591_i2c_15 \t- {0}".format(msg))

    bus = I2C_MaaPi(1)

    @classmethod 
    def listIsZero(self,data): 
        for i in data: 
            if i > 0: 
                return True 
        return False

    @classmethod
    def toVolts(self, data, Vmultip,vcc, reference, maxV, calibration):
        factor = vcc / 256.0
        out = []
        for di in data:
            if di < 250:
                m_volts = abs(di - reference) * factor
                if m_volts < maxV:
                    out.append(((m_volts) * Vmultip)-calibration) 

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
        #self.bus.write_byte(address,int(sensor))
        data = []
        for i in range(0,loops):
            data.append(self.bus.write_read_i2c_block_data32(address,int(sensor),int(sensor),accuracy))
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
        maxV = 240
        calibration = 0
        if kind == "W" and address == 0x48:
	    calibration	    = 0.01
            Vmultip         = 0.65
            STDfilter       = True
            accuracy        = 15
            ChauvenetC 	    = 1
            STDdirection    ="all"
            reference       = 126.9
            toAmperToWat    = True
            sinf            = False
            loops           = 4
            vcc             = 3.27
            maxV            = 1

        elif kind == "V" and address == 0x48: # 5v 
            Vmultip      = 2
            STDfilter    = True
            accuracy     = 10
            vcc          = 3.27 
            STDdirection = "all"

        elif kind == "V" and address == 0x4c and sensor == 3 :  # 3.3v 
            Vmultip      = 1
            STDfilter    = False
            accuracy     = 15
            vcc          = 3.27 
            STDdirection = "all"
            

        elif kind == "V" and sensor == 0 and address == 0x4c: #230v
            Vmultip      = 143.6
            loops        = 2
            accuracy     = 10
            vcc          = 3.27
            sinf 	     = False

        return  Vmultip, STDfilter,STDdirection, ChauvenetC, accuracy,  vcc,  toAmper, toAmperToWat, avgToCut, sinf, reference, loops, maxV, calibration


    @classmethod
    def sinFilter(self, data):
        value = np.array(data)
        out = []
        b, a = signal.butter(1, 0.05)
        out = signal.filtfilt(b, a, value)

        return out


    @classmethod
    def getValue(self,sensor,address,kind):
        vMultip, STDfilter, STDdirection, ChauvenetC, accuracy, vcc,  toAmper, toAmperToWat, avgToCut , sinf , reference, loops, maxV, calibration = self.getSensorConf(sensor,address,kind)
        out = []
#        data_tmp =[]
        data_ = self.readFromI2C(sensor, address, accuracy, loops)
        try:
            for data_tmp in data_: 
                if STDfilter:
                    data_tmp = self.filter_stdCh(data_tmp, ChauvenetC, STDdirection)

                data_tmp=(self.toVolts(data_tmp, vMultip, vcc, reference, maxV,calibration ))
                
                
                if sinf:
                    data_tmp = self.sinFilter(data_tmp)

                if toAmper or toAmperToWat :
                    data_tmp = self.toAmper(data_tmp)

                if toAmperToWat:
                    data_tmp = self.toWat(data_tmp)
                out.append(max(data_tmp))   
            
            out_ = min(out)
	
        except Exception as e:
            print e
            out_ = 0
		
        return  out_
    #read data from sensor
    @classmethod
    def __init__(self, *args):
	for arg in args:
            try:
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
                print stop - start
            except Exception as e:
		print e
                self._debug(1, "\tERROR reading values from dev: {0}".format(e))
                self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg)) 
                maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)


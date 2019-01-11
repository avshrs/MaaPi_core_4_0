#!/usr/bin/python

import sys
from statistics import median, stdev
from datetime import datetime
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
    def avg(self,data):
        data_ = 0
        for i in data: 
            data_+= i 
        return data_/(len(data))


    @classmethod
    def read(self,sensor, address):
        counter = 30
        self.bus.write_byte(address,0x04)
        out = []
        for ix in range(0,counter):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            if  data[12] > 0 and data[12] < 255:
                for da in data:
                    out.append(da)
        return out
    @classmethod
    def factorCalc(self,data,multip):
        vcc = 2.29
        factor = vcc / 256.0  # pfc factor
        data_=[]
        for di in data:
            idd = ((di * (factor)) - (vcc/2)) * multip
            data_.append(abs(idd))
        return data_

    @classmethod
    def convert(self,data,kind):
        out = 0
        if data:
            if kind == "W":
                volts  = max(self.factorCalc(data,1))
                ampers = volts / 0.0333333
                wats   = ampers * 235.0
                out = wats
            if kind == "V":
                volts  = max(self.factorCalc(data,205))
                ampers = 0
                wats   = 0
                out = volts
    
        return out


   
    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            try:
                nr = int(arg[1][-2],10)
                
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]
              
                data = self.read(nr, addr)

                value = self.convert(data,str(kind))
     
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                
            except:
                self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
		            maapidb.MaaPiDBConnection.insert_data(arg[0][0], 0," " , False)


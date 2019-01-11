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
        counter = 20
        accuracy = 200
        self.bus.write_byte(address,0x04)
        out = []
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)[5:]
            if  min(data) < 200 and max(data) > 1 and max(data) < 240:
                d = max(data)
                out.append(d)
                counter -= 1
                if counter < 1:
                    break
        return out

    @classmethod
    def convert(self,data,kind):
        factor = 2.29 / 256.0  # pfc factor
        out = 0
        print data
        if data:
            dataAvg = max(data)
            if kind == "W":
                volts  = (dataAvg * factor )
                ampers = volts / 0.0333333
                wats   = ampers * 235.0
                out = wats
            if kind == "V":
                 
                volts  = (dataAvg * factor )*190
                ampers = 0
                wats   = 0
                out = volts
        else:
            volts  = 0
            ampers = 0
            wats   = 0
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


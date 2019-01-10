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
    def read(self,sensor):
        counter = 20
        accuracy = 50
        self.bus.write_byte(0x48,0x04)
        out = []
        for ix in range(0,accuracy):
            data = self.bus.read_i2c_block_data(0x48,int(sensor),32)[5:]
            if  data[12] > 0 and data[13] > 0 and data[14] > 0:
                d = max(data)
#                if sensor !=0 :
#                    if d > 78:
#                        continue
                out.append(d)
                counter -= 1
                if counter < 1:
                    break
        return out

    @classmethod
    def convert(self,data,type_):
        factor = 2.29 / 256.0  # pfc factor
        if data:
            dataAvg = max(data)
            if type_ != 0:
                volts  = dataAvg * factor 
                ampers = volts / 0.0333333
                wats   = ampers * 235.0
                volts  = 0
            else: 
                volts  = (dataAvg * factor )*190
                ampers = 0
                wats   = 0
        else:
            volts  = 0
            ampers = 0
            wats   = 0
        return volts,ampers,wats


   
    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
          try:
                data = self.read(int(arg[1][-1:][0]))
                volt, amper, wat = self.convert(data,int(arg[1][-1:][0]))
                if int(arg[1][-1:]) > 0:
                    maapidb.MaaPiDBConnection.insert_data(arg[0],wat ," " , True)
                else:
                    
                    maapidb.MaaPiDBConnection.insert_data(arg[0],volt," " , True)
          except:
                self._debug(1, "\tERROR reading values from dev: {0}".format(arg[1]))
		errr=0
                maapidb.MaaPiDBConnection.insert_data(arg[0][0], errr," " , False)


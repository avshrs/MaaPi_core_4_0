#!/usr/bin/python

import sys
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
    def read(self,sensor):
        counter = 7
        accuracy = 70
        self.bus.write_byte(0x48,0x04)
        out = []
        for ix in range(0,accuracy):
            data = self.bus.read_i2c_block_data(0x48,int(sensor),32)[5:]
            if  data[1] > 1 and data[2] > 1:
                d = max(data)
                if sensor !=0 :
                    if d > 78:
                        continue
                out.append(d)
                counter -= 1
                if counter < 1:
                    break
            if len(out) < 1:
                out = [0]
        #print out   # print printprintprintprintprint
        return out
    @classmethod
    def avg(self,data):
        data_ = 0
        for i in data:
            data_+= i
        return data_/(len(data))
    @classmethod
    def convert(self,data,type_):
        factor = 2.29 / 256.0  # pfc factor
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
                maapidb.MaaPiDBConnection.insert_data(arg[0][0], 0," " , False)


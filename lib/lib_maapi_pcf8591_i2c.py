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
    dataCout = 0
    @classmethod
    def read(self,sensor, address):
        counter = 30
        accuracy = 30
        self.dataCout = counter * 32
        self.bus.write_byte(address,int(sensor))
        out = []
        for ix in range(0,accuracy):      
            data = self.bus.read_i2c_block_data(address,int(sensor),32)
            if  data[0] > 0 and data[0] < 254 and data[31] < 254 and data[31] > 0:
                for da in data:
                    out.append(da)
                counter -= 1
                if counter < 1:
                    break    
        return out

    @classmethod
    def factorCalc(self,data,multip,filter_,chaver):
        vcc = 2.29
        factor = vcc / 256.0  # pfc factor
        data_=[]
        svOut = []
        for di in data:
            idd = ((di * (factor)) - (vcc/2)) * multip
            if idd != 0:
                data_.append(abs(idd))
        data_.sort(reverse=True)
        if filter_:
            
            avg = mean(data_[:-20])
            std = stdev(data_[:-20])
            for sv in data_:
                if sv < avg + (std * chaver) and sv > avg - (std * chaver):
                    svOut.append(sv)
            return svOut
        else:
            return data_[:-20]

        

    @classmethod
    def convert(self,nr,addr,kind):
        allData = []
        range_  = 5
        out     = []
        for i in range (0,range_):
            allData.append(self.read(nr, addr))
        for data in allData:
            if data:
                if kind == "W":
                    volts  = max(self.factorCalc(data,1,True,2))
                    ampers = volts / 0.0333333
                    out.append(ampers * 234.0)

                if kind == "V":
                    out.append(max(self.factorCalc(data,205,False,1)))
                
                if kind == "A":
                    volts  = max(self.factorCalc(data,1,False,4))
                    out.append(volts / 0.0333333)
        return max(out)


   
    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
           # try:
                start = dt.now()
                nr = int(arg[1][-2],10)
                addr = int(arg[1][-7:-3],16)
                kind = arg[1][-1]
                
                value = self.convert(nr, addr, str(kind))
                maapidb.MaaPiDBConnection.insert_data(arg[0],value ," " , True)
                stop = dt.now()
                print stop-start
                self._debug(1, "\tReading values from Analog device : {0} - time of exec {1}".format(arg[1],stop-start))
          #  except:
           #     self._debug(1, "\tERROR reading values from dev: {0}".format(arg))
             #   self._debug(1, "\tERROR ------------------------------------------------------- {0}".format(arg))
            #    maapidb.MaaPiDBConnection.insert_data(arg[0],0, " " , False)

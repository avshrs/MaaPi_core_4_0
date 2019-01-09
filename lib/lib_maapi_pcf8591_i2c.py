#!/usr/bin/python

import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb
import smbus
import time


class class_get_values(object):
    debug = 0
    device = 0x48
    supplayVolts = 235
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    acc = 200
    sens=    [0,1,2,3]
    dataOut= [0,0,0,0]
    volts =  [0,0,0,0]
    ampers = [0,0,0,0]
    wats =   [0,0,0,0]

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BH1750 {0} {1}, {2}".format(level, datetime.now(),msg))

    @classmethod
    def convertToVolts(self, readings):
        vcc  = 2.22                                                                                                                                                           
        factor = (vcc)/256                                                                                                                                                     
        return (readings * factor) 

    @classmethod
    def convertToAmpers(self, volts):
        return volts * (1/30)

    @classmethod
    def convertToWats(self, ampers):
        return ampers * self.supplayVolts

    @classmethod
    def readFromBus(self, sens):
        self.bus.write_byte(0x48,sens)   
        time.sleep(0.001)
        return self.bus.read_byte(0x48)

    @classmethod
    def getData(self):
        for sa in range(0,self.acc):
            for ii in self.sens:
                ints = self.readFromBus(int(self.sens[ii]))
                volt = self.convertToVolts(ints)
                
                if volt > 0 or volt < 1.3 :
                    print volt
                    if self.dataOut[ii] < volt:
                        self.dataOut[ii] = volt
        for s in self.sens:
            self.volts[s]  = self.dataOut[s]
          
            self.ampers[s] = self.convertToAmpers(self.volts[s])
          
            self.wats[s]   = self.convertToWats(self.ampers[s])
          


    #read data from sensor
    @classmethod
    def __init__(self, *args):
        
        for arg in args:
            #try:
                self.getData()
                print self.wats[int(arg[1][-1:][0])]
                maapidb.MaaPiDBConnection.insert_data(arg[0][0], self.wats[int(arg[1][-1:][0])]," " , True)

            #except:
                self._debug(1, "\tERROR reading values from dev: {0}".format(arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0][0], 0," " , False)


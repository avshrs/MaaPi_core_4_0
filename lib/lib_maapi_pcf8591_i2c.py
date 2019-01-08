#!/usr/bin/python

import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb
import math
import smbus
import time


class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BH1750 {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        DEVICE = 0x48
        supplayVolts = 235
        bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
        accuracy = 1000 # 1 / 1000
        sens = [0,1,2,3]
        VoltsSqValues=[0,0,0,0]
        volts = [0,0,0,0]
        ampers = [0,0,0,0]
        wats = [0,0,0,0]
        
        def convertToVolts(readings):
            vcc  = 3.3                                                                                                                                                            
            vgnd = vcc/2                                                                                                                                                          
            factor = (vcc)/256                                                                                                                                                     
            return (readings * factor) - vgnd

        def convertToAmpers(volts_):
            return volts_ * (1/30)

        def convertToWats(ampers_):
            return ampers_ * supplayVolts
        
        def readFromBus(addr, sens):
            bus.write_byte(addr,int(sens))   
            return  bus.read_byte(addr)
        
        def getData():
            for i in range(0,accuracy):
                for i in sens:
                    Vreaded = convertToVolts(readFromBus(DEVICE,sens[i]))
                    VoltsSqValues[i]+= (Vreaded*Vreaded)
            
            
            for i in sens:
                volts[i] = math.sqrt(VoltsSqValues[i])
                ampers[i] = convertToAmpers(volts[i])
                wats[i] = convertToWats(ampers[i])





        for arg in args:
#           try:
#                getData()
		print "---------------------------------------------------------------------"
		print int(arg[1][-1:][0])
		print volts[int(arg[1][-1:][0])]
		print ampers[int(arg[1][-1:][0])]
		print wats[int(arg[1][-1:][0])]

                maapidb.MaaPiDBConnection.insert_data(arg[0], wats[int(arg[1][-1:][0])],arg[2] , True)
  #         except:
   #             self._debug(1, "\tERROR reading values from dev: {0}".format(arg[1]))
#		maapidb.MaaPiDBConnection.insert_data(arg[0], 0,arg[2] , False)


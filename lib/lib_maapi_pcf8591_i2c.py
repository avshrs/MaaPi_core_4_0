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
        device = 0x48
        supplayVolts = 235
        bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
        volt = 0
        accuracy = 100
        sens = [0,1,2,3]
        VoltsSqValues=[0,0,0,0]
        volts = [0,0,0,0]
        ampers = [0,0,0,0]
        wats = [0,0,0,0]
        
        def convertToVolts(readings):
            vcc  = 2.22                                                                                                                                                           
            factor = (vcc)/256                                                                                                                                                     
            return (readings * factor) 

        def convertToAmpers(volts_):
            return volts_ * (1/30)

        def convertToWats(ampers_):
            return ampers_ * supplayVolts
        
        def readFromBus(addr, sens):
            bus.write_byte(addr,sens)   
            time.sleep(0.002)
            data = bus.read_byte(addr)
            if data > 250:
                return  0
            else: 
                return data 
        
        def getData():
           for a in range(0,accuracy):
                for i in sens:
                    int_ = readFromBus(device,sens[i])
                    volt = convertToVolts(int_)
		    if volt > 0 or < 1.3:
              		volt*= (-1)
                    if volt < 1 :
                        VoltsSqValues[i] += (volt * volt)

           for s in sens:

                volts[s]  = math.sqrt(VoltsSqValues[s])

                ampers[s] = convertToAmpers(volts[s])

                wats[s]   = convertToWats(ampers[s])


        for arg in args:
#           try:
	      
              getData()
              
	      print wats[int(arg[1][-1:][0])]
              print wats[1]
              print wats[2]
              print wats[3]
#	      maapidb.MaaPiDBConnection.insert_data(arg[0], wats[int(arg[1][-1:][0])]," " , True)

 #          except:
              self._debug(1, "\tERROR reading values from dev: {0}".format(arg[1]))
 #             maapidb.MaaPiDBConnection.insert_data(arg[0], 0," " , False)


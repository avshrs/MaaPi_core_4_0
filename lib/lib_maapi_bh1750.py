#!/usr/bin/python

import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb

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
        DEVICE = 0x23  # Default device I2C address
        POWER_DOWN = 0x00  # No active state
        POWER_ON = 0x01  # Power on
        RESET = 0x07  # Reset data register value

        # Start measurement at 4lx resolution. Time typically 16ms.
        CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_LOW_RES_MODE = 0x23

        #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
        bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

        def convertToNumber(data):
            # Simple function to convert 2 bytes of data
            # into a decimal number
            return ((data[1] + (256 * data[0])) / 1.2)

        def readLight(addr=DEVICE):
            data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_2)
            return convertToNumber(data)

        for arg in args:
            try:
                maapidb.MaaPiDBConnection.insert_data(arg[0], readLight(),
                                                      arg[2], True)
            except:
                self._debug(1, "\tERROR reading values from dev: {0}".format(
                    arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)

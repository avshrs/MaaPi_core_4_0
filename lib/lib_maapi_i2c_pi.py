#i2c imports
import os
import sys
from fcntl import ioctl
from ctypes import c_uint32, c_uint8, c_uint16, c_char, POINTER, Structure, Array, Union, create_string_buffer
#---
from threading import Lock
from datetime import datetime as dt
import lib.MaaPi_DB_connection as maapidb
import logging

logging.basicConfig(
    filename='/home/pi/MaaPi110/bin/logs/Maapi_Selector.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S')

class I2C_MaaPi(object):
    debug = 0
    
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            logging.debug("lib_maapi_pcf8591_i2c_15 \t- {0}".format(msg))
 
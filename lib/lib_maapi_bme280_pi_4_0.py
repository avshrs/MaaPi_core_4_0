from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb

from lib.Adafruit_BME280 import *


class class_get_values(object):
    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BMP180 {0} {1}, {2}".format(level, datetime.now(), msg))

    #read data from sensor
    @classmethod
    def __init__(self,*args):
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()

        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)
        for arg in args:
            try:
                if arg[2] == "BME280_Temp_pi":
                    temp = float(sensor.read_temperature())
                    maapidb.MaaPiDBConnection.insert_data(arg[0],temp,arg[2],True)
                if arg[2] == "BME280_Pressure_pi":
                    pressure = float(sensor.read_pressure())
                    if pressure >= 95000 and pressure <= 110000:
                        maapidb.MaaPiDBConnection.insert_data(arg[0],pressure/100,arg[2],True)
                if arg[2] == "BME280_Humidity_pi":
                    temp = float(sensor.read_humidity())
                    maapidb.MaaPiDBConnection.insert_data(arg[0],temp,arg[2],True)


            except:
                self._debug(1,"\tERROR reading values from rom_id[1]: {0}".format(arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0],0,arg[2],False)

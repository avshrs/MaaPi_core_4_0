from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb
from lib.Adafruit_BME280 import *


class class_get_values(object):
    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BME280\t\t {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            try:
                if arg[2] == "BME280_Temperature_pi":
                    sensor = BME280(t_mode=BME280_OSAMPLE_8)
                    temp = sensor.read_temperature()
                    maapidb.MaaPiDBConnection.insert_data(
                        arg[0], temp, arg[2], True)
                    self._debug(1,"\Temperature = {0}".format(temp))
                if arg[2] == "BME280_Pressure_pi":
                    sensor2 = BME280(p_mode=BME280_OSAMPLE_8)
                    pressure = float(sensor2.read_pressure())
                    maapidb.MaaPiDBConnection.insert_data(
                        arg[0], pressure / 100, arg[2], True)
                    self._debug(1,"\Pressure = {0}".format(pressure))
                if arg[2] == "BME280_Humidity_pi":
                    sensor3 = BME280(h_mode=BME280_OSAMPLE_8)
                    hum = float(sensor3.read_humidity())
                    maapidb.MaaPiDBConnection.insert_data(
                        arg[0], hum, arg[2], True)
                    self._debug(1,"\Humidity = {0}".format(hum))

            except:
                self._debug(
                    1, "\tERROR reading values from rom_id[1]: {0}".format(
                        arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)

from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb
from lib.Adafruit_BME280 import *
from lib.lib_maapi_check import Check


class class_get_values(object):
    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BME280\t\t {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    @classmethod
    def read_values(self, name, s_id):
        try:
            if name == "BME280_Temperature_pi":
                sensor = BME280(p_mode=BME280_OSAMPLE_8)
                temp = float(sensor.read_temperature())
                maapidb.MaaPiDBConnection.insert_data(s_id, temp, name, True)
                self._debug(1,"Temperature = {0} ".format(temp))

            if name == "BME280_Pressure_pi":
                sensor2 = BME280(p_mode=BME280_OSAMPLE_8)
                pressure = float(sensor2.read_pressure())
                maapidb.MaaPiDBConnection.insert_data(s_id, pressure / 100, name, True)
                self._debug(1,"Pressure = {0} ".format(pressure))

            if name == "BME280_Humidity_pi":
                sensor3 = BME280(h_mode=BME280_OSAMPLE_8)
                hum = float(sensor3.read_humidity())
                maapidb.MaaPiDBConnection.insert_data(s_id, hum, name, True)
                self._debug(1,"Humidity = {0} ".format(hum))
        except:
            self._debug(1, "\tERROR reading values from: {0}".format(s_id))
            maapidb.MaaPiDBConnection.insert_data(s_id, 0, name, False)

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            condition, condition_min_max, force_value  = Check().condition(arg[0])
            self._debug(2,"condition is = {0}\t condition_min_max is = {1}, \t forced value is = {2}".format(condition, condition_min_max, force_value))
            if condition:
                if condition_min_max:
                    self.read_values(arg[2], arg[0])
                else:
                    maapidb.MaaPiDBConnection.insert_data(arg[0],force_value,arg[2],True)
                    self._debug(1,"forcing value for sensor id = {0} forced vslur is = {1} ".format(arg[0],force_value))
            else:
                self.read_values(arg[2], arg[0])

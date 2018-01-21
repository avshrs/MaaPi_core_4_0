from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb
from lib.Adafruit_BME280 import *


class class_get_values(object):
    debug = 1
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BMP180 {0} {1}, {2}".format(level, datetime.now(), msg))

    #read data from sensor
    @classmethod
    def __init__(self,*args):
        for arg in args:

                if arg[2] == "BME280_Temp_pi":
                    sensor = BME280(t_mode=BME280_OSAMPLE_8)
                    temp = sensor.read_temperature()
                    maapidb.MaaPiDBConnection.insert_data(arg[0],temp,arg[2],True)
                    print ("temp readed {0}".format(temp))
                if arg[2] == "BME280_Pressure_pi":
                    sensor2 = BME280(p_mode=BME280_OSAMPLE_8)
                    pressure = float(sensor2.read_pressure())
                    maapidb.MaaPiDBConnection.insert_data(arg[0],pressure/100,arg[2],True)
                    print ("pressure readed {0}".format(pressure))

                if arg[2] == "BME280_Humidity_pi":
                    sensor3 = BME280(h_mode=BME280_OSAMPLE_8)
                    hum = float(sensor3.read_humidity())
                    maapidb.MaaPiDBConnection.insert_data(arg[0],hum,arg[2],True)
                    print ("temp readed {0}".format(hum))


            

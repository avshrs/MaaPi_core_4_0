import Adafruit_BMP.BMP085 as BMP085
from datetime import datetime

import sys
import lib.MaaPi_DB_connection as maapidb


class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG BMP180 {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        # You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
        # BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
        # datasheet for more details on
        # he meanings of each mode (accuracy and power
        # consumption are primarily the differences).  The default mode is STANDARD.
        sensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)
        for arg in args:
            try:
                if arg[2] == "BMP180_Temp_pi":
                    temp = float(sensor.read_temperature())
                    maapidb.MaaPiDBConnection.insert_data(
                        arg[0], temp, arg[2], True)
                if arg[2] == "BMP180_Press_pi":
                    pressure = float(sensor.read_pressure())
                    if pressure >= 95000 and pressure <= 110000:
                        maapidb.MaaPiDBConnection.insert_data(
                            arg[0], pressure / 100, arg[2], True)
            except:
                self._debug(
                    1, "\tERROR reading values from rom_id[1]: {0}".format(
                        arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)

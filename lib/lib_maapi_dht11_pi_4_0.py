#!/usr/bin/python
import Adafruit_DHT
from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb


class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG dht11  {0} {1}, {2}".format(level, datetime.now(),
                                                     msg))

    #read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            try:
                device_gpio = maapidb.MaaPiDBConnection().table(
                    "devices").columns("dev_id", "dev_gpio_pin").filters_eq(
                        dev_id=31,
                        dev_rom_id="DHT11_1_1",
                    ).get()
                self._debug(1, "\tgpio: {0}".format(device_gpio))

                humidity, temp = Adafruit_DHT.read_retry(
                    11, device_gpio[arg[0]]["dev_gpio_pin"])
                self._debug(1, "\thum: {0}".format(humidity))
                self._debug(1, "\ttemp: {0}".format(temp))

                if arg[2] == "DHT11_Temp_pi":
                    if temp >= 90:
                        maapidb.MaaPiDBConnection.insert_data(
                            arg[0], 0, arg[2], False)
                        self._debug(1,
                                    "\terror hum >= 90: {0}".format(humidity))
                    else:
                        maapidb.MaaPiDBConnection.insert_data(
                            arg[0], temp, arg[2], True)
                        self._debug(1, "\thum updated: {0}".format(humidity))
                if arg[2] == "DHT11_Hum_pi":
                    if humidity <= 90:
                        maapidb.MaaPiDBConnection.insert_data(
                            arg[0], humidity, arg[2], True)
                        self._debug(1, "\ttemp updated: {0}".format(humidity))
                    else:
                        maapidb.MaaPiDBConnection.insert_data(
                            arg[0], 0, arg[2], False)
                        self._debug(1,
                                    "\terror hum >= 90: {0}".format(humidity))
            except:
                self._debug(
                    1, "\tERROR reading values from rom_id[1]: {0}".format(
                        arg[1]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)

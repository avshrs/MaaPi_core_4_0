#!/usr/bin/python
import smbus
from datetime import datetime, timedelta
import time
import psycopg2
import RPi.GPIO as GPIO
import sys
import lib.MaaPi_DB_connection as maapidb

# deprecated

"""
1. recive dev_id
2. get data from maapi_switch table
3. validate


"""


class class_set_values(object):
    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_GPI0 {0} {1}, {2}".format(level, datetime.now(), msg))
    @staticmethod
    def set_gpio_state(mp_table,slonv):
        pass

    @classmethod
    def __init__(self,*args):

    #    GPIO.setmode(GPIO.BCM)
    #    GPIO.setwarnings(False)

        mp_table = maapidb.MaaPiDBConnection().table("maapi_switch").columns('switch_update_rom_id',"*").filters_eq(switch_enabled=True).get()
        device_last_value = maapidb.MaaPiDBConnection().table("devices").columns('dev_id','dev_value').get()
        self._debug(3,"get mp_table ={0}".format(mp_table))
        for arg in args:

            if mp_table[arg[0]]["switch_data_from_sens_id"] and mp_table[arg[0]]["switch_update_rom_id"]:
                self._debug(1,"switch_data_from_sens_id and switch_update_rom_id  is TRUE")

                device_range_value = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_data_from_sens_id"],mp_table[arg[0]]["switch_range_acc"])
                self._debug(1,"get switch_range_acc = {0}".format(device_range_value))

                if mp_table[arg[0]]["switch_reference_sensor_min_e"] and mp_table[arg[0]]["switch_reference_sensor_min_id"]:
                    self._debug(1,"switch_reference_sensor_min_e and switch_reference_sensor_min_id is True".format(device_range_value))
                    device_range_value_ref_min = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_reference_sensor_min_id"],mp_table[arg[0]]["switch_range_acc"])
                    self._debug(1,"get device_range_value_ref_min = {0}".format(device_range_value_ref_min))
                    for i in range(mp_table[arg[0]]["switch_range_acc"]):
                        self._debug(1," ref ={0} < source {1} = {2}".format(device_range_value_ref_min[i] , device_range_value[i],device_range_value_ref_min[i] < device_range_value[i]))
                        if device_range_value_ref_min[i] < device_range_value[i]:
                            self._debug(1," device_range_value_ref_min[i] < device_range_value[i] = True".format())
                else:
                    pass
                if mp_table[arg[0]]["switch_reference_sensor_max_e"] and mp_table[arg[0]]["switch_reference_sensor_max_id"]:
                    pass
                else:
                    pass

if __name__ == "__main__":
    class_set_values()

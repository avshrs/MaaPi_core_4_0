#!/usr/bin/python
import smbus
from datetime import datetime, timedelta
import time
import psycopg2
import RPi.GPIO as GPIO
import sys
import lib.MaaPi_DB_connection as maapidb

# deprecated



class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(level, datetime.now(), msg))

    def set_gpio_state(mp_table,slonv):
        pass

    @classmethod
    def __init__(self,*args):

    #    GPIO.setmode(GPIO.BCM)
    #    GPIO.setwarnings(False)
        for arg in args:
            mp = maapidb.MaaPiDBConnection().table("maapi_switch").filters_eq(switch_enabled=True,switch_update_rom_id=arg[0],).get()
            print mp

            if mp['switch_range_acc']:  # if switch_range_acc is not None
                slnov = maapidb.MaaPiDBConnection().select_last_nr_of_values( mp[arg[0]]['switch_reference_sensor_id'],mp[arg[0]]['switch_range_acc']) #1 arg DEV ID, 2 arg RANGE IN MINUTES
            set_gpio_state(mp,slonv)

if __name__ == "__main__":
    class_get_values()

#!/usr/bin/python
import smbus
from datetime import datetime, timedelta
import time
import RPi.GPIO as GPIO
import sys
import lib.MaaPi_DB_connection as maapidb
from lib.lib_maapi_check import Check
import logging


class class_get_values(object):
    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            logging.debug("DEBUG OneWire_GPI0 {0} {1}, {2}".format(level, datetime.now(), msg))
            print ("DEBUG OneWire_GPI0 {0} {1}, {2}".format(level, datetime.now(), msg))

    @classmethod
    def min_max_checker(self, mp_table, sensID, min_max):
        val = 0
        counter = 0
        param = 0

        if mp_table[sensID]["switch_value_{0}_e".format(min_max)]:
            if mp_table[sensID]["switch_value_{0}_e".format(min_max)] and mp_table[sensID]["switch_reference_sensor_{0}_e".format(min_max)] and mp_table[sensID]["switch_reference_sensor_{0}_id".format(min_max)]:

                device_range_value_ref = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[sensID]["switch_reference_sensor_{0}_id".format(min_max)], mp_table[sensID]["switch_range_acc"])
                device_range_value = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[sensID]["switch_data_from_sens_id"], mp_table[sensID]["switch_range_acc"])
                self._debug(1, "Get history from sensor - dev_id={0} \tsamples={1}".format(mp_table[sensID]["switch_data_from_sens_id"],mp_table[sensID]["switch_range_acc"]))

                for i in range(0, mp_table[sensID]["switch_range_acc"]):
                    if device_range_value_ref[i] != 99999 and device_range_value[i] != 99999:

                        if min_max == "min":
                            if device_range_value[i] < device_range_value_ref[i] - mp_table[sensID]["switch_value_{0}".format(min_max)]:
                                self._debug(1, "{0} from {5} \t Value {1} is True ({2} < {3} - {4}) \t  ".format(i,min_max,device_range_value[i], device_range_value_ref[i], mp_table[sensID]["switch_value_{0}".format(min_max)],mp_table[sensID]["switch_range_acc"]))
                                counter+=1

                        if min_max == "max":
                            if device_range_value[i] > device_range_value_ref[i] + mp_table[sensID]["switch_value_{0}".format(min_max)]:
                                self._debug(1, "{0} from {5} \t Value {1} is True ({2} > {3} + {4}) \t  ".format(i,min_max,device_range_value[i], device_range_value_ref[i], mp_table[sensID]["switch_value_{0}".format(min_max)],mp_table[sensID]["switch_range_acc"]))
                                counter+=1

            else:
                for i in range(mp_table[sensID]["switch_range_acc"]):

                    if min_max == "min":
                        if device_range_value[i] < mp_table[sensID]["switch_value_{0}".format(min_max)]:
                            self._debug(1, "{0} from {5} \t Value {1} is True ({2} < {3} - {4}) \t  ".format(i,min_max,device_range_value[i], device_range_value_ref[i], mp_table[sensID]["switch_value_{0}".format(min_max)],mp_table[sensID]["switch_range_acc"]))
                            counter+=1

                    if min_max == "max":
                        if device_range_value[i] > mp_table[sensID]["switch_value_{0}".format(min_max)]:
                            self._debug(1, "{0} from {5} \t Value {1} is True ({2} > {3} + {4}) \t  ".format(i,min_max,device_range_value[i], device_range_value_ref[i], mp_table[sensID]["switch_value_{0}".format(min_max)],mp_table[sensID]["switch_range_acc"]))
                            counter+=1

        self._debug(1, "Finale Check - {0} from {1} is True for {2} value ".format(counter, mp_table[sensID]["switch_range_acc"], min_max, val))

        if mp_table[sensID]["switch_range_acc"] == counter:
            val = 1
        elif counter==0:
            val = 0
        else: val = 2

        self._debug(1, "Final Value for {0} is  = {1} ".format(min_max, val))
        return val


    @classmethod
    def invert_state(self, sensID,gpio_val,mp_table):
        if mp_table[sensID]["switch_invert"]:
            if gpio_val:
                gpio_finale = 0
            else:
                gpio_finale = 1
        else:
            gpio_finale = gpio_val
        return gpio_finale



    @classmethod
    def __init__(self, *args):
        logging.basicConfig(filename='lib_maapi_gpio.log',level=logging.DEBUG)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        mp_table = maapidb.MaaPiDBConnection().table("maapi_switch").columns('switch_update_rom_id', "*").filters_eq(switch_enabled=True).get()
        device_last_value = maapidb.MaaPiDBConnection().table("devices").columns('dev_id', 'dev_value', 'dev_gpio_pin').get()

        for arg in args:
            if mp_table[arg[0]]["switch_data_from_sens_id"] and mp_table[arg[0]]["switch_update_rom_id"]:
                value = 0
                value_min = self.min_max_checker(mp_table, arg[0], "min")
                self._debug(1, "Check min value - value is={0} \t if False max is not set".format(value_min))
                value_max = self.min_max_checker(mp_table, arg[0], "max")
                self._debug(1, "Check max value - value is={0} \t if False max is not set".format(value_max))

                if value_min == 1 or value_max == 1:
                    value = 1
                elif value_min == 2 or value_max == 2:
                    value = 2
                #update_val, value_forced = self.switch_on_at_sensor(mp_table, arg[0], device_last_value)
                condition, condition_min_max, force_value  = Check().condition(arg[0])

                if condition:
                    if condition_min_max:
                        gpio_finale = value
                        self._debug(1,"Condition min_max = {2}  \t Read value from sensor id = {0}, value is ={1}".format(rom_id[0],value, condition_min_max))
                    else:
                        maapidb.MaaPiDBConnection.insert_data(rom_id[0],force_value,' ',True)
                        self._debug(1,"Forcing value for sensor id = {0} \tforced vslur is = {1} ".format(rom_id[0],force_value))
                else:
                    value = self.read_data_from_1w(rom_id[1],rom_id[0])

                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)
                    self._debug(1,"Read value for sensor id = {0}   is = {1} ".format(rom_id[0],value))






                if  value > 0 and value != 2:
                    value = value_forced
                    gpio_finale = self.invert_state(arg[0], value, mp_table)
                else:
                    gpio_finale = value

                GPIO.setup(device_last_value[arg[0]]["dev_gpio_pin"], GPIO.OUT)

                gpio_finale = self.invert_state(arg[0], value, mp_table)

                if gpio_finale != 2:
                    if GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]):
                        if gpio_finale:
                            maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                        else:
                            GPIO.output(device_last_value[arg[0]]["dev_gpio_pin"], gpio_finale)
                            maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                    else:
                        if gpio_finale:
                            GPIO.output(device_last_value[arg[0]]["dev_gpio_pin"], gpio_finale)
                            maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                        else:
                            maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                else:
                    maapidb.MaaPiDBConnection.insert_data(arg[0], device_last_value[mp_table[arg[0]]["switch_update_rom_id"]]["dev_value"], "_", True)



if __name__ == "__main__":
    class_get_values()

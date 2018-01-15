#!/usr/bin/python
import smbus
from datetime import datetime, timedelta
import time
import psycopg2
import RPi.GPIO as GPIO
import sys
import lib.MaaPi_DB_connection as maapidb
import logging

class class_get_values(object):
    debug = 2

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            logging.debug("DEBUG OneWire_GPI0 {0} {1}, {2}".format(level, datetime.now(), msg))

    @staticmethod
    def set_gpio_state(mp_table, slonv):
        pass

    @classmethod
    def __init__(self, *args):
        logging.basicConfig(filename='lib_maapi_gpio.log',level=logging.DEBUG)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        mp_table = maapidb.MaaPiDBConnection().table("maapi_switch").columns(
            'switch_update_rom_id', "*").filters_eq(switch_enabled=True).get()
        device_last_value = maapidb.MaaPiDBConnection().table(
            "devices").columns('dev_id', 'dev_value', 'dev_gpio_pin').get()
        self._debug(3, "get device_last_value ={0}".format(device_last_value))
        for arg in args:

            if mp_table[arg[0]]["switch_data_from_sens_id"] and mp_table[arg[0]]["switch_update_rom_id"]:
                self._debug(1, "switch_data_from_sens_id and switch_update_rom_id  is TRUE")
                val_max = 1
                val_min = 1

                device_range_value = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_data_from_sens_id"], mp_table[arg[0]]["switch_range_acc"])
                self._debug(1, "get switch_range_acc = {0}".format(device_range_value))

                """ IF MINIMAL VALUE IS ON """
                if mp_table[arg[0]]["switch_value_min_e"]:

                    """ IF MINIMAL REFERENCE SENSOR IS ON AND ID EXIST """
                    if mp_table[arg[0]]["switch_reference_sensor_min_e"] and mp_table[arg[0]]["switch_reference_sensor_min_id"]:

                        self._debug(1, "switch_reference_sensor_min_e and switch_reference_sensor_min_id is True".format())
                        device_range_value_ref_min = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_reference_sensor_min_id"], mp_table[arg[0]]["switch_range_acc"])

                        for i in range(0, mp_table[arg[0]]["switch_range_acc"]):
                            if device_range_value_ref_min[i] is not 99999 and device_range_value[i] is not 99999:
                                if device_range_value[i] < device_range_value_ref_min[i] - mp_table[arg[0]]["switch_value_min"]:
                                    self._debug(2, "val_min  = 1")
                                else:
                                    val_min = 0
                                    self._debug(2, "val_min  = 0 ")

                        self._debug(1, "finally val_min  = {0} ".format(val_min))

                    else:

                        """ IF MINIMAL REFERENCE SENSOR IS OFF"""
                        self._debug( 1, "switch_reference_sensor_min_e and switch_reference_sensor_min_id is False".format())
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):
                            self._debug(2, "source {0} <  val {1} = {2}".format(
                                device_range_value[i],  mp_table[arg[0]]["switch_value_min"], device_range_value[i] < mp_table[arg[0]]["switch_value_min"]))
                            if device_range_value[i] < mp_table[arg[0]]["switch_value_min"]:
                                self._debug(2, "val_min  = 1")
                            else:
                                val_min = 0
                                self._debug(2, "val_min  = 0 ")
                        self._debug(
                            1, "finally val_min  = {0} ".format(val_min))

                """ IF MAXIMUM VALUE IS ON """
                if mp_table[arg[0]]["switch_value_max_e"]:
                    """ IF MAXIMUM REFERENCE SENSOR IS ON AND ID EXIST """
                    if mp_table[arg[0]]["switch_reference_sensor_max_e"] and mp_table[arg[0]]["switch_reference_sensor_max_id"]:

                        self._debug(
                            1, "switch_reference_sensor_max_e and switch_reference_sensor_max_id is True".format())
                        device_range_value_ref_max = maapidb.MaaPiDBConnection().select_last_nr_of_values(
                                                mp_table[arg[0]]["switch_reference_sensor_max_id"],
                                                mp_table[arg[0]]["switch_range_acc"])

                        self._debug(1, "get device_range_value_ref_max = {0}".format(
                            device_range_value_ref_max))
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):
                            if device_range_value_ref_max[i] is not 99999 and device_range_value[i] is not 99999:
                                self._debug(2, "source {0} > ref {1} + val {2} = {3}".format(
                                                device_range_value[i],
                                                device_range_value_ref_max[i],
                                                mp_table[arg[0]]["switch_value_max"],
                                                device_range_value[i] > device_range_value_ref_max[i] + mp_table[arg[0]]["switch_value_max"]))

                                if device_range_value[i] > device_range_value_ref_max[i] + mp_table[arg[0]]["switch_value_max"]:
                                    self._debug(2, "val_max  = 1")
                                else:
                                    val_max = 0
                                    self._debug(2, "val_max  = 0 ")
                        self._debug(
                            1, "finally val_max  = {0} ".format(val_max))
                    else:
                        """ IF MAXIMUM REFERENCE SENSOR IS OFF"""
                        self._debug(
                            1, "switch_reference_sensor_max_e and switch_reference_sensor_max_id is False".format())
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):

                            self._debug(2, "source {0} >  val {1} = {2}".format(
                                device_range_value[i],  mp_table[arg[0]]["switch_value_max"], device_range_value[i] > mp_table[arg[0]]["switch_value_max"]))
                            if device_range_value[i] > mp_table[arg[0]]["switch_value_max"]:
                                self._debug(2, "val_max  = 1")
                            else:
                                val_max = 0
                                self._debug(2, "val_max  = 0 ")
                        self._debug(
                            1, "finally val_max  = {0} ".format(val_max))







                if mp_table[arg[0]]["switch_turn_on_at_sensor_e"] and mp_table[arg[0]]["switch_turn_on_at_sensor_id"]:
                    self._debug(
                        1, "Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                    if mp_table[arg[0]]["switch_turn_on_at_sensor_value_min_e"] and mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"]:
                        self._debug(
                            1, "Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                        if device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"]:
                            self._debug(1, "switch_turn_on_at_sensor_e condition on min {0} < {1} is {2} put normal val_min {3}".format(
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],
                                            mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"],
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"],
                                            val_min))

                        else:
                            self._debug(1, "switch_turn_on_at_sensor_e condition on min {0} < {1} is {2} put forced val_min to {3}".format(
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],
                                            mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"],
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min"],
                                            mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]))
                            val_max = mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]
                            val_min = mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]

                    if mp_table[arg[0]]["switch_turn_on_at_sensor_value_max_e"] and mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"]:
                        self._debug(
                            1, "Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                        if device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"]:
                            self._debug(1, "switch_turn_on_at_sensor_e condition on max {0} > {1} is {2} put normal val_max {3}".format(
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],
                                            mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"],
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"],
                                            val_max))

                        else:
                            self._debug(1, "switch_turn_on_at_sensor_e condition on max {0} > {1} is {2} put forced val_max to {3}".format(
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],
                                            mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"],
                                            device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max"],
                                            mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]))

                            val_max = mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]
                            val_min = mp_table[arg[0]]["switch_turn_on_at_cond_not_val"]

                self._debug(1, "min = {0},  max ={1}".format(val_min, val_max))

                if val_min or val_max:
                    gpio_val = 1
                else:
                    gpio_val = 0

                if mp_table[arg[0]]["switch_invert"]:
                    if gpio_val:
                        gpio_finale = 0
                    else:
                        gpio_finale = 1
                    self._debug(1, "was inverted forom {0} to {1}".format(
                        gpio_val, gpio_finale))
                else:
                    self._debug(1, "none invert")
                    gpio_finale = gpio_val

                GPIO.setup(device_last_value[arg[0]]["dev_gpio_pin"], GPIO.OUT)

                self._debug(1, "GPIO.setup({0}, GPIO.OUT)".format(
                    device_last_value[arg[0]]['dev_gpio_pin']))


                if GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]) and gpio_finale:
                    self._debug(1, "GPIO ACTUAL STATE IS {0} NEW STATE IS = {1} DO NOT TOUCH GPIO PIN  ".format(
                                        GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]),
                                        gpio_finale))

                    maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                else:
                    self._debug(1, "GPIO ACTUAL STATE IS {0} NEW STATE IS = {1}".format(
                                        GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]),
                                        gpio_finale))

                    gpio_nr = device_last_value[arg[0]]["dev_gpio_pin"]
                    if gpio_finale:
                        GPIO.output(gpio_nr, gpio_finale)
                        self._debug(1, "GPIO state is {0}".format(GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"])))
                        maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                        self._debug(1, "GPIO {0} STATE UPDATED TO: {1}".format(device_last_value[arg[0]]["dev_gpio_pin"], gpio_finale))
                    else:

                        GPIO.output(gpio_nr, gpio_finale)
                        self._debug(1, "GPIO state is {0}".format(GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"])))
                        maapidb.MaaPiDBConnection.insert_data(arg[0], gpio_finale, "_", True)
                        self._debug(1, "GPIO {0} STATE UPDATED TO: {1}".format(device_last_value[arg[0]]["dev_gpio_pin"], gpio_finale))


if __name__ == "__main__":
    class_get_values()

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
    debug = 2

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_GPI0 {0} {1}, {2}".format(level, datetime.now(), msg))
    @staticmethod
    def set_gpio_state(mp_table,slonv):
        pass

    @classmethod
    def __init__(self,*args):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        mp_table = maapidb.MaaPiDBConnection().table("maapi_switch").columns('switch_update_rom_id',"*").filters_eq(switch_enabled=True).get()
        device_last_value = maapidb.MaaPiDBConnection().table("devices").columns('dev_id','dev_value','dev_gpio_pin').get()
        self._debug(3,"get device_last_value ={0}".format(device_last_value))
        for arg in args:

            if mp_table[arg[0]]["switch_data_from_sens_id"] and mp_table[arg[0]]["switch_update_rom_id"]:
                self._debug(1,"switch_data_from_sens_id and switch_update_rom_id  is TRUE")
                val_max=1
                val_min=1
                device_range_value = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_data_from_sens_id"],mp_table[arg[0]]["switch_range_acc"])
                self._debug(1,"get switch_range_acc = {0}".format(device_range_value))
                if mp_table[arg[0]]["switch_value_min_e"]:
                    if mp_table[arg[0]]["switch_reference_sensor_min_e"] and mp_table[arg[0]]["switch_reference_sensor_min_id"]:

                        self._debug(1,"switch_reference_sensor_min_e and switch_reference_sensor_min_id is True".format())
                        device_range_value_ref_min = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_reference_sensor_min_id"],mp_table[arg[0]]["switch_range_acc"])

                        self._debug(1,"get device_range_value_ref_min = {0}".format(device_range_value_ref_min))
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):

                            self._debug(2,"source {0} < ref {1} - val {2} = {3}".format(device_range_value[i] , device_range_value_ref_min[i] , mp_table[arg[0]]["switch_value_min"] ,device_range_value[i] < device_range_value_ref_min[i] - mp_table[arg[0]]["switch_value_min"] ))
                            if  device_range_value[i] < device_range_value_ref_min[i] - mp_table[arg[0]]["switch_value_min"] :
                                self._debug(2,"val_min  = 1")
                            else:
                                val_min=0
                                self._debug(2,"val_min  = 0 ")
                        self._debug(1,"finally val_min  = {0} ".format(val_min))
                    else:
                        self._debug(1,"switch_reference_sensor_min_e and switch_reference_sensor_min_id is False".format())
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):

                            self._debug(2,"source {0} <  val {1} = {2}".format(device_range_value[i] ,  mp_table[arg[0]]["switch_value_min"] ,device_range_value[i] <  mp_table[arg[0]]["switch_value_min"] ))
                            if  device_range_value[i] < mp_table[arg[0]]["switch_value_min"] :
                                self._debug(2,"val_min  = 1")
                            else:
                                val_min=0
                                self._debug(2,"val_min  = 0 ")
                        self._debug(1,"finally val_min  = {0} ".format(val_min))


                if mp_table[arg[0]]["switch_value_max_e"]:
                    if mp_table[arg[0]]["switch_reference_sensor_max_e"] and mp_table[arg[0]]["switch_reference_sensor_max_id"]:

                        self._debug(1,"switch_reference_sensor_max_e and switch_reference_sensor_max_id is True".format())
                        device_range_value_ref_max = maapidb.MaaPiDBConnection().select_last_nr_of_values(mp_table[arg[0]]["switch_reference_sensor_max_id"],mp_table[arg[0]]["switch_range_acc"])

                        self._debug(1,"get device_range_value_ref_max = {0}".format(device_range_value_ref_max))
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):

                            self._debug(2,"source {0} > ref {1} + val {2} = {3}".format(device_range_value[i] , device_range_value_ref_max[i] , mp_table[arg[0]]["switch_value_max"] ,device_range_value[i] > device_range_value_ref_max[i] + mp_table[arg[0]]["switch_value_max"] ))
                            if  device_range_value[i] > device_range_value_ref_max[i] + mp_table[arg[0]]["switch_value_max"] :
                                self._debug(2,"val_max  = 1")
                            else:
                                val_max=0
                                self._debug(2,"val_max  = 0 ")
                        self._debug(1,"finally val_max  = {0} ".format(val_max))
                    else:
                        self._debug(1,"switch_reference_sensor_max_e and switch_reference_sensor_max_id is False".format())
                        for i in range(mp_table[arg[0]]["switch_range_acc"]):

                            self._debug(2,"source {0} >  val {1} = {2}".format(device_range_value[i] ,  mp_table[arg[0]]["switch_value_max"] ,device_range_value[i] >  mp_table[arg[0]]["switch_value_max"] ))
                            if  device_range_value[i] > mp_table[arg[0]]["switch_value_max"] :
                                self._debug(2,"val_max  = 1")
                            else:
                                val_max=0
                                self._debug(2,"val_max  = 0 ")
                        self._debug(1,"finally val_max  = {0} ".format(val_max))

                gpio_val = lambda: 1 if val_min and val_max else 0

                GPIO.setup(device_last_value[arg[0]]["dev_gpio_pin"], GPIO.OUT)

                self._debug(1,"GPIO ACTUAL STATE IS {0} NEW STATE IS = {1} ".format(GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]),gpio_val()))

                if mp_table[arg[0]]["switch_invert"]:
                    self._debug(1,"invert is true".format(val_max))
                    v_min = val_min
                    v_max = val_max
                    val_min = lambda: 1 if val_min == 0 else 0
                    val_max = lambda: 1 if val_max == 0 else 0

                    self._debug(1,"was inverted min = {0} from {1} and max = {2} from {3} ".format(val_min(), v_min,val_max(),v_max))

                if mp_table[arg[0]]["switch_turn_on_at_sensor_e" ] and mp_table[arg[0]]["switch_turn_on_at_sensor_id" ]:
                    self._debug(1,"Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                    if mp_table[arg[0]]["switch_turn_on_at_sensor_value_min_e" ] and mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ]:
                        self._debug(1,"Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                        if device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ]:
                            self._debug(1,"switch_turn_on_at_sensor_e condition on min {0} < {1} is {2} put normal val_min {3}".format(device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ],device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ],val_min()))
                        else:
                            self._debug(1,"switch_turn_on_at_sensor_e condition on min {0} < {1} is {2} put forced val_min to {3}".format(device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ],device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] < mp_table[arg[0]]["switch_turn_on_at_sensor_value_min" ],mp_table[arg[0]]["switch_turn_on_at_cond_not_val" ]))
                            val_min = lambda  s: 1 if mp_table[arg[0]]["switch_turn_on_at_cond_not_val" ]  else 0

                    if mp_table[arg[0]]["switch_turn_on_at_sensor_value_max_e" ] and mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ]:
                        self._debug(1,"Table switch_turn_on_at_sensor_e and switch_turn_on_at_sensor_id is True".format())

                        if device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ]:
                            self._debug(1,"switch_turn_on_at_sensor_e condition on max {0} > {1} is {2} put normal val_max {3}".format(device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ],device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ],val_max()))
                        else:
                            self._debug(1,"switch_turn_on_at_sensor_e condition on max {0} > {1} is {2} put forced val_max to {3}".format(device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"],mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ],device_last_value[mp_table[arg[0]]["switch_turn_on_at_sensor_id"]]["dev_value"] > mp_table[arg[0]]["switch_turn_on_at_sensor_value_max" ],mp_table[arg[0]]["switch_turn_on_at_cond_not_val" ]))
                            val_max = lambda  s: 1 if mp_table[arg[0]]["switch_turn_on_at_cond_not_val" ]  else 0

                    if val_min == 0 and val_max ==0:
                        self._debug(1,"val_min and val_max is equal 0 ".format())
                        if GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]):
                            self._debug(1,"GPIO PIN IS {0}".format(device_last_value[arg[0]]["dev_gpio_pin"]))
                        else:
                            GPIO.output(device_last_value[arg[0]]["dev_gpio_pin"],0)
                            if GPIO.input(device_last_value[arg[0]]["dev_gpio_pin"]) is not True:
                                maapidb.MaaPiDBConnection.insert_data(arg[0],0,True)
                                self._debug(1,"GPIO {0} STATE UPDATED TO: {1}".format(device_last_value[arg[0]]["dev_gpio_pin"], 0))

                    elif Value_min == 1 or Value_max ==1:
                        GPIO.output(switch_gpio_nr,1)
                        qa("{0} - dev {1}      - or exec gpio - min or max == 1".format(datetime.now(),i))
                        if GPIO.input(switch_gpio_nr):
                            qa("{1} - dev {2}      - exec gpio - gpio state 1".format(GPIO.input(switch_gpio_nr),datetime.now(),i))
                            x.execute("SELECT dev_value FROM devices WHERE dev_id={0}".format(switch_update_id[i][0]))
                            dev_value_old = x.fetchone()[0]
                            x.execute("UPDATE devices SET dev_value={0}, dev_value_old={1}, dev_last_update=NOW(), dev_read_error='{2}'  WHERE dev_id='{3}'".format(1, dev_value_old,'ok' ,switch_update_id[i][0]))
                            conn.commit()
                            x.execute("SELECT dev_rom_id FROM devices WHERE dev_id='{0}' ".format(switch_update_id[i][0]))
                            dev_rom_id = x.fetchone()[0]
                            x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), switch_update_id[i][0],1))
                            conn.commit()


if __name__ == "__main__":
    class_set_values()

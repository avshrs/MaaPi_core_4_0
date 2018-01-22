#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.5
#                   Calculate Math Sentens
#
##############################################################
import sys
import unittest
from datetime import datetime
from MaaPi_Settings import *
from MaaPi_DB_connection import MaaPiDBConnection as MaaPiDBConnection_new
from MaaPi_DB_connection_2 import MaaPiDBConnection


class MaaPiExecMath_Verbose(object):
    def __init__(self, message):
        try:
            if sys.argv[1] == "-v":
                qa(message)
        except:
            pass


class MaaPiExecMath_exec(object):
    def run_math_expressions(self, math_id, force_e, force_v):
        qa = MaaPiExecMath_Verbose
        qa('run_math_expressions        -            running')
        qa("run")
        if self.device_table[int(self.math_table[math_id][
                "math_update_rom_id"])]["dev_type_id"] == self.maapi_math_id:
            qa("dupa")
            old_value = self.device_table[int(
                self.math_table[math_id]["math_update_rom_id"])]["dev_value"]

            if self.math_table[math_id]["math_data_from_1_id"] is not None:
                V1 = v1 = self.device_table[self.math_table[math_id][
                    "math_data_from_1_id"]]["dev_value"]
            else:
                V1 = v1 = 'none'

            if self.math_table[math_id]["math_data_from_2_id"] is not None:
                V2 = v2 = self.device_table[self.math_table[math_id][
                    "math_data_from_2_id"]]["dev_value"]
            else:
                V2 = v2 = 'none'

            if self.math_table[math_id]["math_data_from_3_id"] is not None:
                V3 = v3 = self.device_table[self.math_table[math_id][
                    "math_data_from_3_id"]]["dev_value"]
            else:
                V3 = v3 = 'none'

            if self.math_table[math_id]["math_data_from_4_id"] is not None:
                V4 = v4 = self.device_table[self.math_table[math_id][
                    "math_data_from_4_id"]]["dev_value"]
            else:
                V4 = v4 = 'none'

            if force_e: value = force_v
            else: value = eval(self.math_table[math_id]["math_math"])
            qa("insert")
            MaaPiDBConnection().insert_data(
                self.math_table[math_id]["math_update_rom_id"], value,
                self.device_type, True)
            qa("inserting data")

    def __init__(self):
        qa = MaaPiExecMath_Verbose
        #    self.db_con = MaaPiDBConnection
        """Name of device type"""
        self.device_type = 'PythonMath'

        self.maapi_math_id = 0
        """ GET MAAPI_MATH TABLE """

        self.math_table = MaaPiDBConnection_new().filters_eq(
            math_enabled="TRUE").order_by("id", "asc").get_table("maapi_math")
        """ GET MAAPI_DEVICE_LIST TABLE """

        maapi_device_list = MaaPiDBConnection_new().get_table(
            "maapi_device_list")
        """ GET DEVICES TABLE """
        self.device_table = MaaPiDBConnection_new().filters_eq(
            dev_status="TRUE").get_table("devices")

        for i in maapi_device_list:
            """ CHANGE TO PythonMath !!! """
            if maapi_device_list[i]["device_name"] == 'MathExpr':
                self.maapi_math_id = maapi_device_list[i]["id"]

        for math in self.math_table:
            enable = 0
            qa('\nmath reg {0}'.format(math))
            if self.math_table[math]["math_exec_if_cond_e"]:
                qa('exec if cond enabled {0}'.format(
                    self.math_table[math]["math_exec_if_cond_e"]))
                if self.math_table[math]["math_exec_cond_id"] is not None:
                    qa('sensor exist {0}'.format(
                        self.math_table[math]["math_exec_cond_id"]))
                    dev_value = self.device_table[self.math_table[math][
                        "math_exec_cond_id"]]["dev_value"]

                    if self.math_table[math]["math_exec_cond_value_min_e"]:
                        qa('math_exec_cond_value_min_e {0}'.format(
                            self.math_table[math][
                                "math_exec_cond_value_min_e"]))

                        if dev_value < self.math_table[math]["math_exec_cond_value_min"]:
                            qa('dev_value={0} < math_exec_cond_value_min={1}  = {2}'.
                               format(dev_value, self.math_table[math][
                                   "math_exec_cond_value_min"],
                                      dev_value < self.math_table[math]
                                      ["math_exec_cond_value_min"]))
                            enable = 1
                        else:
                            self.run_math_expressions(
                                math, self.math_table[math][
                                    "math_exec_cond_force_value_e"],
                                self.math_table[math][
                                    "math_exec_cond_force_value"])
                            qa('dev_value={0} < math_exec_cond_value_min={1}  = {2} -------------------------------force 0 on min--------------------------------'.
                               format(dev_value, self.math_table[math][
                                   "math_exec_cond_value_min"],
                                      dev_value < self.math_table[math]
                                      ["math_exec_cond_value_min"]))
                    if self.math_table[math]["math_exec_cond_value_max_e"]:
                        qa('math_exec_cond_value_max_e {0}'.format(
                            self.math_table[math][
                                "math_exec_cond_value_max_e"]))
                        if (dev_value > self.math_table[math]
                            ["math_exec_cond_value_max"]):
                            qa('dev_value={0} > math_exec_cond_value_max={1}  = {2}'.
                               format(dev_value, self.math_table[math][
                                   "math_exec_cond_value_max"],
                                      (dev_value > self.math_table[math]
                                       ["math_exec_cond_value_max"])))
                            enable = 1
                            qa('enable =1 ')
                        else:
                            self.run_math_expressions(
                                math, self.math_table[math][
                                    "math_exec_cond_force_value_e"],
                                self.math_table[math][
                                    "math_exec_cond_force_value"])
                            qa('dev_value={0} > math_exec_cond_value_max={1}  = {2} -------------------------------force 0 on max--------------------------------'.
                               format(dev_value, self.math_table[math][
                                   "math_exec_cond_value_max"],
                                      (dev_value > self.math_table[math]
                                       ["math_exec_cond_value_max"])))
                if enable == 1:
                    self.run_math_expressions(math, False, 0)
            else:
                self.run_math_expressions(math, False, 0)


try:
    if sys.argv[1] == "--help":
        qa("MaaPi Senosrs module : Cron Managment\n -v\t verbose")
    else:
        startTime = datetime.now()
        MaaPiExecMath_exec()
        endTime = datetime.now()
        delta = endTime - startTime
        time_s = delta.seconds
        time_ms = delta.microseconds
        d = float(time_ms) / 100000
        time = d + float(time_s)
        MaaPiDBConnection().update_cron(sys.argv[0], time)
except:
    startTime = datetime.now()
    MaaPiExecMath_exec()
    endTime = datetime.now()
    delta = endTime - startTime
    time_s = delta.seconds
    time_ms = delta.microseconds
    d = float(time_ms) / 100000
    time = d + float(time_s)
    MaaPiDBConnection().update_cron(sys.argv[0], time)

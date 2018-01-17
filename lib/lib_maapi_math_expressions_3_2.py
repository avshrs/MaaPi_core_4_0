#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.5
#                   Calculate Math Sentens
#
##############################################################
import sys
from datetime import datetime
import math
import lib.MaaPi_DB_connection as maapidb


class class_get_values(object):
    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(level, datetime.now(), msg))


    @classmethod
    def __init__(self,*args):
        maapi_devices = maapidb.MaaPiDBConnection().table("devices").columns('dev_id',
                                                                             'dev_rom_id',
                                                                             'dev_value',
                                                                             'dev_collect_values_if_cond_e',
                                                                             'dev_collect_values_if_cond_force_value_e',
                                                                             'dev_collect_values_if_cond_force_value',
                                                                             'dev_collect_values_if_cond_min_e',
                                                                             'dev_collect_values_if_cond_max_e',
                                                                             'dev_collect_values_if_cond_max',
                                                                             'dev_collect_values_if_cond_min',
                                                                             'dev_collect_values_if_cond_from_dev_e',
                                                                             'dev_collect_values_if_cond_from_dev_id',
                                                                             ).get()
        maapi_math = maapidb.MaaPiDBConnection().table("maapi_math").columns( 'id',
                                                                               'math_user_id',
                                                                               'math_name',
                                                                               'math_update_rom_id',
                                                                               'math_data_from_1_id',
                                                                               'math_data_from_2_id',
                                                                               'math_data_from_3_id',
                                                                               'math_data_from_4_id',
                                                                               'math_math',
                                                                               'math_descript',
                                                                               'math_enabled',
                                                                               ).get()
        for dev_id in args:
            print args
            for math in maapi_math:
                print maapi_math[math]['math_update_rom_id']
                if int(dev_id[0]) is int(maapi_math[math]['math_update_rom_id']):
                    print ("dupa")
                else:
                    print("podwjna dupa")


        #    if maapi_math[maapi_devices[dev_id[0]]['dev_id']]["math_data_from_1_id"]:
        #        V1 = v1 = self.device_table[self.math_table[math_id][
        #            "math_data_from_1_id"]]["dev_value"]
        #    else:
        #        V1 = v1 = 'none'

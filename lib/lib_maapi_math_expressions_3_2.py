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
    def get_values_and_count(self, math_id, maapi_math, maapi_devices):
        value = 0
        if maapi_math[math_id]['math_data_from_1_id']:
            V1 = v1 = maapi_devices[int(maapi_math[math_id]['math_data_from_1_id'])]['dev_value']
        else: V1 = v1 = 'none'

        if maapi_math[math_id]['math_data_from_2_id']:
            type( maapi_math[math_id]['math_data_from_2_id'])
            V2 = v2 = maapi_devices[int(maapi_math[math_id]['math_data_from_2_id'])]['dev_value']
        else: V2 = v2 = 'none'

        if maapi_math[math_id]['math_data_from_3_id']:
            V3 = v3 = maapi_devices[int(maapi_math[math_id]['math_data_from_3_id'])]['dev_value']
        else: V3 = v3 = 'none'

        if maapi_math[math_id]['math_data_from_4_id']:
            V4 = v4 = maapi_devices[int(maapi_math[math_id]['math_data_from_4_id'])]['dev_value']
        else: V4 = v4 = 'none'

        try:
            value = eval(maapi_math[math_id]["math_math"])
        except:
            maapidb.MaaPiDBConnection.insert_data(maapi_math[math_id]['math_update_rom_id'],0,' ',False)
        print value
        return value

    @classmethod
    def update_at_sensor(self, dev_id ,devices):
        if devices[dev_id]['dev_collect_values_if_cond_{0}_e'.format(min_max)]:
            self._debug(1,"collect values from sensor if condition - True \t {0} values on ".format(min_max))

            if devices[dev_id]['dev_collect_values_if_cond_from_dev_e'] and devices[dev_id]['dev_collect_values_if_cond_from_dev_id']:
                self._debug(1,"collect values from sensor if condition - True \t compare to other sensor")

                if min_max=="min":
                    if devices[devices[dev_id]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] < devices[dev_id]['dev_collect_values_if_cond_{0}'.format(min_max)]:

                        value = self.read_data_from_1w(rom_id[1],dev_id)

                        self._debug(1,"collect values from sensor if condition - True \t compared sensor < {1} value = true - puting readed value = {0}".format(value,min_max))

                    else:
                        if devices[dev_id]['dev_collect_values_if_cond_force_value_e']:
                            value = devices[dev_id]['dev_collect_values_if_cond_force_value']
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor < {1} value = false - puting forced value = {0}".format(devices[dev_id]['dev_collect_values_if_cond_force_value'],min_max))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor < {0} value = false - do nothing".format(min_max))

                if min_max == "max":
                    if devices[devices[dev_id]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] > devices[dev_id]['dev_collect_values_if_cond_{0}'.format(min_max)]:

                        value = self.read_data_from_1w(rom_id[1],dev_id)

                        self._debug(1,"collect values from sensor if condition - True \t compared sensor > {1} value = true - puting readed value = {0}".format(value,min_max))

                    else:
                        if devices[dev_id]['dev_collect_values_if_cond_force_value_e']:
                            value = devices[dev_id]['dev_collect_values_if_cond_force_value']
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor > {1} value = false - puting forced value = {0}".format(devices[dev_id]['dev_collect_values_if_cond_force_value'],min_max))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor > {0} value = false - do nothing".format(min_max))

            else:
                value = self.read_data_from_1w(rom_id[1],dev_id)
                if min_max == "min":
                    if value < devices[dev_id]['dev_collect_values_if_cond_{0}'.format(min_max)]:
                        self._debug(1,"collect values from sensor if condition - True \t readed sensor < {1} value = true - puting readed value = {0}".format(value,min_max))
                    else:
                        if devices[dev_id]['dev_collect_values_if_cond_force_value_e']:
                            value = devices[dev_id]['dev_collect_values_if_cond_force_value']
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor < {1} value = False - puting forced value = {0}".format(devices[dev_id]['dev_collect_values_if_cond_force_value'],min_max))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor < {0} value = False - do nothing".format(min_max))
                if min_max == "max":
                    if value > devices[dev_id]['dev_collect_values_if_cond_{0}'.format(min_max)]:
                        self._debug(1,"collect values from sensor if condition - True \t readed sensor > {1} value = true - puting readed value = {0}".format(value,min_max))
                    else:
                        if devices[dev_id]['dev_collect_values_if_cond_force_value_e']:
                            value = devices[dev_id]['dev_collect_values_if_cond_force_value']
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor > {1} value = False - puting forced value = {0}".format(devices[dev_id]['dev_collect_values_if_cond_force_value'],min_max))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor > {0} value = False - do nothing".format(min_max))
        return value




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
            for math_id in maapi_math:
                if int(dev_id[0]) == int(maapi_math[math_id]['math_update_rom_id']):
                    state_min = self.update_at_sensor( maapi_math[math_id]['math_update_rom_id'] , maapi_devices,"min")
                    state_max = self.update_at_sensor( maapi_math[math_id]['math_update_rom_id'] , maapi_devices,"max")
                    if state:
                        value = self.get_values_and_count(math_id, maapi_math, maapi_devices)
                        maapidb.MaaPiDBConnection.insert_data(maapi_math[math_id]['math_update_rom_id'],value,' ',True)

#!/usr/bin/python

import lib.MaaPi_DB_connection as maapidb

class Check(object):


    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(level, datetime.now(), msg))

    def __init__(self, dev_id, value):
        for i in range(2):
            if i == 0: min_max="min"
        elif i == 1: min_max="max"
            devices = maapidb.MaaPiDBConnection().table("devices").columns('dev_id', 'dev_rom_id','dev_value','dev_collect_values_if_cond_e','dev_collect_values_if_cond_force_value_e','dev_collect_values_if_cond_force_value','dev_collect_values_if_cond_min_e', 'dev_collect_values_if_cond_max_e', 'dev_collect_values_if_cond_max', 'dev_collect_values_if_cond_min', 'dev_collect_values_if_cond_from_dev_e', 'dev_collect_values_if_cond_from_dev_id', ).get()
            self._debug(1,"condition_check {0} ".format(min_max))

            if devices[rom_id[0]]['dev_collect_values_if_cond_{0}_e'.format(min_max)]:
                self._debug(1,"collect values from sensor if condition - True \t {0} values on ".format(min_max))

                if devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_e'] and devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_id']:
                    self._debug(1,"collect values from sensor if condition - True \t compare to other sensor")

                    if min_max=="min":
                        if devices[devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] < devices[rom_id[0]]['dev_collect_values_if_cond_{0}'.format(min_max)]:

                            value = self.read_data_from_1w(rom_id[1],rom_id[0])

                            self._debug(1,"collect values from sensor if condition - True \t compared sensor < {1} value = true - puting readed value = {0}".format(value,min_max))

                        else:
                            if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                                value = devices[rom_id[0]]['dev_collect_values_if_cond_force_value']
                                self._debug(1,"collect values from sensor if condition - True \t compared sensor < {1} value = false - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],min_max))
                            else:
                                self._debug(1,"collect values from sensor if condition - True \t compared sensor < {0} value = false - do nothing".format(min_max))

                    if min_max == "max":
                        if devices[devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] > devices[rom_id[0]]['dev_collect_values_if_cond_{0}'.format(min_max)]:

                            value = self.read_data_from_1w(rom_id[1],rom_id[0])

                            self._debug(1,"collect values from sensor if condition - True \t compared sensor > {1} value = true - puting readed value = {0}".format(value,min_max))

                        else:
                            if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                                value = devices[rom_id[0]]['dev_collect_values_if_cond_force_value']
                                self._debug(1,"collect values from sensor if condition - True \t compared sensor > {1} value = false - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],min_max))
                            else:
                                self._debug(1,"collect values from sensor if condition - True \t compared sensor > {0} value = false - do nothing".format(min_max))

                else:
                    value = self.read_data_from_1w(rom_id[1],rom_id[0])
                    if min_max == "min":
                        if value < devices[rom_id[0]]['dev_collect_values_if_cond_{0}'.format(min_max)]:
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor < {1} value = true - puting readed value = {0}".format(value,min_max))
                        else:
                            if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                                value = devices[rom_id[0]]['dev_collect_values_if_cond_force_value']
                                self._debug(1,"collect values from sensor if condition - True \t readed sensor < {1} value = False - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],min_max))
                            else:
                                self._debug(1,"collect values from sensor if condition - True \t readed sensor < {0} value = False - do nothing".format(min_max))
                    if min_max == "max":
                        if value > devices[rom_id[0]]['dev_collect_values_if_cond_{0}'.format(min_max)]:
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor > {1} value = true - puting readed value = {0}".format(value,min_max))
                        else:
                            if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                                value = devices[rom_id[0]]['dev_collect_values_if_cond_force_value']
                                self._debug(1,"collect values from sensor if condition - True \t readed sensor > {1} value = False - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],min_max))
                            else:
                                self._debug(1,"collect values from sensor if condition - True \t readed sensor > {0} value = False - do nothing".format(min_max))
            return value

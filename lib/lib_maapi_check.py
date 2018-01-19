#!/usr/bin/python

import   lib.MaaPi_DB_connection as maapidb

class Check(object):
    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(level, datetime.now(), msg))


    def run(self, dev_id):
        devices_db = maapidb.MaaPiDBConnection().table("devices").columns(
                                                                          "dev_id",
                                                                          "dev_value",
                                                                          "dev_rom_id",
                                                                          "dev_collect_values_if_cond_e",
                                                                          "dev_collect_values_if_cond_min_e",
                                                                          "dev_collect_values_if_cond_max_e",
                                                                          "dev_collect_values_if_cond_max",
                                                                          "dev_collect_values_if_cond_min",
                                                                          "dev_collect_values_if_cond_from_dev_e",
                                                                          "dev_collect_values_if_cond_from_dev_id",
                                                                          "dev_collect_values_if_cond_force_value_e",
                                                                          "dev_collect_values_if_cond_force_value",
                                                                          ).get()
        value_min=False
        value_max=False
        if devices_db[dev_id]['dev_collect_values_if_cond_e']:
            if devices_db[dev_id]['dev_collect_values_if_cond_from_dev_e'] and devices_db[dev_id]['dev_collect_values_if_cond_from_dev_id']:

                if devices_db[dev_id]['dev_collect_values_if_cond_min_e'] and devices_db[dev_id]['dev_collect_values_if_cond_min']:
                    if devices_db[devices_db[dev_id]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] < devices_db[dev_id]['dev_collect_values_if_cond_min']:
                        value_min = True
                    else:
                        value_min = False
                else:
                    value_min = False

                if devices_db[dev_id]['dev_collect_values_if_cond_max_e'] and devices_db[dev_id]['dev_collect_values_if_cond_max']:
                    if devices_db[devices_db[dev_id]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] > devices_db[dev_id]['dev_collect_values_if_cond_max']:
                        value_max = True
                    else:
                        value_max = False
                else:
                    value_max = False
            else:

                if devices_db[dev_id]['dev_collect_values_if_cond_min_e'] and devices_db[dev_id]['dev_collect_values_if_cond_min']:
                    if devices_db[dev_id]['dev_value'] <= devices_db[dev_id]['dev_collect_values_if_cond_min']:
                        value_min = True
                    else:
                        value_min = False
                else:
                    value_min = False

                if devices_db[dev_id]['dev_collect_values_if_cond_max_e'] and devices_db[dev_id]['dev_collect_values_if_cond_max']:
                    if devices_db[dev_id]['dev_value'] >= devices_db[dev_id]['dev_collect_values_if_cond_max']:
                        value_max = True
                    else:
                        value_max = False
                else:
                    value_max = False
        value = False
        if value_max == False or value_min != False:
            value = False
        else:
            value = True
        return value

    

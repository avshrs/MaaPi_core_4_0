#!/usr/bin/python
import lib.MaaPi_DB_connection as maapidb

class Check(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(
                level, datetime.now(), msg))

    def condition(self, dev_id):
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
        condition_min = False
        condition_max = False
        condition = False
        condition_min_max = False
        force = False
        #print (devices_db)
        if devices_db[dev_id]['dev_collect_values_if_cond_e']:
            condition = devices_db[dev_id]['dev_collect_values_if_cond_e']
            if devices_db[dev_id]['dev_collect_values_if_cond_from_dev_e'] and devices_db[dev_id]['dev_collect_values_if_cond_from_dev_id']:

                if devices_db[dev_id]['dev_collect_values_if_cond_min_e'] and devices_db[dev_id]['dev_collect_values_if_cond_min']:
                    if devices_db[devices_db[dev_id]
                                  ['dev_collect_values_if_cond_from_dev_id']]['dev_value'] < devices_db[dev_id]['dev_collect_values_if_cond_min']:
                        condition_min = True
                    else:
                        condition_min = False
                else:
                    condition_min = False

                if devices_db[dev_id]['dev_collect_values_if_cond_max_e'] and devices_db[dev_id]['dev_collect_values_if_cond_max']:
                    if devices_db[devices_db[dev_id]
                                  ['dev_collect_values_if_cond_from_dev_id']]['dev_value'] > devices_db[dev_id]['dev_collect_values_if_cond_max']:
                        condition_max = True
                    else:
                        condition_max = False
                else:
                    condition_max = False
            else:

                if devices_db[dev_id]['dev_collect_values_if_cond_min_e'] and devices_db[dev_id]['dev_collect_values_if_cond_min']:
                    if devices_db[dev_id]['dev_value'] <= devices_db[dev_id]['dev_collect_values_if_cond_min']:
                        condition_min = True
                    else:
                        condition_min = False
                else:
                    condition_min = False

                if devices_db[dev_id]['dev_collect_values_if_cond_max_e'] and devices_db[dev_id]['dev_collect_values_if_cond_max']:
                    if devices_db[dev_id]['dev_value'] >= devices_db[dev_id]['dev_collect_values_if_cond_max']:
                        condition_max = True
                    else:
                        condition_max = False
                else:
                    condition_max = False

            if condition_max == False or condition_min != False:
                condition_min_max = False
            else:
                condition_min_max = True
            if condition_min_max == False:
                if devices_db[dev_id]['dev_collect_values_if_cond_force_value_e']:
                    force = devices_db[dev_id]['dev_collect_values_if_cond_force_value']
                    
        return condition,condition_min_max, force

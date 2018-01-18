#!/usr/bin/python
import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb


class class_get_values(object):
    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(level, datetime.now(), msg))


    @classmethod
    def switch_on_at_sensor(self,mp_table, sensID, device_last_value):
        state_return = 0
        val = False
        if mp_table[sensID]["switch_turn_on_at_sensor_e"] and mp_table[sensID]["switch_turn_on_at_sensor_id"]:
            if mp_table[sensID]["switch_turn_on_at_sensor_value_min_e"]:
                if device_last_value[mp_table[sensID]["switch_turn_on_at_sensor_id"]]["dev_value"] <= mp_table[sensID]["switch_turn_on_at_sensor_value_min"]:
                    state_return = False
                else:
                    val = mp_table[sensID]["switch_turn_on_at_cond_not_val"]
                    state_return = True

            if mp_table[sensID]["switch_turn_on_at_sensor_value_max_e"] and mp_table[sensID]["switch_turn_on_at_sensor_value_max"]:

                if device_last_value[mp_table[sensID]["switch_turn_on_at_sensor_id"]]["dev_value"] >= mp_table[sensID]["switch_turn_on_at_sensor_value_max"]:
                    state_return = False
                else:
                    val = mp_table[sensID]["switch_turn_on_at_cond_not_val"]
                    state_return = True

        return state_return, val

    @classmethod
    def read_data_from_1w(self,rom_id,dev_id):
        try:
            w1_file = open('/sys/bus/w1/devices/{0}/w1_slave'.format(rom_id), 'r')
            self._debug(2,"open file /sys/bus/w1/devices/{0}/w1_slave".format(rom_id))
            w1_line = w1_file.readline()
            w1_crc = w1_line.rsplit(' ',1)
            w1_crc = w1_crc[1].replace('\n', '')

            if w1_crc=='YES':
                self._debug(2,"CRC - YES")
                w1_line = w1_file.readline()
                w1_temp = w1_line.rsplit('t=',1)
                temp = float(float(w1_temp[1])/float(1000))
                self._debug(1,"read_data_from_1w - Value is {0} for rom_id[1] {1}".format(temp,dev_id))
                w1_file.close()
                self._debug(2,"Close file")
            else:
                w1_file.close()
                self._debug(2,"CRC False")
                maapidb.MaaPiDBConnection.insert_data(dev_id,99999,' ',False)

        except:
            self._debug(2,"\tERROR reading values from rom_id[1]: {0}".format(dev_id))
            maapidb.MaaPiDBConnection.insert_data(dev_id,99999,' ',False)
        return temp

    @classmethod
    def condition_check(self, rom_id, devices, min_max):
        self._debug(1,"condition_check {0} ".format(min_max))
        value =99992
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

    @classmethod
    def __init__(self,*args):

        devices = maapidb.MaaPiDBConnection().table("devices").columns('dev_id', 'dev_rom_id','dev_value', 'dev_gpio_pin','dev_collect_values_if_cond_e','dev_collect_values_if_cond_force_value_e','dev_collect_values_if_cond_force_value','dev_collect_values_if_cond_min_e', 'dev_collect_values_if_cond_max_e', 'dev_collect_values_if_cond_max', 'dev_collect_values_if_cond_min', 'dev_collect_values_if_cond_from_dev_e', 'dev_collect_values_if_cond_from_dev_id', ).get()
        for rom_id in args:
            #print "ROM ID = {0}".format(rom_id)
            if devices[rom_id[0]]['dev_collect_values_if_cond_e']:
                value_min = self.condition_check(rom_id, devices, "min")
                self._debug(1,"value_min = {0}".format(value_min))

                if value_min != 99992:
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],value_min,' ',True)
                else:
                    value_max = self.condition_check(rom_id, devices, "max")
                    self._debug(1,"value_max = {0}".format(value_max))
                    if value_max != 99992:
                        maapidb.MaaPiDBConnection.insert_data(rom_id[0],value_max,' ',True)

            else:
                value = self.read_data_from_1w(rom_id[1],rom_id[0])
                #print "ROM ID = {0} - values updated".format(rom_id)
                maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)

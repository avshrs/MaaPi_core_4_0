#!/usr/bin/python
import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb


class class_get_values(object):
    debug = 1
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


    classmethod
    def condition_check(self, rom_id, devices):
            self._debug(1,"collect values from sensor if condition - True")

            if devices[rom_id[0]]['dev_collect_values_if_cond_min_e']:
                self._debug(1,"collect values from sensor if condition - True \t min values on ")

                if devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_e']:
                    self._debug(1,"collect values from sensor if condition - True \t compare to other sensor")

                    if devices[devices[rom_id[0]]['dev_collect_values_if_cond_from_dev_id']]['dev_value'] < devices[rom_id[0]]['dev_collect_values_if_cond_min']:

                        value = self.read_data_from_1w(rom_id[1],rom_id[0])
                        maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)
                        self._debug(1,"collect values from sensor if condition - True \t compared sensor < min value = true - puting readed value = {0}".format(value))

                    else:
                        if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                            maapidb.MaaPiDBConnection.insert_data(rom_id[0],devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],' ',True)
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor < min value = true - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value']))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t compared sensor < min value = true - do nothing")
                else:
                    value = self.read_data_from_1w(rom_id[1],rom_id[0])
                    if value < devices[rom_id[0]]['dev_collect_values_if_cond_min']:
                        maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)
                        self._debug(1,"collect values from sensor if condition - True \t readed sensor < min value = true - puting readed value = {0}".format(value))
                    else:
                        if devices[rom_id[0]]['dev_collect_values_if_cond_force_value_e']:
                            maapidb.MaaPiDBConnection.insert_data(rom_id[0],devices[rom_id[0]]['dev_collect_values_if_cond_force_value'],' ',True)
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor < min value = true - puting forced value = {0}".format(devices[rom_id[0]]['dev_collect_values_if_cond_force_value']))
                        else:
                            self._debug(1,"collect values from sensor if condition - True \t readed sensor < min value = true - do nothing")


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
                self._debug(2,"Value is {0} for rom_id[1] {1}".format(temp,dev_id))
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
    def __init__(self,*args):
        devices = maapidb.MaaPiDBConnection().table("devices").columns('dev_id', 'dev_rom_id','dev_value', 'dev_gpio_pin','dev_collect_values_if_cond_e','dev_collect_values_if_cond_force_value_e','dev_collect_values_if_cond_force_value','dev_collect_values_if_cond_min_e', 'dev_collect_values_if_cond_max_e', 'dev_collect_values_if_cond_max', 'dev_collect_values_if_cond_min', 'dev_collect_values_if_cond_from_dev_e', 'dev_collect_values_if_cond_from_dev_id', ).get()
        for rom_id in args:
            value=0
            print args
            if devices[rom_id[0]]['dev_collect_values_if_cond_e']:
                value_min = condition_check(self, rom_id, devices,"min"):
                value_max = condition_check(self, rom_id, devices,"max"):
            else:
                value = self.read_data_from_1w(rom_id[1],rom_id[0])
                self._debug(1,"collect values from sensor if condition - False")
                maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)

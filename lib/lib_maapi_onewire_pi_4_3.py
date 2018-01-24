#!/usr/bin/python
import sys
from datetime import datetime
import lib.MaaPi_DB_connection as maapidb
from lib.lib_maapi_check import Check


class class_get_values(object):
    debug = 1
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire\t\t {0} {1}, {2}".format(level, datetime.now(), msg))

    @classmethod
    def read_data_from_1w(self,rom_id,dev_id):
        try:
            w1_file = open('/sys/bus/w1/devices/{0}/w1_slave'.format(rom_id), 'r')
            self._debug(2,"Open file /sys/bus/w1/devices/{0}/w1_slave".format(rom_id))
            w1_line = w1_file.readline()
            w1_crc = w1_line.rsplit(' ',1)
            w1_crc = w1_crc[1].replace('\n', '')
            if w1_crc=='YES':
                self._debug(2,"CRC - YES")
                w1_line = w1_file.readline()
                w1_temp = w1_line.rsplit('t=',1)
                temp = float(float(w1_temp[1])/float(1000))
                self._debug(2,"Read_data_from_1w - Value is {0} for rom_id[1] {1}".format(temp,dev_id))
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
        for rom_id in args:
            condition, condition_min_max, force_value  = Check().condition(rom_id[0])
            self._debug(2,"Condition is = {0}\t condition_min_max is = {1}, \t forced value is = {2}".format(condition, condition_min_max, force_value))
            if condition:
                if condition_min_max:
                    value = self.read_data_from_1w(rom_id[1],rom_id[0])
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)
                    self._debug(1,"Condition min_max = {2}  \t Read value from sensor id = {0}, value is ={1}".format(rom_id[0],value, condition_min_max))
                else:
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],force_value,' ',True)
                    self._debug(1,"Forcing value for sensor id = {0} \tforced vslur is = {1} ".format(rom_id[0],force_value))
            else:
                value = self.read_data_from_1w(rom_id[1],rom_id[0])

                maapidb.MaaPiDBConnection.insert_data(rom_id[0],value,' ',True)
                self._debug(1,"Read value for sensor id = {0}   is = {1} ".format(rom_id[0],value))

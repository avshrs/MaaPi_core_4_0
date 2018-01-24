
from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb
from lib.lib_maapi_check import Check
import commands


class class_get_values(object):
    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG linux cmd\t\t {0} {1}, {2}".format(
                level, datetime.now(), msg))


    @classmethod
    def get_value(self, arg):
        try:
            self._debug(2, "Cmd_update_rom_id: {0}".format(arg[0]))
            maapi_commandline = maapidb.MaaPiDBConnection().table(
                "maapi_commandline").columns('cmd_update_rom_id', 'cmd_command').get()
            self._debug(2, "\t Command line:: {0}".format(
                maapi_commandline))
            self._debug(2, "\t Command line:: {0}".format(
                maapi_commandline[str(arg[0])]['cmd_command']))
            value = commands.getstatusoutput('{0}'.format(
                maapi_commandline[str(arg[0])]['cmd_command']))
            self._debug(2, "\t Command value:: {0}".format(value[1]))
            maapidb.MaaPiDBConnection.insert_data(
                arg[0], float(value[1]), arg[2], True)
            return float(value[1])
        except:
            self._debug(
                1, "\tERROR reading values from id: {0}".format(arg[0]))
            maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)



    # read data from sensor
    @classmethod
    def __init__(self, *args):
        for dev_id in args:
            condition, condition_min_max, force_value  = Check().condition(dev_id[0])
            self._debug(2,"Condition is = {0}\t condition_min_max is = {1}, \t forced value is = {2}".format(condition, condition_min_max, force_value))
            if condition:
                if condition_min_max:
                    value = self.get_value(dev_id)
                    self._debug(1,"Condition min_max = {2}  \t Read value from sensor id = {0}, value is ={1}".format(dev_id[0],value, condition_min_max))
                else:
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],force_value,' ',True)
                    self._debug(1,"Forcing value for sensor id = {0} \t forced vslur is = {1} ".format(dev_id[0],force_value))
            else:
                value = self.get_value(dev_id)
                self._debug(1,"Readed value for sensor id = {0}  is {1} ".format(dev_id[0], value))

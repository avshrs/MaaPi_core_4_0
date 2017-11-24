
from datetime import datetime
import sys
import lib.MaaPi_DB_connection as maapidb


import commands


class class_get_values(object):
    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG linux cmd {0} {1}, {2}".format(
                level, datetime.now(), msg))

    # read data from sensor
    @classmethod
    def __init__(self, *args):
        for arg in args:
            try:
                self._debug(1, "\cmd_update_rom_id: {0}".format(arg[0]))
                maapi_commandline = maapidb.MaaPiDBConnection().table(
                    "maapi_commandline").columns('cmd_update_rom_id', 'cmd_command').get()
                self._debug(3, "\t command line:: {0}".format(
                    maapi_commandline))
                self._debug(1, "\t command line:: {0}".format(
                    maapi_commandline[str(arg[0])]['cmd_command']))
                value = commands.getstatusoutput('{0}'.format(
                    maapi_commandline[str(arg[0])]['cmd_command']))
                self._debug(1, "\t command value:: {0}".format(value[1]))
                maapidb.MaaPiDBConnection.insert_data(
                    arg[0], float(value[1]), arg[2], True)
            except:
                self._debug(
                    1, "\tERROR reading values from id: {0}".format(arg[0]))
                maapidb.MaaPiDBConnection.insert_data(arg[0], 0, arg[2], False)

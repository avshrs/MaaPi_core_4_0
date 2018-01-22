#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 4.0
#                 reindex tabels with data
#
##############################################################

import lib.MaaPi_DB_connection as maapidb
from datetime import datetime


class class_get_values(object):

    debug = 1

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG OneWire_PI0 {0} {1}, {2}".format(
                level, datetime.now(), msg))

    #read data from sensor
    @classmethod
    def __init__(self):
        data_devices = maapidb.MaaPiDBConnection().table("devices").columns(
            "dev_id",
            "dev_rom_id",
        ).order_by('dev_id').filters_eq(
            dev_status=True, ).get()
        maapidb.MaaPiDBConnection().reindex(data_devices)


if __name__ == "__main__":
    class_get_values()

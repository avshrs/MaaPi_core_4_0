#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date
import sys
import lib.MaaPi_DB_connection as maapidb

from astral import *

"""

0 = New moon
7 = First quarter
14 = Full moon
21 = Last quarter

"""

class class_get_values(object):

    debug = 0

    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG MoonPhase\t\t  {0} {1}, {2}".format(level, datetime.now(), msg))

    #read data from sensor
    @classmethod
    def __init__(self,*args):
        for rom_id in args:
            try:
                a = Astral()
                location = a['Warsaw'] # finaly data from DB conf table
                timezone = location.timezone
                moon = location.moon_phase(date=datetime.now())
                self._debug(1,"Moon var is {0}".format(moon))
                d = round(float(moon) / 14 * 100,0)+(moon/100)+0.001
                if d > 100:
                    moon_phase = (200 - d)
                else: moon_phase = d
                self._debug(1,"Moonphase is {0}".format(moon_phase))
                maapidb.MaaPiDBConnection.insert_data(rom_id[0],moon_phase,rom_id[2],True)
            except:
                maapidb.MaaPiDBConnection.insert_data(rom_id[0],0,rom_id[2],False)

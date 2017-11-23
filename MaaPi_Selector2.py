#!/usr/bin/python

from lib.MaaPi_DB_connection import MaaPiDBConnection
from datetime import datetime
from MaaPi_Settings import *
import threading
import sched
import time
import sys


class Selector(object):
    debug=1
    start  = datetime.now()
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG Selector    {0} {1}, {2}".format(level, datetime.now(), msg))

    @classmethod
    def to_sec(self,value,unit):
        _seconds=0
        if unit == 2:
            _seconds = value * 60
        elif unit == 3:
            _seconds = value * 3600
        else:
            _seconds = value
        return _seconds

    @classmethod
    def get_data_and_validate(self):
        start  = datetime.now()

        self._debug(2,"Get data from table {0}".format("maapi_device_list"))
        data_devices_list = MaaPiDBConnection().table("maapi_device_list").get()
        self._debug(2,"Get data from table {0}".format("devices"))
        data_devices=MaaPiDBConnection().table("devices").columns(
                                                          "dev_id",
                                                          "dev_type_id",
                                                          "dev_rom_id",
                                                          "dev_bus_type_id",

                                                          "dev_last_update",
                                                          "dev_interval",
                                                          "dev_interval_unit_id",
                                                          "dev_interval_queue",
                                                          ).order_by('dev_id').filters_eq(dev_status=True).get()
        self._debug(1,"ittering {0}".format("data_devices_list"))

        for types in data_devices_list:
            self._debug(2,"ittering {0}".format("data_devices_list"))
            if data_devices_list[types]["device_lib_name"]:
                self._debug(2,"lib and class name is not None".format())
                _temp = __import__('lib.{0}'.format(data_devices_list[types]["device_lib_name"]), globals(), locals(), ['get_value'], -1)
                self._debug(2,"Import modules and class".format())
                devices_list=[]
                self._debug(3,"ittering {0}".format("data_devices"))
                for devices in data_devices:
                    if data_devices[devices]["dev_type_id"] == data_devices_list[types]["id"] and data_devices[devices]["dev_interval_queue"] is not True:
                        self._debug(3,"if dev type id is {0}".format( data_devices_list[types]["device_name"]))
                        if data_devices[devices]["dev_interval"] and data_devices[devices]["dev_interval_unit_id"]:
                            self._debug(3,"if dev interval is not None ".format( ))
                            time_delta = (datetime.now() - data_devices[devices]["dev_last_update"]).total_seconds()
                            self._debug(3,"time delta {0}".format( time_delta))
                            if  time_delta >= self.to_sec(data_devices[devices]["dev_interval"],data_devices[devices]["dev_interval_unit_id"]):
                                self._debug(3,"time delta >= dev_interval ".format( time_delta))
                                MaaPiDBConnection.queue(data_devices[devices]["dev_id"],True)
                                devices_list.append((data_devices[devices]["dev_id"],data_devices[devices]["dev_rom_id"], data_devices_list[types]["device_name"] ))
                self._debug(1,"runing method as thread ".format())
                self._debug(1,"sensors in queue {0} in {1} ".format(devices_list, data_devices_list[types]["device_name"]))
                thread = threading.Thread(target=_temp.class_get_values, args=(devices_list))
                thread.daemon = True
                thread.start()

        time_of_exec = ((float((datetime.now() - start).seconds) * 1000) + (float((datetime.now() - start).microseconds) / 1000))/1000
        self._debug(1,"get_data_and_validate run {0} s".format(time_of_exec))
        return time_of_exec

    @classmethod
    def run(self):
        MaaPiDBConnection.queue_all(False)
        loop = 60
        time_l = ((loop - ((datetime.now() - self.start).seconds + (float((datetime.now() - self.start).microseconds) / 1000000)) /1000) -0.150 ) / loop
        self._debug(1,"preparing time {0} s".format(time_l))

        for i in xrange(loop):
            lag = self.get_data_and_validate()
            time.sleep(time_l-lag)
        self._debug(1,"overal time of exec {0} s".format(((datetime.now() - self.start).seconds + (float((datetime.now() - self.start).microseconds) / 1000000))))


if __name__ == "__main__":
    Selector.run()
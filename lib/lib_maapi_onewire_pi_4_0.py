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

    #read data from sensor
    @classmethod
    def __init__(self,*args):

        for rom_id in args:
            try:
                w1_file = open('/sys/bus/w1/devices/{0}/w1_slave'.format(rom_id[1]), 'r')
                self._debug(1,"open file /sys/bus/w1/devices/{0}/w1_slave".format(rom_id[1]))
                w1_line = w1_file.readline()
                w1_crc = w1_line.rsplit(' ',1)
                w1_crc = w1_crc[1].replace('\n', '')

                if w1_crc=='YES':
                    self._debug(1,"CRC - YES")
                    w1_line = w1_file.readline()
                    w1_temp = w1_line.rsplit('t=',1)
                    temp = float(float(w1_temp[1])/float(1000))
                    self._debug(1,"Value is {0} for rom_id[1] {1}".format(temp,rom_id[1]))
                    w1_file.close()
                    self._debug(1,"Close file")

                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],temp,rom_id[2],True)


                else:
                    w1_file.close()
                    self._debug(1,"CRC False")
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],99999,rom_id[2],False)


            except:
                self._debug(1,"\tERROR reading values from rom_id[1]: {0}".format(rom_id[1]))
                maapidb.MaaPiDBConnection.insert_data(rom_id[0],99999,rom_id[2],False)

    """
    @classmethod
    def scan(self,*args):
        try:
            file_one_wire = open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r')
            dev_rom_id = MaaPiDBConnection().table("devices").filters_eq(dev_enabled=True,device_location=Maapi_location).get()
            var_d=0
            var_i=1
            for line in file_one_wire:
                line2=line.strip('\n')
                for rom in dev_rom_id:
                    if line2 == rom[0]:
                        var_d=1
                if var_d==0:
                    maapidb.MaaPiDBConnection.insert_data(rom_id[0],99999,rom_id[2],False)
                    x.execute("INSERT INTO maapi_scaned_one_wire_list VALUES (default,'{0}' , (SELECT device_name FROM maapi_one_wire_sensors_list WHERE device_id='{1}') ,(SELECT device_description FROM maapi_one_wire_sensors_list WHERE device_id='{2}'), {3})".format(line2,line2[:2],line2[:2],"FALSE" ))
                    conn.commit()
                var_d=0
                var_i+=1
    """

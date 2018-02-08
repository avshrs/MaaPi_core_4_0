#!/usr/bin/python
import psycopg2
import subprocess
import os
from conf.MaaPi_Settings import *
import sys

try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
except:

    def qa(message):
        try:
            if sys.argv[1]=="-v":
                print message
        except:
            pass

    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        qa( "I am unable to connect to the database")
    x = conn.cursor()


    file_one_wire = open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'r')
    qa("file from one wire list opended")
    x.execute("SELECT id from maapi_bustypes where bus_enabled=True AND bus_type='OneWire_pi'")
    bus_id= x.fetchone()[0]
    x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
    conn.commit()
    x.execute("SELECT COUNT(*) FROM devices WHERE dev_bus_type_id={0}".format(bus_id))
    counter = x.fetchone()
    x.execute("SELECT dev_rom_id FROM devices WHERE dev_bus_type_id={0}".format(bus_id))
    dev_rom_id = x.fetchall()

    var_d=0
    var_i=1
    for line in file_one_wire:


        line2=line.strip('\n')
        qa("sensor nr: {0} rom id:{1}".format(var_i,line2))

        for rom in dev_rom_id:

            if line2 == rom[0]:
                qa("for rom: {0} = {1} match\n".format(rom[0],line2))
                var_d=1
        if var_d==0:
            qa( "Adding device to database: {0}".format(line2))
            x.execute("INSERT INTO maapi_scaned_one_wire_list VALUES (default,'{0}' , (SELECT device_name FROM maapi_one_wire_sensors_list WHERE device_id='{1}') ,(SELECT device_description FROM maapi_one_wire_sensors_list WHERE device_id='{2}'), {3})".format(line2,line2[:2],line2[:2],"FALSE" ))
            conn.commit()
        var_d=0
        var_i+=1

    conn.close()



    #x.execute("INSERT INTO devices VALUES (default, default, 0, 'oneWire', '','PI-SYS-CPU-TEMP','cpu-load','cpu-load' , 'sys' ,0,0,'Temperature',0,now(),' ',1,' ',' ',0, ' ',0, ' ',0,1,1,FALSE,FALSE,FALSE,FALSE, ' ',' ',' ')

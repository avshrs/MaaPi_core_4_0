#!/usr/bin/python
import smbus
from datetime import datetime, timedelta
import time
import psycopg2
import RPi.GPIO as GPIO
from MaaPi_Settings import *
import sys



def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

def run():
    """ set mode of gpio """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #datbase init
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()
        x.execute("SELECT id from maapi_bustypes where bus_enabled=True AND bus_type='GpioSwitch'")
        bus_id= x.fetchone()[0]

        x.execute("SELECT COUNT(*) FROM maapi_switch WHERE switch_enabled=True")
        counter = x.fetchone()

        x.execute("SELECT switch_value_min FROM maapi_switch WHERE switch_enabled=True")
        switch_value_min= x.fetchall()

        x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()

        x.execute("SELECT switch_data_from_sens_id FROM maapi_switch WHERE switch_enabled=True")
        switch_data_from_sens_id= x.fetchall()

        x.execute("SELECT switch_reference_sensor_min_id FROM maapi_switch WHERE switch_enabled=True")
        switch_reference_sensor_min_id = x.fetchall()

        x.execute("SELECT switch_reference_sensor_max_id FROM maapi_switch WHERE switch_enabled=True")
        switch_reference_sensor_max_id = x.fetchall()

        x.execute("SELECT switch_reference_sensor_min_e FROM maapi_switch WHERE switch_enabled=True")
        switch_reference_sensor_min_e = x.fetchall()

        x.execute("SELECT switch_reference_sensor_max_e FROM maapi_switch WHERE switch_enabled=True")
        switch_reference_sensor_max_e = x.fetchall()

        x.execute("SELECT switch_value_max FROM maapi_switch WHERE switch_enabled=True")
        switch_value_max= x.fetchall()

        x.execute("SELECT switch_value_max_e FROM maapi_switch WHERE switch_enabled=True")
        switch_value_max_e= x.fetchall()

        x.execute("SELECT switch_value_min_e FROM maapi_switch WHERE switch_enabled=True")
        switch_value_min_e= x.fetchall()

        x.execute("SELECT switch_invert FROM maapi_switch WHERE switch_enabled=True")
        switch_invert= x.fetchall()

        x.execute("SELECT switch_update_rom_id FROM maapi_switch WHERE switch_enabled=True")
        switch_update_id= x.fetchall()

        x.execute("SELECT switch_range_acc FROM maapi_switch WHERE switch_enabled=True")
        switch_range_acc= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_e FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_e= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_id FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_id= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_value_max_e FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_value_max_e= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_value_max FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_value_max= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_value_min_e FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_value_min_e= x.fetchall()

        x.execute("SELECT switch_turn_on_at_sensor_value_min FROM maapi_switch WHERE switch_enabled=True")
        switch_turn_on_at_sensor_value_min= x.fetchall()



        """ Exec """

        def get_state(i,referenceId,sensId,rangeAcc,valueToCopmare,signToCompare):
            """
            referenceId     = if int use ref sensor if None not.
            sensId          = updated sensor id
            rangeAcc        = accuracy range
            valueToCopmare  = value to compare
            signToCompare   = sign to compare 1 = > ,  0 = <
            """
            qa("\nget data - id={0}, referenceId = {1},  sensId = {2},  rangeAcc = {3}, valueToCopmare  = {4}, signToCompare ={5}".format(i, referenceId,sensId,rangeAcc,valueToCopmare,signToCompare))

            x.execute("SELECT dev_value FROM devices WHERE dev_id={0}".format(sensId))
            sensId_dev_value = x.fetchone()[0]
            x.execute("SELECT dev_rom_id FROM devices WHERE dev_id={0}".format(sensId))
            sensId_dev_rom_id = x.fetchone()[0]
            qa("{0} - function {2} - if reference {1}".format(datetime.now(),referenceId,i))

            """__________________________________________________________________________________________________________________________________________"""
            if referenceId is not None:
                x.execute("SELECT dev_rom_id FROM devices WHERE dev_id={0}".format(referenceId))
                switch_reference_dev_rom_id = x.fetchone()[0]

                qa("{0} - function {2} - switch_reference_dev_rom_id {1}".format(datetime.now(),switch_reference_dev_rom_id,i))
                switch_reference_value={}
                switch_reference_isNone=False

            switch_update_value={}
            switch_update_isNone=False

            """__________________________________________________________________________________________________________________________________________"""
            for i2 in xrange(rangeAcc):

                date_now_a = datetime.now().replace(second=0,microsecond=0) - timedelta(minutes=i2)
                date_now_b = datetime.now().replace(second=0,microsecond=0) - timedelta(minutes=i2+1)
                try:
                    x.execute("""SELECT dev_value from maapi_dev_rom_{0}_values where dev_timestamp>='{1}' and dev_timestamp<='{2}'""".format(sensId_dev_rom_id.replace("-", "_"),date_now_b,date_now_a))
                    switch_update_value[i2]=x.fetchone()[0]
                    qa("{0} - function {2} - for                switch_update_value {1}".format(datetime.now(),switch_update_value[i2],i))
                except:
                    switch_update_value[i2]=None
                    switch_update_isNone=True
                if referenceId is not None:
                    try:
                        x.execute("""SELECT dev_value from maapi_dev_rom_{0}_values where dev_timestamp>='{1}' and dev_timestamp<='{2}'""".format(switch_reference_dev_rom_id.replace("-", "_"),date_now_b,date_now_a))
                        switch_reference_value[i2]=x.fetchone()[0]
                        qa("{0} - function {2} - for if refererd switch_reference_value {1}".format(datetime.now(),switch_reference_value[i2],i))
                    except:
                        switch_reference_value[i2]=None
                        switch_reference_isNone=True

            value_is_not=0
            value_is_None=0
            qa("{0} - function {2} + for if signToCompare==1 {1}".format(datetime.now(),signToCompare,i))

            """__________________________________________________________________________________________________________________________________________"""
            for i3 in xrange(switch_range_acc[i][0]):
                if signToCompare==0:

                    if referenceId is not None:
                        if switch_reference_isNone is not True and switch_update_isNone is not True :
                            if switch_update_value[i3] <  (switch_reference_value[i3] - valueToCopmare) :
                                qa("{0} - function {4} - if ref switch_update_value={1} <  (switch_reference_value{2} - valueToCopmare={3}) true".format(datetime.now(),switch_update_value[i3],switch_reference_value[i3],valueToCopmare,i))
                            else:
                                qa("{0} - function {4} - if ref switch_update_value={1} <  (switch_reference_value{2} - valueToCopmare={3}) false".format(datetime.now(),switch_update_value[i3],switch_reference_value[i3],valueToCopmare,i))
                                value_is_not+=1
                        else:
                            value_is_None+=1
                            qa("{0} - function {2} - for ref else value is None err reading data =={1}".format(datetime.now(),value_is_None,i))
                    else:
                        if switch_update_isNone is not True :
                            qa("{0} - function - for if switch_update_isNone=={1}".format(datetime.now(),switch_update_isNone))
                            if switch_update_value[i3] <  valueToCopmare :
                                qa("{0} - function {3} - for if switch_update_value={1} < switch_update_value={2}".format(datetime.now(),switch_update_value[i3],switch_update_value[i3],i))
                            else:
                                qa("{0} - function {2} - for else value_is_not=={1}".format(datetime.now(),value_is_not,i))
                                value_is_not+=1
                        else:
                            qa("{0} - function {2} - for else value_is_None=={1}".format(datetime.now(),value_is_None,i))
                            value_is_None+=1

                """__________________________________________________________________________________________________________________________________________"""
                if signToCompare==1:

                    if referenceId is not None:

                        if switch_reference_isNone is not True and switch_update_isNone is not True:
                            if switch_update_value[i3] > (switch_reference_value[i3] + valueToCopmare):
                                qa("{0} - function {4} + if ref switch_update_value={1} >  (switch_reference_value{2} + valueToCopmare={3}){5} true".format(datetime.now(),switch_update_value[i3],switch_reference_value[i3],valueToCopmare,i,switch_reference_value[i3]+valueToCopmare))
                            else:
                                qa("{0} - function {4} + if ref switch_update_value={1} >  (switch_reference_value{2} + valueToCopmare={3}) false".format(datetime.now(),switch_update_value[i3],switch_reference_value[i3],valueToCopmare,i))
                                value_is_not+=1
                        else:
                            qa("{0} - function {2} + for else value_error=={1}".format(datetime.now(),value_is_None,i))
                            value_is_None+=1
                    else:
                        if switch_update_isNone is not True :
                            qa("{0} - function {2} + for if switch_update_isNone=={1}".format(datetime.now(),switch_update_isNone,i))
                            if switch_update_value[i3] > valueToCopmare:
                                qa("{0} - function {3} + for if switch_update_value={1} < switch_update_value={2}".format(datetime.now(),switch_update_value[i3],switch_update_value[i3],i))
                            else:
                                qa("{0} - function {2} + for else value_is_not=={1}".format(datetime.now(),value_is_not,i))
                                value_is_not+=1
                        else:
                            qa("{0} - function {2} + for else value_is_None=={1}".format(datetime.now(),value_is_None,i))
                            value_is_None+=1

            if value_is_not==0 and value_is_None==0:
                qa("{0} - function TRUE  gpio = 1".format(datetime.now(),i,value_is_not,value_is_None))
                return 1
            else:
                qa("{0} - function FALSE  gpio = 0".format(datetime.now(),i,value_is_not,value_is_None))
                return 0

        """__________________________________________________________________________________________________________________________________________"""

        for i in xrange(0,counter[0]):
            Value_min=0
            Value_max=0

            x.execute("SELECT dev_gpio_pin FROM devices WHERE dev_id='{0}' ".format(switch_update_id[i][0]))
            switch_gpio_nr = x.fetchone()[0]
            qa("\n\n\n{0} - dev {1}      - exec gpio - gpio nr {2}".format(datetime.now(),i,switch_gpio_nr))
            GPIO.setup(switch_gpio_nr, GPIO.OUT)

            x.execute("SELECT dev_bus_type_id FROM devices WHERE dev_id='{0}' ".format(switch_update_id[i][0]))
            dev_bus_type_id = x.fetchone()[0]




            if dev_bus_type_id == bus_id:
                if switch_value_min_e[i][0]:
                    Value_min = get_state(i,switch_reference_sensor_min_id[i][0], switch_data_from_sens_id[i][0], switch_range_acc[i][0], switch_value_min[i][0], 0)
                if switch_value_max_e[i][0]:
                    Value_max = get_state(i,switch_reference_sensor_max_id[i][0], switch_data_from_sens_id[i][0], switch_range_acc[i][0], switch_value_max[i][0], 1)

                if switch_turn_on_at_sensor_e[i][0]:
                    qa("{0} - dev {1}      - if switch_turn_on_at_sensor_e = {2}".format(datetime.now(),i,switch_turn_on_at_sensor_e[i][0]))
                    if switch_turn_on_at_sensor_id is not None:
                        qa("{0} - dev {1}      - if switch_turn_on_at_sensor_id = {2}".format(datetime.now(),i,switch_turn_on_at_sensor_id[i][0]))
                        x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(switch_turn_on_at_sensor_id[i][0]))
                        dev_value_on = x.fetchone()[0]
                        if switch_turn_on_at_sensor_value_min_e[i][0]:
                            qa("{0} - dev {1}      - if switch_turn_on_at_sensor_value_min_e = {2}".format(datetime.now(),i,switch_turn_on_at_sensor_value_min_e[i][0]))
                            if dev_value_on < switch_turn_on_at_sensor_value_min[i][0]:
                                qa("{0} - dev {1}      - if dev_value_on < switch_turn_on_at_sensor_value_min[i][0] = {2}".format(datetime.now(),i,dev_value_on < switch_turn_on_at_sensor_value_min[i][0]))
                            else:
                                Value_min=0
                        if switch_turn_on_at_sensor_value_max_e[i][0]:
                            qa("{0} - dev {1}      - if  switch_turn_on_at_sensor_value_max_e[i][0] = {2}".format(datetime.now(),i,switch_turn_on_at_sensor_value_max_e[i][0]))
                            if dev_value_on > switch_turn_on_at_sensor_value_max[i][0]:
                                qa("{0} - dev {1}      - if  dev_value_on > switch_turn_on_at_sensor_value_max[i][0] = {2}".format(datetime.now(),i,dev_value_on > switch_turn_on_at_sensor_value_max[i][0]))
                            else:
                                Value_max=0
                    else:
                        print "err dev id == none"

                if switch_invert[i][0]:
                    qa("{0} - dev {1}      - invert  ".format(datetime.now(),i,dev_value_on > switch_turn_on_at_sensor_value_max[i][0]))
                    if Value_min==1:
                        Value_min=0
                    if Value_min==0:
                        Value_min=1
                    if Value_max==1:
                        Value_max=0
                    if Value_max==0:
                        Value_max=1

                if Value_min == 0 and Value_max ==0:
                    GPIO.output(switch_gpio_nr,0)
                    qa("{0} - dev {1}      - and exec gpio - min={2} and max={3} == 0".format(datetime.now(),i,Value_min,Value_max))
                    if GPIO.input(switch_gpio_nr) is not True:
                        qa("{1} - dev {2}      - exec gpio - gpio state 0".format(GPIO.input(switch_gpio_nr),datetime.now(),i))
                        x.execute("SELECT dev_value FROM devices WHERE dev_id={0}".format(switch_update_id[i][0]))
                        dev_value_old = x.fetchone()[0]
                        x.execute("UPDATE devices SET dev_value={0}, dev_value_old={1}, dev_last_update=NOW(), dev_read_error='{2}'  WHERE dev_id='{3}'".format(0, dev_value_old,'ok' ,switch_update_id[i][0]))
                        conn.commit()
                        x.execute("SELECT dev_rom_id FROM devices WHERE dev_id='{0}' ".format(switch_update_id[i][0]))
                        dev_rom_id = x.fetchone()[0]
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), switch_update_id[i][0],0))
                        conn.commit()
                elif Value_min == 1 or Value_max ==1:
                    GPIO.output(switch_gpio_nr,1)
                    qa("{0} - dev {1}      - or exec gpio - min or max == 1".format(datetime.now(),i))
                    if GPIO.input(switch_gpio_nr):
                        qa("{1} - dev {2}      - exec gpio - gpio state 1".format(GPIO.input(switch_gpio_nr),datetime.now(),i))
                        x.execute("SELECT dev_value FROM devices WHERE dev_id={0}".format(switch_update_id[i][0]))
                        dev_value_old = x.fetchone()[0]
                        x.execute("UPDATE devices SET dev_value={0}, dev_value_old={1}, dev_last_update=NOW(), dev_read_error='{2}'  WHERE dev_id='{3}'".format(1, dev_value_old,'ok' ,switch_update_id[i][0]))
                        conn.commit()
                        x.execute("SELECT dev_rom_id FROM devices WHERE dev_id='{0}' ".format(switch_update_id[i][0]))
                        dev_rom_id = x.fetchone()[0]
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), switch_update_id[i][0],1))
                        conn.commit()

        conn.close()
try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()

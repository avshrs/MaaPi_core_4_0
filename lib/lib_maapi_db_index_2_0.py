#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.0
#                 Send Mail When Condtions are met
#
##############################################################

#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from MaaPi_Settings import *
from MaaPi_DB_connection import select_data, insert_data, update_cron
from datetime import datetime, timedelta
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys


def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

def run():
        mail_table = select_single_table_data("maapi_mail")
        devices_table = select_single_table_data("devices")
        update_cron(sys.argv[0],Maapi_location)

        x.execute("SELECT mail_data_from_sensor_id FROM maapi_mail WHERE mail_enabled=True")
        mail_data_from_sensor_id = x.fetchall()

        x.execute("SELECT id FROM maapi_mail WHERE mail_enabled=True")
        mail_id = x.fetchall()

        x.execute("SELECT mail_data_id FROM maapi_mail WHERE mail_enabled=True")
        mail_data_id = x.fetchall()

        x.execute("SELECT mail_condition_min_e FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_min_e = x.fetchall()

        x.execute("SELECT mail_condition_min FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_min = x.fetchall()

        x.execute("SELECT mail_condition_max_e FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_max_e = x.fetchall()

        x.execute("SELECT mail_condition_max FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_max = x.fetchall()

        x.execute("SELECT mail_name FROM maapi_mail WHERE mail_enabled=True")
        mail_name = x.fetchall()

        x.execute("SELECT mail_send_to FROM maapi_mail WHERE mail_enabled=True")
        mail_send_to = x.fetchall()

        x.execute("SELECT mail_subject FROM maapi_mail WHERE mail_enabled=True")
        mail_subject = x.fetchall()

        x.execute("SELECT mail_mesge_if_min FROM maapi_mail WHERE mail_enabled=True")
        mail_mesge_if_min = x.fetchall()

        x.execute("SELECT mail_mesge_if_max FROM maapi_mail WHERE mail_enabled=True")
        mail_mesge_if_max = x.fetchall()

        x.execute("SELECT mail_range_acc FROM maapi_mail WHERE mail_enabled=True")
        mail_range_acc = x.fetchall()

        x.execute("SELECT mail_last_sended_at_value_min FROM maapi_mail WHERE mail_enabled=True")
        mail_last_sended_at_value_min = x.fetchall()

        x.execute("SELECT mail_last_sended_at_value_max FROM maapi_mail WHERE mail_enabled=True")
        mail_last_sended_at_value_max = x.fetchall()


        def check_conditiion(mail_data_from_sensor_id,mail_condition,mail_range_acc,signToCompare):
            x.execute("SELECT dev_rom_id FROM devices WHERE dev_id={0}".format(mail_data_from_sensor_id))
            source_dev_rom_id = x.fetchone()[0]
            qa("{0} - function {2} - if reference {1}".format(datetime.now(),mail_data_from_sensor_id,i))

            switch_update_value={}
            switch_update_isNone=False

            for i2 in xrange(mail_range_acc):
                date_now_a = datetime.now().replace(second=0,microsecond=0) - timedelta(minutes=i2)
                date_now_b = datetime.now().replace(second=0,microsecond=0) - timedelta(minutes=i2+1)
                try:
                    x.execute("""SELECT dev_value from maapi_dev_rom_{0}_values where dev_timestamp>='{1}' and dev_timestamp<='{2}'""".format(source_dev_rom_id.replace("-", "_"),date_now_b,date_now_a))
                    switch_update_value[i2]=x.fetchone()[0]
                    qa("{0} - function {2} - for                switch_update_value {1}".format(datetime.now(),switch_update_value[i2],i))
                except:
                    switch_update_value[i2]=None
                    switch_update_isNone=True
            value_is_not=0
            value_is_None=0
            for i3 in xrange(mail_range_acc):

                if signToCompare==0:
                    if switch_update_isNone is not True :
                        qa("{0} - function - for if switch_update_isNone=={1}".format(datetime.now(),switch_update_isNone))
                        if switch_update_value[i3] <  mail_condition :
                            qa("{0} - function {3} - for if switch_update_value={1} < mail_condition={2}".format(datetime.now(),switch_update_value[i3],mail_condition,i))
                        else:
                            qa("{0} - function {2} - for else value_is_not=={1}".format(datetime.now(),value_is_not,i))
                            value_is_not+=1
                    else:
                        qa("{0} - function {2} - for else value_is_None=={1}".format(datetime.now(),value_is_None,i))
                        value_is_None+=1
                if signToCompare==1:
                    if switch_update_isNone is not True :
                        qa("{0} - function - for if switch_update_isNone=={1}".format(datetime.now(),switch_update_isNone))
                        if switch_update_value[i3] >  mail_condition :
                            qa("{0} - function {3} - for if switch_update_value={1} < mail_condition={2}".format(datetime.now(),switch_update_value[i3],mail_condition,i))
                        else:
                            qa("{0} - function {2} - for else value_is_not=={1}".format(datetime.now(),value_is_not,i))
                            value_is_not+=1
                    else:
                        qa("{0} - function {2} - for else value_is_None=={1}".format(datetime.now(),value_is_None,i))
                        value_is_None+=1

            if value_is_not==0 and value_is_None==0:
                qa("{0} - function TRUE  gpio = 1".format(datetime.now(),i,value_is_not,value_is_None))
                return 1
            else:
                qa("{0} - function FALSE  gpio = 0".format(datetime.now(),i,value_is_not,value_is_None))
                return 0


        for i in xrange(0,counter[0]):
            x.execute("SELECT ml_user FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_user = x.fetchone()[0]

            x.execute("SELECT ml_password FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_password  = x.fetchone()[0]

            x.execute("SELECT ml_smtp FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_smtp = x.fetchone()[0]

            x.execute("SELECT ml_port FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_port = x.fetchone()[0]


            qa("for")


            if mail_condition_min_e[i][0]:
                qa("mail_condition_min_e {0}".format(mail_condition_min_e[i][0]))
                qa("\n\n{0} - function {2} - check condtion min  for {1}".format(datetime.now(),mail_name[i][0],i))
                """exec fuction check"""
                value_min= check_conditiion(mail_data_from_sensor_id[i][0],mail_condition_min[i][0],mail_range_acc[i][0],0)

                if value_min:
                    if mail_last_sended_at_value_min[i][0] <= mail_condition_min[i][0]:
                        pass
                    else:
                        qa("value {0} <= mail_condition_min {1}".format(value_min, mail_condition_min[i][0]))
                        msg = MIMEMultipart()
                        msg['From'] = ml_user
                        msg['To'] = mail_send_to[i][0]
                        msg['Subject'] = mail_subject[i][0]
                        msg.attach(MIMEText('{0} - value {1}'.format(mail_mesge_if_min[i][0],value_min)))
                        mailServer = smtplib.SMTP(ml_smtp, ml_port)
                        mailServer.ehlo()
                        mailServer.starttls()
                        mailServer.ehlo()
                        mailServer.login(ml_user, ml_password)
                        mailServer.sendmail(ml_password, mail_send_to[i][0], msg.as_string())
                        mailServer.close()
                        x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_min='{0}' WHERE id='{1}'".format(value_max,mail_id[i][0]))
                        conn.commit()
                else:
                    x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_min='{0}' WHERE id='{1}'".format(value_max,mail_id[i][0]))
                    conn.commit()

            if mail_condition_max_e[i][0]:
                qa("mail_condition_max_e {0}".format(mail_condition_max_e[i][0]))
                """exec fuction check"""
                qa("\n\n{0} - function {2} - check condtion max  for {1}".format(datetime.now(),mail_name[i][0],i))
                value_max= check_conditiion(mail_data_from_sensor_id[i][0],mail_condition_max[i][0],mail_range_acc[i][0],1)

                if value_max:
                    qa("value {0} >= mail_condition_max {1}".format(value_max, mail_condition_max[i][0]))
                    if mail_last_sended_at_value_max[i][0] >= mail_condition_max[i][0]:
                        pass
                        qa("last {0} >= condition max {1} ".format(value_max, mail_condition_max[i][0]))
                    else:

                        msg = MIMEMultipart()
                        msg['From'] = ml_user
                        msg['To'] = mail_send_to[i][0]
                        msg['Subject'] = mail_subject[i][0]
                        msg.attach(MIMEText('{0} - value {1}'.format(mail_mesge_if_max[i][0],value_max)))
                        mailServer = smtplib.SMTP(ml_smtp, ml_port)
                        mailServer.ehlo()
                        mailServer.starttls()
                        mailServer.ehlo()
                        mailServer.login(ml_user, ml_password)
                        mailServer.sendmail(ml_password, mail_send_to[i][0], msg.as_string())
                        mailServer.close()
                        x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_max='{0}' WHERE id='{1}'".format(value_max,mail_id[i][0]))
                        conn.commit()
                else:
                    x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_max='{0}' WHERE id='{1}'".format(value_max,mail_id[i][0]))
                    conn.commit()


try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()

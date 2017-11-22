#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from crontab import CronTab
from conf.MaaPi_Settings import *
import psycopg2
import sys




def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

def run():
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        qa("I am unable to connect to the database")
    else:
        x = conn.cursor()

        x.execute("SELECT COUNT(*) FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' ".format(Maapi_location) )
        counter = x.fetchone()[0]

        x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()

        x.execute("SELECT id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_id = x.fetchall()

        x.execute("SELECT cron_minute_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_minute_id = x.fetchall()

        x.execute("SELECT cron_minute_on_every_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_minute_on_every_id = x.fetchall()

        x.execute("SELECT cron_hour_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_hour_id = x.fetchall()

        x.execute("SELECT cron_hour_on_every_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_hour_on_every_id = x.fetchall()

        x.execute("SELECT cron_day_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_day_id = x.fetchall()

        x.execute("SELECT cron_day_on_every_id FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_day_on_every_id = x.fetchall()

        x.execute("SELECT cron_interpreter FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_interpreter = x.fetchall()

        x.execute("SELECT cron_file_path FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_file_path = x.fetchall()

        x.execute("SELECT cron_comment FROM maapi_cron WHERE cron_enabled=True and cron_where_exec='{0}' order by id".format(Maapi_location) )
        cron_comment = x.fetchall()

        my_cron = CronTab(user=Maapi_sys_user)
        my_cron_len=len(my_cron)
        var_i=0

        for i in xrange(counter):

            qa("{0} from {1}".format(i+1,counter))
            """ if remove some cron task from dadbase"""

            if my_cron_len > counter:
                """ remove all at once """
                if var_i == 0:
                    qa("cron > db")
                    my_cron.remove_all()
                    my_cron.write()
                    var_i=1

                """ create new crons """
                job = my_cron.new(command="{0} {1}".format(cron_interpreter[i][0],cron_file_path[i][0]))
                job.set_comment("{0}".format(cron_id[i][0]))
                x.execute("UPDATE maapi_cron set cron_last_exec_date=now() where id={0}".format(cron_id[i][0]))
                conn.commit()
                if cron_minute_id[i][0] is not None:
                    if cron_minute_on_every_id[i][0] is not None:
                        if cron_minute_on_every_id[i][0] == 1:
                            job.minute.on(cron_minute_id[i][0])
                            qa("cron_minute_on_every_id == on")
                        if cron_minute_on_every_id[i][0] == 2:
                            job.minute.every(cron_minute_id[i][0])
                            qa("cron_minute_on_every_id == every")
                    else:
                        qa("cron_minute_on_every_id == None")
                else:
                    qa("cron_minute_id == None")


                if cron_hour_id[i][0] is not None:
                    if cron_hour_on_every_id[i][0] is not None:
                        if cron_hour_on_every_id[i][0] ==1:
                            job.hour.on(cron_hour_id[i][0])
                            qa("cron_hour_on_every_id == on")
                        if cron_hour_on_every_id[i][0] ==2:
                            job.hour.every(cron_hour_id[i][0])
                            qa("cron_hour_on_every_id == every")
                    else:
                        qa("cron_hour_on_every_id == None")
                else:
                    qa("cron_hour_id == None")


                if cron_day_id[i][0] is not None:
                    if cron_day_on_every_id[i][0] is not None:
                        if cron_day_on_every_id[i][0] == 1:
                            job.day.on(cron_day_id[i][0])
                            qa("cron_day_on_every_id == on")
                        if cron_day_on_every_id[i][0] == 2:
                            job.day.every(cron_day_id[i][0])
                            qa("cron_day_on_every_id == every")
                    else:
                        qa("cron_day_on_every_id == None")
                else:
                    qa("cron_day_id == None")



                my_cron.write()
            else:
                try:
                    job = my_cron[i]
                    x.execute("UPDATE maapi_cron set cron_last_exec_date=now() where id={0}".format(cron_id[i][0]))
                    conn.commit()

                    """ if command changed - update """
                    if job.command == "{0} {1}".format(cron_interpreter[i][0],cron_file_path[i][0]):
                        qa("command == true")
                    else:
                        job.set_command("{0} {1}".format(cron_interpreter[i][0],cron_file_path[i][0]))
                        qa("command updated")
                        my_cron.write()
                    """ if comment changed - update """
                    if job.comment == "{0}".format(cron_id[i][0]):
                        qa("comment == true")
                    else:
                        job.set_comment("{0}".format(cron_id[i][0]))
                        qa("comment updated")
                        my_cron.write()

                    """ if slices changed - update """
                    qa("minute - {0} should {1}".format(job.minute,cron_minute_id[i][0]))
                    qa("hour   - {0} should {1}".format(job.hour,cron_hour_id[i][0]))
                    qa("day    - {0} should {1}".format(job.day,cron_day_id[i][0]))
                    #qa("on every {0}".format(job.day.every(10)))

                    """Cron minute value update"""
                    """on """
                    if cron_minute_id[i][0] is not None:
                        if cron_minute_on_every_id[i][0] ==1 :
                            if job.minute == "{0}".format(cron_minute_id[i][0]):
                                qa("e minute== true")
                            else:
                                job.minute.on(cron_minute_id[i][0])
                                qa("e minute updated {0}".format(job.minute.on(cron_minute_id[i][0])))
                                my_cron.write()

                        """on every"""
                        if cron_minute_on_every_id[i][0] == 2:
                            if cron_minute_id[i][0] == 1:
                                if job.minute == "*" :
                                    qa("e minute== true")
                            elif job.minute == "*/{0}".format(cron_minute_id[i][0]):
                                qa("e minute== true")
                            else:
                                job.minute.every(cron_minute_id[i][0])
                                qa("e minute updated {0}".format(job.minute.every(cron_minute_id[i][0])))
                                my_cron.write()
                        if cron_minute_on_every_id[i][0] == None:
                            job.minute.every(1)
                            qa("e minute  == none")
                            my_cron.write()


                    """Cron hour value update"""
                    """on """
                    if cron_hour_id[i][0] is not None:
                        if cron_hour_on_every_id[i][0] == 1:
                            if job.hour == "{0}".format(cron_hour_id[i][0]):
                                qa("o hour  == true")
                            else:
                                job.hour.on(cron_hour_id[i][0])
                                qa("o hour  updated {0}".format(job.hour.on(cron_hour_id[i][0])))
                                my_cron.write()
                        """on every"""
                        if cron_hour_on_every_id[i][0] == 2:
                            if cron_hour_id[i][0] == 1:
                                if job.hour == "*" :
                                    qa("e hour== true")
                            elif job.hour == "*/{0}".format(cron_hour_id[i][0]):
                                qa("e hour== true")
                            else:
                                job.hour.every(cron_hour_id[i][0])
                                qa("e hour updated {0}".format(job.hour.every(cron_hour_id[i][0])))
                                my_cron.write()

                        if cron_hour_on_every_id[i][0] == None:
                            job.hour.every(1)
                            qa("e hour  == none")
                            my_cron.write()


                    """Cron day value update"""
                    """on """
                    if cron_day_id[i][0] is not None:
                        if cron_day_on_every_id[i][0] == 1:
                            if job.day == "{0}".format(cron_day_id[i][0]):
                                qa("o day   == true")
                            else:
                                job.day.on(cron_day_id[i][0])
                                qa("o day   updated {0}".format(cron_id[i][0]))
                                my_cron.write()
                        """on every"""

                        if cron_day_on_every_id[i][0] == 2:
                            if cron_day_id[i][0] == 1:
                                if job.day == "*" :
                                    qa("e day== true")
                            elif job.day == "*/{0}".format(cron_day_id[i][0]):
                                qa("e day== true")
                            else:
                                job.day.every(cron_day_id[i][0])
                                qa("e day updated {0}".format(job.day.every(cron_day_id[i][0])))
                                my_cron.write()

                            """none"""
                        if cron_day_on_every_id[i][0] == None:
                            job.day.every(1)
                            qa("e day   == none")
                            my_cron.write()


                except:




                    """ if cron task not exist - create """
                    job = my_cron.new(command="{0} {1}".format(cron_interpreter[i][0],cron_file_path[i][0]))
                    if cron_minute_id[i][0] is not None:
                        if cron_minute_on_every_id[i][0] is not None:
                            if cron_minute_on_every_id[i][0] == 1:
                                job.minute.on(cron_minute_id[i][0])
                                qa("cron_minute_on_every_id == on")
                            if cron_minute_on_every_id[i][0] == 2:
                                job.minute.every(cron_minute_id[i][0])
                                qa("cron_minute_on_every_id == every")
                        else:
                            qa("cron_minute_on_every_id == None")
                    else:
                        qa("cron_minute_id == None")


                    if cron_hour_id[i][0] is not None:
                        if cron_hour_on_every_id[i][0] is not None:
                            if cron_hour_on_every_id[i][0] == 1:
                                job.hour.on(cron_hour_id[i][0])
                                qa("cron_hour_on_every_id == on")
                            if cron_hour_on_every_id[i][0] == 2:
                                job.hour.every(cron_hour_id[i][0])
                                qa("cron_hour_on_every_id == every")
                        else:
                            qa("cron_hour_on_every_id == None")
                    else:
                        qa("cron_hour_id == None")


                    if cron_day_id[i][0] is not None:
                        if cron_day_on_every_id[i][0] is not None:
                            if cron_day_on_every_id[i][0] == 1:
                                job.day.on(cron_day_id[i][0])
                                qa("cron_day_on_every_id == on")
                            if cron_day_on_every_id[i][0] == 2:
                                job.day.every(cron_day_id[i][0])
                                qa("cron_day_on_every_id == every")
                        else:
                            qa("cron_day_on_every_id == None")
                    else:
                        qa("cron_day_id == None")
                    job.set_comment("{0}".format(cron_id[i][0]))
                    qa("except create ")
                    my_cron.write()

        conn.close()

try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()

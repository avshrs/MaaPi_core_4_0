#!/usr/bin/python
import psycopg2
from MaaPi_Settings import *
import sys


def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

try:
    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
except:
    print "I am unable to connect to the database"
else:
    x = conn.cursor()

    x.execute("SELECT COUNT(*) FROM m_functions WHERE f_status=1 AND f_interval=1")
    counter = x.fetchone()

    x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
    conn.commit()

    x.execute("SELECT f_name FROM m_functions WHERE f_status=1 AND f_interval=1")
    f_run= x.fetchall()
    for i in xrange(0,counter[0]):
       qa( f_run[i][0])
       try:
           x.execute("SELECT {0};".format(f_run[i][0]))
           qa( "execute")
       except psycopg2.IntegrityError:
           conn.rollback()
           qa( "rollback - sql error - running sql connand")
           x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'MaaPi_runSQLfunction.py' , 'sql error -  running sql connand' , 'IntegrityError')")
           conn.commit()
       else:
           conn.commit()
           qa( "commit")
    conn.close()

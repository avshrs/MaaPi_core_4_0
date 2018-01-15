#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 3.1
#                   connection with DB
#
##############################################################
import psycopg2
from datetime import datetime, timedelta
from conf.MaaPi_Settings import *


class MaaPiDBConnection(object):
    debug = 0
    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG MaaPi Connection DB Main {0} {1}, {2}".format(level, datetime.now(), msg))

    @classmethod
    def insert_data(self,senor_id,value,sensor_type,status):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
            self._debug(1,"open database connection")

        except:
            print ("I am unable to connect to the database")
        else:
            self._debug(1,"SENSOR ID ={0}".format(senor_id))
            self._debug(1,"value ={0}".format(value))
            self._debug(1,"sensor_type ={0}".format(sensor_type))
            x = conn.cursor()
            self._debug(1,"x connection cursor")
            x.execute("SELECT dev_value, dev_rom_id, dev_collect_values_to_db FROM devices WHERE dev_id='{0}' and dev_status=True".format(senor_id))
            db_data = x.fetchone()
            self._debug(1,"get data from devices")
            try:
                x.execute("UPDATE devices SET dev_value_old={0} WHERE dev_id='{1}' and dev_status=True".format(db_data[0],senor_id))
                conn.commit()
            except:
                pass
            if status is True:
                self._debug(1,"sensor status TRUE")
                """if stst is true, update actual value, date and stat on devices"""
                if value == True:
                    x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(1,senor_id))
                    conn.commit()
                    if db_data[2]:
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,1))
                        conn.commit()
                    """if dev_collect_values_to_db true - enable write to values table"""
                elif value == False:
                    x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(0,senor_id))
                    conn.commit()
                    if db_data[2]:
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,0))
                        conn.commit()
                    """if dev_collect_values_to_db true - enable write to values table"""
                else:
                    x.execute("UPDATE devices SET dev_value={0}, dev_interval_queue = {2}, dev_last_update=NOW(), dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(value,senor_id,False))
                    conn.commit()

                    if db_data[2]:
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,value))
                        conn.commit()
            else:
                x.execute("UPDATE devices SET  dev_interval_queue = {2},dev_value={0},dev_read_error='Error' WHERE dev_id='{1}' and dev_status=True".format(9999,senor_id,False))
                conn.commit()
            conn.close()



    @classmethod
    def queue(self,dev_id,status):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print ("I am unable to connect to the database")
        else:
            #print("time={0}\t file name={1}\t file_location={2}".format(time,file_name,Maapi_location))

            x = conn.cursor()
            if dev_id == '*':
                x.execute("UPDATE devices SET dev_interval_queue={0} where dev_status=TRUE".format(status))
                conn.commit()
            else:
                x.execute("UPDATE devices SET dev_interval_queue={0} where dev_id={1}".format(status,dev_id))
                conn.commit()
            conn.close()


    @classmethod
    def select_last_nr_of_values(self,dev_id,range_nr):
            try:
                conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
            except:
                print "I am unable to connect to the database"
            else:
                x = conn.cursor()

                try:
                    x.execute("SELECT dev_rom_id FROM devices where dev_id={0}".format(dev_id))
                    dev_rom_id = x.fetchone()[0]
                    x.execute("SELECT dev_read_error FROM devices where dev_id={0}".format(dev_id))
                    error = x.fetchone()[0]

                except (Exception, psycopg2.DatabaseError) as error:
                    values_history_error=True
                else:
                    values_history=[]
                    if error == "ok":
                        x.execute("""SELECT dev_value, dev_timestamp from maapi_dev_rom_{0}_values  order by dev_timestamp desc limit  {1}""".format(dev_rom_id.replace("-", "_"),range_nr))
                        values_history_temp = x.fetchall()
                        for i in range(range_nr):
                            values_history.append(values_history_temp[i][0])


                self._debug(1,"value_history{0}".format(values_history))

                conn.close()
            return  values_history

    @classmethod
    def queue_all(self,status):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print ("I am unable to connect to the database")
        else:
            #print("time={0}\t file name={1}\t file_location={2}".format(time,file_name,Maapi_location))
            x = conn.cursor()
            x.execute("UPDATE devices SET dev_interval_queue={0} ".format(status))
            conn.commit()
            conn.close()

    def columns(self, *args):
        self.columns_ = args
        return self

    def filters_eq(self, **kwargs):
        self.filters_ = kwargs
        return self

    def order_by(self, *args):
        self.orders_ = args
        return self

    def if_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def table(self, *args):
        if len(args) != 1:
            raise ValueError(
                ".get_table('table name') should only have a table name")
        self.table_ = args[0]
        return self

    def get(self):
        if self.columns_:
            c_len = len(self.columns_)
            c_i = 1
            columns = " "
            for c in self.columns_:
                if c_len > 1:
                    columns += "{0}".format(c)
                    if c_i < c_len:
                        columns += ", "
                    c_i += 1
                else:
                    columns += "{0}".format(c)
        else:
            columns = "*"
            self.columns_var = "*"

        query = "SELECT {0} FROM {1} ".format(columns, self.table_)

        if self.filters_:
            f_len = len(self.filters_)
            f_i = 1
            query += "WHERE "
            for i in self.filters_:
                if f_i == 1:
                    if self.if_number(self.filters_[i]):
                        query += " {0} = {1}".format(i, self.filters_[i])
                    else:
                        query += " {0} = '{1}'".format(i, self.filters_[i])
                else:
                    query += " and "
                    if self.if_number(self.filters_[i]):
                        query += " {0} = {1}".format(i, self.filters_[i])
                    else:
                        query += " {0} = '{1}'".format(i, self.filters_[i])
                f_i += 1
        if self.orders_:
            try:
                self.orders_[1]
            except:
                query += " ORDER BY {0}".format(self.orders_[0])
            else:
                if self.orders_[1] == "asc" or self.orders_[1] == "ASC" or self.orders_[1] == "desc" or self.orders_[1] == "DESC":
                    query += " ORDER BY {0} {1}".format(self.orders_[0],
                                                        self.orders_[1])
                else:
                    raise ValueError(
                        "order_by Second Value should be empty or ASC or DESC but get: '{0}'".
                        format(self.orders_[1]))
        query += ";"

        data = self.exec_query_select(query, self.table_)

        return data



    def exec_query_select(self, query, name):
        #print query
        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(
                    Maapi_dbname, Maapi_user, Maapi_host, Maapi_passwd))
        except:
            raise IOError(
                "Can not open connection with DB {0}".format(Maapi_dbname))
        else:
            table_data_dict = {}
            x = conn.cursor()
            try:
                x.execute(query)
                table_data = x.fetchall()


                if self.columns_var == '*':
                    x.execute(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".
                        format(name))
                    table_names = x.fetchall()

                #print type(table_names)
                    for row_s in range(len(table_data)):
                        sensor_rows = {}
                        i = 0
                        for r_s in table_data[row_s]:
                            sensor_rows[table_names[i][0]] = r_s
                            i += 1
                        table_data_dict[table_data[row_s][0]] = sensor_rows

                else:
                    if self.columns_[1]== "*":
                        self.columns_=list(self.columns_)
                        x.execute(
                            "SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".
                            format(name))
                        table_names_tmp = x.fetchall()
                        table_names = [(self.columns_[0],),]+table_names_tmp
                    else:
                        table_names = self.columns_

                    for row_s in range(len(table_data)):
                        sensor_rows = {}
                        i = 0
                        if isinstance(table_names[i], tuple):
                            for r_s in table_data[row_s]:
                                sensor_rows[table_names[i][0]] = r_s
                                i += 1
                        else:
                            for r_s in table_data[row_s]:
                                sensor_rows[table_names[i]]= r_s
                                i += 1
                        table_data_dict[table_data[row_s][0]] = sensor_rows

            except (Exception, psycopg2.DatabaseError) as error:
                pass

            conn.close()
        return table_data_dict

    @classmethod
    def update_cron(self,file_name,time):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print ("I am unable to connect to the database")
        else:

            #print("time={0}\t file name={1}\t file_location={2}".format(time,file_name,Maapi_location))
            x = conn.cursor()
            x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW(), cron_time_of_exec={1} WHERE cron_file_path ='{2}' and cron_where_exec='{3}'".format(datetime.now(),time,file_name,Maapi_location))

            conn.commit()

            conn.close()


    @classmethod
    def reindex(self,tables):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print ("I am unable to connect to the database")
        else:

            x = conn.cursor()
            for t in tables:
                x.execute("REINDEX TABLE maapi_dev_rom_{0}_values".format(tables[t]['dev_rom_id'].replace("-", "_")))
                #print ("REINDEX TABLE maapi_dev_rom_{0}_values".format(tables[t]['dev_rom_id'].replace("-", "_")))
                conn.commit()
            conn.close()


    def __init__(self):
        self.filters_ = {}
        self.orders_ = {}
        self.columns_ = {}
        self.columns_var = {}
        self.table_ = {}

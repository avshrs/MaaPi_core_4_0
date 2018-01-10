#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 3.1
#                   self.connection with DB
#
##############################################################
import psycopg2
from datetime import datetime, timedelta
from conf.MaaPi_Settings import *

class db(object):
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        x = conn.cursor()
class MaaPiDBConnection(db):

    def __init__(self):
        self.filters_ = {}
        self.orders_ = {}
        self.columns_ = {}
        self.columns_var = {}
        self.table_ = {}
    debug = 0


    @classmethod
    def _debug(self, level, msg):
        if self.debug >= level:
            print("DEBUG MaaPi DB 2  {0} {1}, {2}".format(level, datetime.now(), msg))

    @classmethod
    def insert_data(self,senor_id,value,sensor_type,status):

        self._debug(1,"SENSOR ID ={0}".format(senor_id))
        self._debug(1,"value ={0}".format(value))
        self._debug(1,"sensor_type ={0}".format(sensor_type))
        db.x = db.conn.cursor()
        self._debug(1,"x self.connection cursor")
        db.x.execute("SELECT dev_value, dev_rom_id, dev_collect_values_to_db FROM devices WHERE dev_id='{0}' and dev_status=True".format(senor_id))
        db_data = db.x.fetchone()
        self._debug(1,"get data from devices")
        try:
            db.x.execute("UPDATE devices SET dev_value_old={0} WHERE dev_id='{1}' and dev_status=True".format(db_data[0],senor_id))
            db.conn.commit()
        except:
            pass
        if status is True:
            self._debug(1,"sensor status TRUE")
            """if stst is true, update actual value, date and stat on devices"""
            if value == True:
                db.x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(1,senor_id))
                db.conn.commit()
                if db_data[2]:
                    db.x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,1))
                    db.conn.commit()
                """if dev_collect_values_to_db true - enable write to values table"""
            elif value == False:
                db.x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(0,senor_id))
                db.conn.commit()
                if db_data[2]:
                    db.x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,0))
                    db.conn.commit()
                """if dev_collect_values_to_db true - enable write to values table"""
            else:
                db.x.execute("UPDATE devices SET dev_value={0}, dev_interval_queue = {2}, dev_last_update=NOW(), dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(value,senor_id,False))
                db.conn.commit()

                if db_data[2]:
                    db.x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,value))
                    db.conn.commit()
        else:
            db.x.execute("UPDATE devices SET  dev_interval_queue = {2},dev_value={0},dev_read_error='Error' WHERE dev_id='{1}' and dev_status=True".format(9999,senor_id,False))
            db.conn.commit()


    @classmethod
    def queue(self,dev_id,status):
        db.x = db.conn.cursor()
        self._debug(1,"Queue set {1} ={0}".format(status,dev_id))
        if dev_id == '*':
            self._debug(2,"Queue set {1} = {0} - done ".format(status,dev_id))
            db.x.execute("UPDATE devices SET dev_interval_queue={0} where dev_status=TRUE".format(status))
            db.conn.commit()
        else:
            self._debug(2,"Queue set {1} = {0} - done ".format(status,dev_id))
            db.x.execute("UPDATE devices SET dev_interval_queue={0} where dev_id={1}".format(status,dev_id))
            db.conn.commit()


#    @classmethod
    #def queue_all(self,status):
#        db.x.execute("UPDATE devices SET dev_interval_queue={0} ".format(status))
#        db.conn.commit()


    def columns(self, *args):
        self._debug(2,"columns: {0}".format(args))
        self.columns_ = args
        return self

    def filters_eq(self, **kwargs):
        self._debug(2,"filters_eq: {0}".format(kwargs))
        self.filters_ = kwargs
        return self

    def order_by(self, *args):
        self._debug(2,"order_by: {0}".format(args))
        self.orders_ = args
        return self

    def if_number(self, s):
        self._debug(2,"if_number: {0}".format(s))
        try:
            float(s)
            return True
        except ValueError:
            return False

    def table(self, *args):
        self._debug(2,"table: {0}".format(args))
        if len(args) != 1:
            raise ValueError(
                ".get_table('table name') should only have a table name")
        self.table_ = args[0]
        return self

    def get(self):
        self._debug(2,"get")
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
        db.x = db.conn.cursor()
        table_data_dict = {}
        try:
            db.x.execute(query)
            table_data = db.x.fetchall()
            if self.columns_var == '*':
                db.x.execute(
                    "SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".
                    format(name))
                table_names = db.x.fetchall()

                for row_s in range(len(table_data)):
                    sensor_rows = {}
                    i = 0
                    for r_s in table_data[row_s]:
                        sensor_rows[table_names[i][0]] = r_s
                        i += 1
                    table_data_dict[table_data[row_s][0]] = sensor_rows

            else:
                table_names = self.columns_
                for row_s in range(len(table_data)):
                    sensor_rows = {}
                    i = 0
                    for r_s in table_data[row_s]:
                        sensor_rows[table_names[i]] = r_s
                        i += 1
                    table_data_dict[table_data[row_s][0]] = sensor_rows

        except (Exception, psycopg2.DatabaseError) as error:
            pass

        return table_data_dict

    @classmethod
    def update_cron(self,file_name,time):

        db.x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW(), cron_time_of_exec={1} WHERE cron_file_path ='{2}' and cron_where_exec='{3}'".format(datetime.now(),time,file_name,Maapi_location))

        db.conn.commit()

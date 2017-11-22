#!/usr/bin/python
import MySQLdb
import sys
from lxml import html
import requests
from MaaPi_Settings import *
err="ok"
conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
x = conn.cursor()

x.execute("SELECT COUNT(*) FROM devices WHERE d_status=True AND d_bus_type='www'")
counter = x.fetchone()
x.execute("select d_rom_id from devices where d_status=True AND d_bus_type='www'")
rom_id= x.fetchall()
x.execute("select d_www_url from devices where d_status=True AND d_bus_type='www'")
www_url= x.fetchall()
x.execute("select d_www_class from devices where d_status=True AND d_bus_type='www'")
www_class= x.fetchall()


for i in xrange(1,counter[0]+1):
   try:
      requests.get(www_url[i-1][0])
   except requests.exceptions.ConnectionError as e:
      err=e

   if err=="ok":
      page=requests.get(www_url[i-1][0])
      tree = html.fromstring(page.content)
      distance = tree.xpath(www_class[i-1][0])
      x.execute("INSERT INTO devices_values VALUES (null,(SELECT d_device_id FROM devices WHERE d_rom_id=%s), %s,null, %s,1)",(rom_id[i-1][0],rom_id[i-1][0],distance[0] ))
      conn.commit()
      x.execute("UPDATE devices SET d_value=%s, d_last_update=NOW(), d_read_err=%s WHERE d_rom_id=%s", (distance[0],err, rom_id[i-1][0]))
      conn.commit()
   else:
      x.execute("UPDATE devices SET d_value=%s, d_last_update=NOW(), d_read_err=%s WHERE d_rom_id=%s", (99999,err, rom_id[i-1][0]))
      conn.commit()

conn.close()

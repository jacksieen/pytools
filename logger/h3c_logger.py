#!/bin/env python
# -*- encodiing:utf-8 -*-
import os,sys
import re, datetime, string
import MySQLdb


DB_HOST =            "localhost"
DB_USER =            "root"
DB_PASSWORD =        "root"
DB_NAME =            "database"
TABLE_NAME =         "tables"
TABLE_ERROR =        "tables"

class logpack:
    patt = re.compile(r'\s+')
    default_msg = "Mar 16 12:08:33 E_J28D_3F_E352B_S3 %%10PTVL/5/WARNING(l):- 1 -The link partner of Ethernet1/0/24 may be bad,sending lots of error packets !"
    TIMEFORMAT =                    "%Y/%m/%d-%X"    
    
    def __init__(self, msg=default_msg):
        try:
            self.recvtime =         datetime.datetime.utcnow().strftime(self.TIMEFORMAT)
            log = logpack.patt.split(msg, 6)
            self.devicetime =       log[:3]
            self.devicetime = ' '.join(self.devicetime)
            self.hostname =         log[3]
            self.MLD =              log[4]
            self.info =             log[5]
            self.content =          log[6]
            self.devIP =            ''
            self.module =           ''
            self.level =            ''
            self.digest =           ''
            self.__parse() 
            self.__getip()
        except:
            self.failback()
            exit()

    
    def __parse(self):
        tmp = self.MLD.split('/')
        self.module = tmp[0]
        self.level = tmp[1]
        self.digest = tmp[2].split(':')[0]
        return

    def __getip(self):
        expr = r'\d+(.)\d+(.)\d+(.)\d+'
        pattern = re.compile(expr)
        if pattern.search(self.info):
            self.devIP = pattern.search(self.info).group()
        else:
            self.devIP = pattern.search(self.content).group()

    def save(self):
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
        conn.select_db(DB_NAME)
        curs = conn.cursor()
        sql = 'insert into %s (ReceiveTime, HostName, DeviceIP, DeviceTime, Module, Level, Digest, info, content) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        curs.execute(sql % (TABLE_NAME, self.recvtime, self.hostname, self.devIP, self.devicetime, self.module, self.level, self.digest, self.info, self.content))
        conn.commit()
        curs.close()

    def failback(self):
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
        conn.select_db(DB_NAME)
        curs = conn.cursor()
        sql = 'insert into %s (ReceiveTime, HostName, Message) values ("%s", "%s", "%s")'
        curs.execute(sql % (TABLE_ERROR, self.recvtime, self.hostname, msg))
        conn.commit()
        curs.close()
 
if __name__ == "__main__":
    msg = sys.stdin.readline()
    l = logpack(msg)
    l.save()



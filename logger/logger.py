#!/bin/env python
# -*- encoding:utf-8 -*-

import sys, string
import re, datetime
import MySQLdb

DB_HOST =           "localhost"
DB_USERNAME =       "root"
DB_PASSWORD =       "root"
DB_NAME =           "database"
TABLENAME =         "tables"




class logpack:
    default_msg = "Dec  9 21:15:30 archlinux kernel: [    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009f7ff] usable"
    patt = re.compile(r'\s+')
    TIMEFORMAT =                    "%Y/%m/%d-%X"
    
    def __init__(self, msg=default_msg):
        try:
            self.recvtime =         datetime.datetime.now().strftime(self.TIMEFORMAT)
            log = logpack.patt.split(msg, 5)
            self.devicetime =       log[:3]
            self.hostname =         log[3]
            self.facility =         log[4]
            self.content =          log[5]
        except IndexError:
            self.content = "except logbuf"
        if self.facility == 'kernel:' or 'sudo:':
            self.facility = self.facility.split(':')[0]
            self.pid = '0'
        else:
            try:
                tmp = self.facility.split('[')
                self.facility = tmp[0]
                self.pid = tmp[1].split(']')[0]
            except:
                pass
        self.__formatTime()
    
    def __formatTime(self):
        dtime = self.devicetime[0]+'-'+self.devicetime[1]+'-'+self.devicetime[2]
        dtime = datetime.datetime.strptime(dtime, "%b-%d-%X")
        self.devicetime = dtime.strftime("%m-%d %X")
        return 
    
    def save(self):
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USERNAME, passwd=DB_PASSWORD)
        conn.select_db(DB_NAME)
        curs = conn.cursor()
        sql = 'insert into %s (ReceiveTime, HostName, Facility, Devicetime, content) values ("%s", "%s", "%s", "%s", "%s")'
        curs.execute(sql % (TABLENAME, self.recvtime, self.hostname, self.facility, self.devicetime, self.content))
        conn.commit()
        curs.close()
    

msg = sys.stdin.readline()
l = logpack(msg)
l.save()

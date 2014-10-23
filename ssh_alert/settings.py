# -*- coding:utf-8 -*-
import sys, os

LOG_FILE =          "/var/log/message"
DB_HOST =           "localhost"
DB_NAME =           "db"
DB_TABLE =          "table"
DB_USER =           "user"
DB_PASSWORD =       "upass"

def getpwd():
    pwd = sys.path[0]
    if os.path.isfile(pwd):
        pwd = os.path.dirname(pwd)
    return pwd

ADMIN_EMAIL =    'admin@localhost'
SMTP_SERVER =    'localhost'
SMTP_LOGIN =     'admin@localhost'
SMTP_PASSWD =    'pass'
SMTP_SUBJECT =   'SERVER LOGIN NOTICE'
WORKING_DIR =    getpwd() + '/'
WHITE_LIST =     WORKING_DIR + 'white_list'
ALERT_TEMPLATE = 'User %s has logined %s from %s at %s'

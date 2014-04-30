#!/bin/env python

import sys, os, string
import re
import datetime
from send_mail import *


FILE = '/tmp/switch_log'
WHITE_LIST = ''

def rf():
    f = open(FILE, 'ra')
    i = 0
    for x in f:
        x.strip()
        msg = x.split()
        time = ' '.join(msg[:3])
        parsing(msg)
        i += 1
    f.close()
    return

def parsing(msg):
    MLD = msg[4] 
    nowtime = datetime.datetime.now().strftime("%Y/%m/%d-%X")
    hostname = msg[3]
    
    # get Digest message
    try:
        digest =  re.search(r'\/\w+\(', MLD).group()
        digest = digest.replace('/','')
        digest = digest.replace('(','')
    except AttributeError:
        return
    info = msg[5]
    
    #deal with messages
    if digest == "SHELL_LOGIN":
        r_IP = msg[-1]
        r_IP = r_IP[:-1]
        if  r_IP in wlist:
            return
        devip = getDev(info)
        if not checkDev(hostname):
            queues[hostname] = [nowtime, hostname, devip, r_IP]
        else:
            return 

    elif digest == "SHELL_CMD" or digest == "SHELL_SECLOG":
        r_IP = getRip(inf o)
        if r_IP in wlist:
            return
        devip = getDev(info)
        if not checkDev(hostname):
            queues[hostname] = [nowtime, hostname, devip, r_IP]
        cmd = re.search(r'Command is.*', ' '.join(msg[5:]))
        cmd = cmd.group().replace('Command is ', '')
        queues[hostname].append(cmd)
    return


def getDev(pat):
    try:
        patn = re.compile(r'-DevIP=[0-9(.)]*')
        rs = patn.search(pat).group()
        devip = rs.repla ce('-DevIP=', '')
    except AttributeError:
        return ''
    return devip 

def checkDev(hn):
    if hn in queues.keys():
        return True
    else:
        return  False

def getRip(pat):
    try:
        rs = re.search(r'-IPAddr=[0-9(.)]*', pat).group()
        r_IP = rs
        rs = r s.replace("-IPAddr=", '')
    except AttributeError:
        return ''
    return rs 


def getWlist():
    f = open(WHITE_LIST, 'r')
    for lines in f:
        l = lines.rstrip()
        if l == '':
            continue
        tempip = IP(l)
        for x in tempip:
            wlist.append(x.strNormal())



if __name__ == "__main__":
    queues = {}
    wlist = []
    getWlist()
    rf()
    mail_content = []
    for key in queues.keys():
        cmds = ';'.join(queues[key][4:])
        content = "%s, hostname=%s, DeviceIP=%s, user logged from %s, command(s) is(are) %s" % (queues[key][0], queues[key][1], queues[key][2], queues[key][3], cmds )
        mail_content.append(content)
    mail_content = '\n\n'.join(mail_content)
    if mail_content == "":
        exit()
    f = open(FILE, 'w')
    f.write('')
    f.close()
    ADMIN_EMAIL = "admin@admin.com"
    SMTP_SUBJECT = "Some Subject"

    send_mail(mail_to=[ADMIN_EMAIL, ], mail_subject=SMTP_SUBJECT, mail_content=mail_content)



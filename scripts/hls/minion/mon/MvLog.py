#!/usr/bin/env python
## -*- coding:utf-8 -*-

import os
import sys
import time
import shutil
import datetime
import subprocess

Day = 0
BakPath = '/data/phplogbak/phplog'

def Get_Days_List(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)).replace('-',''))
    return before_n_days

def MoveLog():
    Servers = [ dir for dir in os.listdir(SrcPath) if os.path.isdir(os.path.join(SrcPath,dir)) ]
    for server in Servers:
        serverpath = os.path.join(SrcPath,server)
        for logtype in os.listdir(serverpath):
            logtypepath = os.path.join(serverpath,logtype)
            for logtime in os.listdir(logtypepath):
                logtimepath = os.path.join(logtypepath,logtime)
                mbpath = os.path.join(BakPath,server,logtype,logtime)
                if os.path.exists(mbpath):
                    mbpath = os.path.join(BakPath, server, logtype,logtime+'-'+time.strftime("%Y%m%d_%H%M%S", time.localtime()))
                if logtime not in dates:
                    shutil.move(logtimepath,mbpath)

def MvLogA():
    SrcPath = '/data/game/log'
    Servers = [dir for dir in os.listdir(SrcPath) if os.path.isdir(os.path.join(SrcPath, dir))]
    for server in Servers:
        serverpath = os.path.join(SrcPath, server)
        if not os.path.exists(os.path.join(BakPath,server)):
            mbpath = os.path.join(BakPath,server)
            print(mbpath)
            os.makedirs(mbpath)
        Cmd = r"find %s -type f -name bi.log* -mtime +%s | egrep '^%s.*.log' | xargs -i mv -n {} %s" % (
            serverpath,
            Day,
            serverpath,
            os.path.join(BakPath,server)
        )
        RunCmd = subprocess.Popen(Cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'A8':
        SrcPath = '/data/game/log'
        MvLogA()
    elif len(sys.argv) == 1:
        SrcPath = '/data/game/phplog'
        dates = Get_Days_List(Day)
        MoveLog()

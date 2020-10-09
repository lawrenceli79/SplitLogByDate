# This script split <LogFile> to many <LogFile>_<yyyymmdd>_<n>
# This file assume each line in <LogFile> begin with yyyy-mm-ddTHH:mm:ss

import sys
import os
import re
import time
import datetime

if (len(sys.argv)<=1):
    str = ("Split large log file by date of each line.\n"
            "Usage:\n"
            "   py {} <LogFile> <Options>\n"
            "Options:\n"
            "   /ds=<val>    Number of splits whithin a day (Default is 1)\n"
            .format(os.path.basename(__file__))
    )
    # print ("Split log by date. Assume")
    # print ("<LogFile> <options>")
    # print ("options:")
    # print ("    /ds=<val>    Split")
    print(str)
    sys.exit()

nSplitInDay = 1
strInFile = sys.argv[1]
for i in range(2,len(sys.argv)):
    strOption = sys.argv[i]
    strOptionl = strOption.lower()
    mo = re.match(r"/ds=(\d)+", strOptionl) 
    if(mo):
        nSplitInDay = int(mo.group(1))
        if nSplitInDay==0: nSplitInDay=1

def OutputStatus(dtStart:datetime, i:int, bFinish:bool):
    dtNow = datetime.datetime.now()
    time_delta = (dtNow - dtStart)
    total_seconds = time_delta.total_seconds()
    # minutes = total_seconds/60
    # str = "Line=%d, Elapse(sec)=%s, Speed(lines/s)=%d" % (i, "{:.2f}".format(minutes), i/total_seconds)
    str = "Line=%d, Elapse(sec)=%d, Speed(lines/s)=%d" % (i, total_seconds, i/total_seconds)
    if(bFinish):
        print(str)
        print("End=" + dtNow.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print(str, end="\r")

with open(strInFile, errors='ignore') as fIn:
    dtBegin = datetime.datetime.now()
    print("Start=" + dtBegin.strftime("%Y-%m-%d %H:%M:%S"))
    dtLast = None
    hrDLast = None
    hrSplit = 24 // nSplitInDay
    strOutFile = strInFile + "_0"
    fOut = open(strOutFile, "w")
    for i,line in enumerate(fIn):
        mo = re.match(r"^(\d\d\d\d)[-/](\d\d)[-/](\d\d)[T ](\d\d):(\d\d):(\d\d)", line)
        if(mo!=None):
            y = int(mo.group(1))
            m = int(mo.group(2))
            d = int(mo.group(3))
            hr = int(mo.group(4))
            mn = int(mo.group(5))
            sc = int(mo.group(6))
            dt = datetime.date(y, m, d)
            hrD = hr // hrSplit

            if (dtLast == None or (dtLast != dt or hrDLast != hrD )):
                if(fOut != None) :
                    fOut.close()
                if(nSplitInDay==1):
                    strOutFile = "{}_{}".format(strInFile, dt.strftime("%Y%m%d"))
                else:
                    strOutFile = "{}_{}_{}".format(strInFile, dt.strftime("%Y%m%d"), hrD)
                fOut = open(strOutFile, "w")
                dtLast = dt
                hrDLast = hrD

        if(i%1000==0):
            OutputStatus(dtBegin, i, False)
        fOut.write(line)

    fOut.close()
    OutputStatus(dtBegin, i, True)

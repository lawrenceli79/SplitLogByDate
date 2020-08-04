# This script split <LogFile> to many <LogFile>_<yyyymmdd>
# This file assume each line in <LogFile> begin with yyyy-mm-dd

import sys
import os
import re
import time
import datetime

if (len(sys.argv)<=1):
    print ("<LogFile>")
    sys.exit()

strInFile = sys.argv[1]

with open(strInFile, errors='ignore') as fIn:
    dtBegin = datetime.datetime.now()
    print("Start=" + dtBegin.strftime("%Y-%m-%d %H:%M:%S"))
    dtLast = None
    strOutFile = strInFile + "_0"
    fOut = open(strOutFile, "w")
    for i,line in enumerate(fIn):
        mo = re.match(r"^(\d\d\d\d)[-/](\d\d)[-/](\d\d)", line)
        if(mo!=None):
            y = int(mo.group(1))
            m = int(mo.group(2))
            d = int(mo.group(3))
            dt = datetime.date(y, m, d)

            if (dtLast == None or dtLast != dt):
                if(fOut != None) :
                    fOut.close()
                strOutFile = strInFile + "_" + dt.strftime("%Y%m%d")
                fOut = open(strOutFile, "w")
                dtLast = dt

        if(i%1000==0):
            print("Processing Line " + str(i), end="\r")
        fOut.write(line)

    fOut.close()
    print("Finished Line " + str(i))
    dtEnd = datetime.datetime.now()
    time_delta = (dtEnd - dtBegin)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    str = "End=%s, Elapse(min)=%s, Speed(lines/s)=%d" % (dtEnd.strftime("%Y-%m-%d %H:%M:%S"), "{:.2f}".format(minutes), i/total_seconds)
    print(str)

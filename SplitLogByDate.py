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

with open(strInFile) as fIn:
    dtLast = None
    strOutFile = strInFile + "_0"
    fOut = open(strOutFile, "w")
    for line in fIn:
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

        fOut.write(line)

    fOut.close()
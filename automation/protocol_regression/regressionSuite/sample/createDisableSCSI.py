import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, executeCmd
config = configFile(sys.argv);
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python createDisableSCSI.py config.txt nodeIP nodePassword outputfile"
    exit()
IP = sys.argv[2]
passwd = sys.argv[3]
outputfile = sys.argv[4]

routput = getControllerInfo(IP, passwd, "touch /etc/disablescsi", outputfile)


import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, resultCollection, getoutput, getControllerInfo, createSFTPConnection, putFileToController

IP="ESXIP"
passwd="ESXPASSWORD"


cmd = getControllerInfo(IP, passwd,"mkdir autofolder","autofolder.txt")
print cmd
output = putFileToController(IP, passwd, "temp/createvml.sh", "/autofolder/createvml.sh")
print output
output = putFileToController(IP, passwd, "tsmlist", "/autofolder/tsmlist")
print output
cmd = getControllerInfo(IP, passwd,"sh -x /autofolder/createvml.sh","esx.txt")
print cmd



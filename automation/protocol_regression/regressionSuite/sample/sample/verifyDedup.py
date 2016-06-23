import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, executeCmd
config = configFile(sys.argv);
if len(sys.argv) < 5:
    print "Argument is not correct.. Correct way as below"
    print "python verifyDedup.py config.txt nodeIP nodePassword PoolName"
    exit()
IP = sys.argv[2]
passwd = sys.argv[3]
poolName = sys.argv[4]
print "IP = "+IP
print "Password = "+passwd
print "Pool = "+poolName

def checkDedup(ip,passwd,PoolName):
    startTime = ctime()
    executeCmd("python enableDedup.py %s" %(sys.argv[1]))
    executeCmd("python copyData.py %s %s %s" %(sys.argv[1], PoolName, 'testfile'))
    time.sleep(30)
    dedupRatio1 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
    for x in range (1, 5): 
        executeCmd("python copyData.py %s %s %s" %(sys.argv[1], PoolName, 'testfile%s'%(x)))
    time.sleep(30)
    dedupRatio2 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
    print dedupRatio1 
    print dedupRatio2
    if float(dedupRatio2.split('x')[0]) > float(dedupRatio1.split('x')[0]):
        return ("PASSED", "")
    else:
        return ("FAILED", "")
output=checkDedup(IP, passwd, poolName);
endTime = ctime()
resultCollection("Verification of Dedup Functionality", output,startTime,endTime)

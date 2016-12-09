import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, executeCmd
config = configFile(sys.argv);
if len(sys.argv) < 5:
    print "Argument is not correct.. Correct way as below"
    print "python verifyMetaSize.py config.txt nodeIP nodePassword PoolName"
    exit()
IP = sys.argv[2]
passwd = sys.argv[3]
poolName = sys.argv[4]
print "IP = "+IP
print "Password = "+passwd
print "Pool = "+poolName
startTime = ctime()
def checkMetaSize(ip,passwd,PoolName):
    type="meta"
    executeCmd("python enableDedup.py");
    executeCmd("python copyData.py %s %s %s" %(sys.argv[1], PoolName, 'testfile'))
    time.sleep(60)
    poolUsedSize1 = getControllerInfo(ip, passwd,"zpool iostat -v %s | grep %s | awk '{print $2}'" %(PoolName, PoolName),"output.txt")
    metaUsedSize1 = getControllerInfo(ip, passwd,"zpool iostat -v %s | grep -A 1 %s | grep raidz1 | awk '{print $2}'" %(PoolName, type),"output.txt")
    print poolUsedSize1.split('M')[0]
    print metaUsedSize1.split('M')[0]
    #for x in range (1, 40): 
    for x in range (1, 11): 
        executeCmd("python copyData.py %s %s %s" %(sys.argv[1], PoolName, 'testfile%s'%(x)))
    time.sleep(60)
    poolUsedSize2 = getControllerInfo(ip, passwd,"zpool iostat -v %s | grep %s | awk '{print $2}'" %(PoolName, PoolName),"output.txt")
    metaUsedSize2 = getControllerInfo(ip, passwd,"zpool iostat -v %s | grep -A 1 %s | grep raidz1 | awk '{print $2}'" %(PoolName, type),"output.txt")
    print poolUsedSize2.split('M')[0]
    print metaUsedSize2.split('M')[0]

    if ((float(poolUsedSize1.split('M')[0]) == float(poolUsedSize2.split('M')[0])) and (float(metaUsedSize2.split('M')[0]) > float(metaUsedSize1.split('M')[0]))):
        return ("PASSED", "")
    else:
        return ("FAILED", "")

output=checkMetaSize(IP, passwd, poolName)
endTime = ctime()
resultCollection("Verification of Meta Size", output,startTime,endTime)

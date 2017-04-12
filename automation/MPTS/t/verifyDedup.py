import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
ip = "20.10.68.20"
def executeCmd(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    if rco != 0:
        return "FAILED", str(errors)
    return "PASSED", ""; 

def filesave(loglocation,permission,content):
        f=open(loglocation,permission)
        f.write(content)
        f.close()
        return;

def getoutput(command):
    print command  
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    try:
       output = ldata
    except IndexError:
       output = 'null'
    return output

def checkDedup(ip,passwd,PoolName):
    output1 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
    executeCmd("python enableDedup.py");
    executeCmd("python copyData.py %s %s" %(PoolName,testfile1))
    executeCmd("python copyData.py %s %s" %(PoolName,testfile2))
    executeCmd("python copyData.py %s %s" %(PoolName,testfile3))
    output2 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
    if float(output2.split('x')[0]) > float(output1.split('x')[0]):
        return "PASSED"
    else:
        returned "FAILED"
print checkDedup("20.10.68.20","test","Pool1");

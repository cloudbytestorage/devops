import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, executeCmd, getControllerInfoAppend
config = configFile(sys.argv);
if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print "python arcStats.py config.txt nodeIP nodePassword sleeptime volumenames seperated by space"
    exit()
IP = sys.argv[2]
passwd = sys.argv[3]
interval= float(sys.argv[4])

poolName=[]
#for y in range(5,len(sys.argv)):
    #poolName.appen(sys.argv[y])
x=0
while True:
    
    f=open("o1.txt","a")
    f.write("\n ************************************************\n")
    f.close()

    print "**********************************************************************************"
    cmd1 = getControllerInfoAppend(IP, passwd, "date" , "o1.txt")
    print cmd1

    for y  in range(5,len(sys.argv)):
   
        poolName.append(sys.argv[y])
        f=open("o1.txt","a")
        f.write("Volume Name = ")
        f.write(poolName[x])            
        f.write("\n")
        f.close()
       
        print "\tARC stats of "+poolName[x]
        print " "

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep c_max | grep -w %s" %(poolName[x]) , "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep arcstats.size | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep arcstats.hits | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep arcstats.misses | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        print "\n\tL2ARC stats of "+poolName[x]
        print " "

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep l2_size | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep l2_hits | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep l2_misses | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1

        cmd1 = getControllerInfoAppend(IP, passwd, "sysctl -a | grep l2_feeds | grep -w %s" %(poolName[x]), "o1.txt")
        print cmd1
        
        x=x+1

    time.sleep(interval)




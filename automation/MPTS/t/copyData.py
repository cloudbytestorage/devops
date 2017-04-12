import json
import requests
import md5
import fileinput
import subprocess
import time
import sys
def executeCmd(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    if rco != 0:
        return "FAILED", str(errors)
    return "PASSED", ""; 

def resultCollection(testcase,value):
    f=open("results/result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.write("\n")
    return;

#### Function(s) Declartion Ends

config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)

########### TestCase Execution Starts.. 

print sys.argv[1];

###NFS
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    if config['volPoolName%d' %(x)] == sys.argv[1]:
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
        ######Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp %s mount/%s' %(sys.argv[2], config['volMountpoint%d' %(x)]))
            print "yes"
        else:
            print "no"
        break ;


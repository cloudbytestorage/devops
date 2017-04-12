import json
import sys
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput
config = configFile(sys.argv);

########### TestCase Execution Starts.. 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 2:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python executionDisableNFS.py config.txt " + bcolors.ENDC
    exit()

filename = "testfile"; 
# exit()

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')


for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    startTime = ctime()
    executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))

    ### Mount
    executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        
    if output[0] == "PASSED":
        endTime = ctime()
        resultCollection("Able to mount NFS Disable volume %s so test case for disable nfs is :" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)
        executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))
    else:
        endTime = ctime()
        resultCollection("Not able to mount NFS Disabled volume %s so test case for disable nfs is : " %(config['volDatasetname%d' %(x)]), ["PASSED", ""], startTime, endTime)

#executeCmd('umount -a -t cifs -l')
#executeCmd('umount -a')

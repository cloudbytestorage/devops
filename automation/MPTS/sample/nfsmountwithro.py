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
    print bcolors.WARNING + "python nfsmountwithro.py config.txt " + bcolors.ENDC
    exit()

filename = "NFSVolume.py"; 

# exit()

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')


for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
    startTime = ctime()

    ### Mount
    output2 = executeCmd('mount -t nfs -o vers=3 -r %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    output = executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        
    if output[0] == "PASSED":
        out2 = executeCmd('cp %s  mount/%s' %(filename, config['volMountpoint%d' %(x)]))
        if out2[0] == 'FAILED':
            endTime = ctime()
            resultCollection("Not able to write on volume %s so test case for mount with ro option is:" %(config['volDatasetname%d' %(x)]), ["PASSED", ""], startTime, endTime)
        else:
            endTime = ctime()
            resultCollection("Able to write on volume %s so test case for mount with ro option is:" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)

        executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))
    else:
        endtime = ctime()
        resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output2, startTime, endTime)


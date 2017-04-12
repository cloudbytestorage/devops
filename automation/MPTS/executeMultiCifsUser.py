import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput

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
    print bcolors.WARNING + "python executeMultiCifsUser.py config.txt" + bcolors.ENDC
    exit()

config = configFile(sys.argv);

### CIFS
for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    startTime = ctime()
    executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
    ### Mount with multiple users
    i = 1;
    for i in range(1, 3):
        user = "%suser%d" %(config['volCifsAccountName%d' %(x)], i)
        password = user
        out = executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%s -o password=%s' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], user, password))
        
        ### 
        if out[0] == "PASSED": 
            print "volume %s mounted successfully with user %s" %(config['volCifsMountpoint%d' %(x)], user)
            endTime = ctime()
            resultCollection("Mount of CIFS Volume %s with user %s is:" %(config['volCifsDatasetname%d' %(x)], user), ['PASSED', ''], startTime, endTime)
            executeCmd('umount mount/%s' %(config['volCifsMountpoint%d' %(x)]))
            time.sleep(2)
                
        else:
            endTime = ctime()
            print "mount failed for volume %s with user %s" %(config['volCifsMountpoint%d' %(x)], user)
            resultCollection("Mount of CIFS Volume %s with user %s is:" %(config['volCifsDatasetname%d' %(x)], user), ['FAILED', ''], startTime, endTime)

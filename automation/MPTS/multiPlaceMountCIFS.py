import json
import sys
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput, mountCIFS

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
    print bcolors.WARNING + "python multiPlaceMountCIFS.py config.txt copyfile1(Optional) copyfile2(Optional) copyfile3(Optional) " + bcolors.ENDC
    exit()

config = configFile(sys.argv);
filename1 = "copy1.txt"; filename2 = "copy2.txt"; filename3 = "copy3.txt";


if len(sys.argv) == 3:
    filename1 = sys.argv[2]
if len(sys.argv) == 4:
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
if len(sys.argv) == 5:
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
    filename3 = sys.argv[4]

for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    startTime = ctime()
    
    executeCmd('mkdir -p mount/cifs1/%s' %(config['volCifsMountpoint%d' %(x)]))
    executeCmd('mkdir -p mount/cifs2/%s' %(config['volCifsMountpoint%d' %(x)]))
    executeCmd('mkdir -p mount/cifs3/%s' %(config['volCifsMountpoint%d' %(x)]))
    
    
    ### Mount
    executeCmd(' mount -t cifs //%s/%s mount/cifs1/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))

    executeCmd(' mount -t cifs //%s/%s mount/cifs2/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))

    executeCmd(' mount -t cifs //%s/%s mount/cifs3/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))

    mountCifs1 = executeCmd('mount | grep mount/cifs1/%s' %(config['volCifsMountpoint%d' %(x)]))
    mountCifs2 = executeCmd('mount | grep mount/cifs2/%s' %(config['volCifsMountpoint%d' %(x)]))
    mountCifs3 = executeCmd('mount | grep mount/cifs3/%s' %(config['volCifsMountpoint%d' %(x)]))

    if mountCifs1[0] == 'PASSED' and mountCifs2[0] == 'PASSED' and mountCifs3[0] == 'PASSED':
        executeCmd('cp %s  mount/cifs1/%s' %(filename1, config['volCifsMountpoint%d' %(x)]))
        executeCmd('cp %s  mount/cifs2/%s' %(filename2, config['volCifsMountpoint%d' %(x)]))
        executeCmd('cp %s  mount/cifs3/%s' %(filename3, config['volCifsMountpoint%d' %(x)]))
        mountres1 = executeCmd('ls mount/cifs1/%s | grep %s' %(config['volCifsMountpoint%d' %(x)], filename1))
        mountres2 = executeCmd('ls mount/cifs1/%s | grep %s' %(config['volCifsMountpoint%d' %(x)], filename2))
        mountres3 = executeCmd('ls mount/cifs1/%s | grep %s' %(config['volCifsMountpoint%d' %(x)], filename3))
        endTime = ctime()
        if mountres1[0] == 'PASSED' and mountres2[0] == 'PASSED' and mountres3[0] == 'PASSED':
            resultCollection("Mount is passed of volume \"%s\", and able to see file copied by other clients : " %(config['volCifsMountpoint%d' %(x)]), ['PASSED', ''], startTime, endTime)
        else:
            resultCollection("Mount is passed of volume \"%s\", but not able to see files copied by other clients : " %(config['volCifsMountpoint%d' %(x)]), ['FAILED', ''], startTime, endTime)
    else:
        endTime = ctime()
        resultCollection("Mount of NFS Volume \"%s\" at multiple places test case is : " %(config['volCifsMountpoint%d' %(x)]), ['FAILED', ''], startTime, endTime)
    
    ### umount
    executeCmd('umount mount/cifs1/%s' %(config['volCifsMountpoint%d' %(x)]))
    executeCmd('umount mount/cifs2/%s' %(config['volCifsMountpoint%d' %(x)]))
    executeCmd('umount mount/cifs3/%s' %(config['volCifsMountpoint%d' %(x)]))

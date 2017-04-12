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
    print bcolors.WARNING + "python multiplacemount.py config.txt copyfile1(Optional) copyfile2(Optional) copyfile3(Optional) " + bcolors.ENDC
    exit()

filename1 = "copy1.py"; filename2 = "copy2.py"; filename3 = "copy3.py";


if len(sys.argv) == 3:
    filename1 = sys.argv[2]
if len(sys.argv) == 4:
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
if len(sys.argv) == 5:
    filename1 = sys.argv[2]
    filename2 = sys.argv[3]
    filename3 = sys.argv[4]


# exit()

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')


for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    startTime = ctime()
    executeCmd('mkdir -p mount/nfs1/%s' %(config['volMountpoint%d' %(x)]))
    executeCmd('mkdir -p mount/nfs2/%s' %(config['volMountpoint%d' %(x)]))
    executeCmd('mkdir -p mount/nfs3/%s' %(config['volMountpoint%d' %(x)]))
    
    ### Mount
    executeCmd('mount -t nfs  %s:/%s mount/nfs1/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    executeCmd('mount -t nfs  %s:/%s mount/nfs2/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    executeCmd('mount -t nfs  %s:/%s mount/nfs3/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    out1 = executeCmd('mount | grep mount/nfs1/%s' %(config['volMountpoint%d' %(x)]))
    out2 = executeCmd('mount | grep mount/nfs2/%s' %(config['volMountpoint%d' %(x)]))
    out3 = executeCmd('mount | grep mount/nfs3/%s' %(config['volMountpoint%d' %(x)]))
    #endTime= ctime
    #resultCollection("Mount of NFS Volume %s at first place is: " %(config['volDatasetname%d' %(x)]), out1, startTime, endTime)
    #resultCollection("Mount of NFS Volume %s at second place is: " %(config['volDatasetname%d' %(x)]), out2, startTime, endTime)
    #resultCollection("Mount of NFS Volume %s at third place is: " %(config['volDatasetname%d' %(x)]), out3, startTime, endTime)

    if out1[0] == 'PASSED' and out2[0] == 'PASSED' and out3[0] == 'PASSED':
        executeCmd('cp %s  mount/nfs1/%s' %(filename1, config['volMountpoint%d' %(x)]))
        executeCmd('cp %s  mount/nfs2/%s' %(filename2, config['volMountpoint%d' %(x)]))
        executeCmd('cp %s  mount/nfs3/%s' %(filename3, config['volMountpoint%d' %(x)]))
        mount1res1 = executeCmd('ls mount/nfs1/%s | grep %s' %(config['volMountpoint%d' %(x)], filename1))
        mount1res2 = executeCmd('ls mount/nfs1/%s | grep %s' %(config['volMountpoint%d' %(x)], filename2))
        mount1res3 = executeCmd('ls mount/nfs1/%s | grep %s' %(config['volMountpoint%d' %(x)], filename3))
        if mount1res1[0] == 'PASSED' and mount1res2[0] == 'PASSED' and mount1res3[0] == 'PASSED':
            endTime = ctime()
            resultCollection("Mount of NFS Volume %s at multiple places test case is : " %(config['volDatasetname%d' %(x)]), ['PASSED', ''], startTime, endTime)
        else:
            endTime = ctime()
            resultCollection("Mount of NFS Volume %s at multiple places test case is : " %(config['volDatasetname%d' %(x)]), ['FAILED', ''], startTime, endTime)

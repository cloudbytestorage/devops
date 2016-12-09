import json
import requests
import md5
import fileinput
import subprocess
import time

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
    f=open("results/regression_result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.write("\n")
    return;

#### Function(s) Declartion Ends

config = {}
with open('regression_config.txt') as cfg:
  config = json.load(cfg)

########### TestCase Execution Starts.. 

###NFS
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
    ######Mount
    executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
    resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
    #######Copy
    if output[0] == "PASSED":
        executeCmd('cp testfile  mount/%s' %(config['volMountpoint%d' %(x)]))
        output=executeCmd('diff testfile mount/%s' %(config['volMountpoint%d' %(x)]))
        resultCollection("Creation of File on NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
    else:
        resultCollection("Further Execution of TCs Skipped on NFS Volume %s" %(config['volDatasetname%d' %(x)]), ('Due to Mount Failed', ' ')) 


###ISCSI
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    ######Discovery 
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    ######Login to ISCSI
    output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --login | grep Login' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
    resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
    
    ######Copy
    if output[0] == "PASSED":
        device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
        device2 = (device[0].split('\n'))[0]
        executeCmd('fdisk /dev/%s' %(device2))
        executeCmd('mkfs.ext3 /dev/%s1' %(device2))
        executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
        executeCmd('cp testfile  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        output=executeCmd('diff testfile mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        resultCollection("Creation of File on ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
        executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        ######Logout to ISCSI
        output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --logout | grep Logout' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
        resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
    else:
        resultCollection("Further Execution of TCs Skipped on iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' ')) 

###CIFS
for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
    ######Mount
    executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
    output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))
    resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output)
    #######Copy
    if output[0] == "PASSED":
        executeCmd('cp testfile  mount/%s' %(config['volCifsMountpoint%d' %(x)]))
        output=executeCmd('diff testfile mount/%s' %(config['volCifsMountpoint%d' %(x)]))
        resultCollection("Creation of File on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output)
    else:
        resultCollection("Further Execution of TCs Skipped on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), ('Due to Mount Failed', ' ')) 



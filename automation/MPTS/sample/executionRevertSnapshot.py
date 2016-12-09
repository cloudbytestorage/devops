import json
import sys
import fileinput
from time import ctime
import time
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend, getoutput


###
# Provide configuration file storage protocol as parameter
###

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if len(sys.argv) < 3:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python executionRevertSnapshot.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> file1(optional) file2(Optional)" + bcolors.ENDC
    exit()

config = configFile(sys.argv);

if sys.argv[2].lower() == "nfs":
    nfsFlag = 1
elif sys.argv[2].lower() == "cifs":
    cifsFlag = 1
elif sys.argv[2].lower() == "iscsi":
    iscsiFlag = 1
elif sys.argv[2].lower() == "fc":
    fcFlag = 1
elif sys.argv[2].lower() == "all":
    allFlag = 1
else:
    print bcolors.WARNING + "python executionRevertSnapshot.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> file1(optional) file2(Optional)" + bcolors.ENDC
    exit()

file1 = "testfile"; file2 = None; file2_check = 0;
parameters = len(sys.argv)

if parameters == 4:
    file1 = sys.argv[3]
elif parameters == 5:
    file1 = sys.argv[3]
    file2 = sys.argv[4]
    file2_check = 1
else:
    print 'Please provide correct argments as follows...'
    print 'python executionRevertSnapshot.py config.txt <protocol>(nfs/cifs/iscsi/all) file1(optional) file2(optional)'


for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --logout | grep Logout' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))

### CIFS
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))

        ### Mount
        executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))

        ### Checking for reverting snapshot
        if output[0] == "PASSED":

            ### file1 should be present in mounted directory
            filepresent = executeCmd('ls mount/%s %s' %(config['volCifsMountpoint%d' %(x)], file1))
            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['volCifsMountpoint%d' %(x)], file1, file1))
            chksumresult = executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(file1, file1))
            endTime = ctime()
            resultCollection('md5sum result of file \'%s\' on volume %s is :' %(file1, config['volCifsDatasetname%d' %(x)]), chksumresult, startTime, endTime)
            
            # The same file executionRevertSnapshot.py will be used for "Data check" in Cloned dataset 
            # So there is no need to check for second file that's why file2_check is there
            
            ### file2 should not be present in mounted directory
            if file2_check:
                filenotpresent = executeCmdNegative('ls mount/%s | grep %s' %(config['volCifsMountpoint%d' %(x)], file2))
                endTime = ctime()
                resultCollection('Result for file \'%s\' should not exit is: ' %(file2), filenotpresent, startTime, endTime)
        else:
            endTime = ctime()
            resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output, startTime, endTime)

### NFS
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))

        ### Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))

        ### Checking for reverting snapshot
        if output[0] == "PASSED":

            ### file1 should be present in mounted directory
            filepresent = executeCmd('ls mount/%s %s' %(config['volMountpoint%d' %(x)], file1))
            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['volMountpoint%d' %(x)], file1, file1))
            chksumresult = executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(file1, file1))
            endTime = ctime()
            resultCollection('md5sum result of file \'%s\' on volume %s is :' %(file1, config['volDatasetname%d' %(x)]), chksumresult, startTime, endTime)
            
            ### file2 should not be present in mounted directory
            if file2_check:
                filenotpresent = executeCmdNegative('ls mount/%s | grep %s' %(config['volMountpoint%d' %(x)], file2))
                endTime = ctime()
                resultCollection('Result for file \'%s\' should not exit is: ' %(file2), filenotpresent, startTime, endTime)
            
            executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))
        else:
            endTime = ctime()
            resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output, startTime, endTime)

### ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))

        ### Discovery 
        executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
        grepforiSCSIvol = (config['voliSCSIMountpoint%d' %(x)])
        grepforiSCSIvol = str(grepforiSCSIvol.split('_')[0]) + '%d' %(x)
        iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)], config['voliSCSIMountpoint%d' %(x)]))
        print iqnname
        if iqnname==[]:
            print "no iscsi volumes discovered on the client"
            endTime = ctime()
            resultCollection("no iscsi volumes discovered on the client",["FAILED",""], startTime, endTime)
        else:
            ### Login to ISCSI
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            print output[0]
            time.sleep(5)

            ### Checking for ISCSI login
            if output[0] == "PASSED":
                device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                device2 = (device[0].split('\n'))[0]
                mountOutput = executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                out2 = executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                
                ### Checking for reverting snapshot
                if out2[0] == "PASSED":

                    ### file1 should be present in mounted directory
                    filepresent = executeCmd('ls mount/%s %s' %(config['voliSCSIMountpoint%d' %(x)], file1))
                    executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['voliSCSIMountpoint%d' %(x)], file1, file1))
                    chksumresult = executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(file1, file1))
                    endTime = ctime()
                    resultCollection('md5sum result of file \'%s\' on volume %s is: ' %(file1, config['voliSCSIDatasetname%d' %(x)]), chksumresult, startTime, endTime)
                    
                    ### file2 should not be present in mounted directory
                    if file2_check:
                        filenotpresent = executeCmdNegative('ls mount/%s | grep %s' %(config['voliSCSIMountpoint%d' %(x)], file2))
                        endTime = ctime()
                        resultCollection('Result for file \'%s\' should not exit is: ' %(file2), filenotpresent, startTime, endTime)

                    executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                else:
                    endTime = ctime()
                    resultCollection("Mount of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), mountOutput, startTime, endTime)
                
                out3 = executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            else:
                endTime = ctime()
                resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)





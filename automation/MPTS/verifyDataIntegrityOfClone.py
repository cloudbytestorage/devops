import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput, sendrequest, filesave
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
########### TestCase Execution Starts.. 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
### Condition for parameters, those can not be less than 4
if len(sys.argv) < 4:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python verifyDataIntegrityOfClone.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> Number_of_Clones Prefix_name_For_Clone(Optional) filename_for_for_check_data_Integrity(optional)" + bcolors.ENDC
    exit()
### Reading configuration file
config = configFile(sys.argv);
prefixName = ''
No_of_Clones = 0
### Checking for protocols
if sys.argv[2].lower() == "nfs":
    nfsFlag = 1
elif sys.argv[2].lower() == "cifs":
    cifsFlag = 1
elif sys.argv[2].lower() == "fc":
    fcFlag = 1
elif sys.argv[2].lower() == "iscsi":
    iscsiFlag = 1
elif sys.argv[2].lower() == "all":
    allFlag = 1
else:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python verifyDataIntegrityOfClone.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> Number_of_Clones Prefix_name_For_Clone(Optional) filename_for_for_check_data_Integrity(optional)" + bcolors.ENDC
    exit()
filename = "testfile";
### Validating parameters
if len(sys.argv) == 4:
    No_of_Clones = sys.argv[3]
    executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
elif len(sys.argv) == 5:
    No_of_Clones = sys.argv[3]
    prefixName = sys.argv[4]
    executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
elif len(sys.argv) == 6:
    No_of_Clones = sys.argv[3]
    prefixName = sys.argv[4]
    filename = sys.argv[5]
    executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
else:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python verifyDataIntegrityOfClone.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> Number_of_Clones Prefix_name_For_Clone(Optional) filename_for_for_check_data_Integrity(optional)" + bcolors.ENDC
    exit()
### Logout iscsi LUN, those are already login
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
        continue
    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
### Its comman url for all the api calls 
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
### command for list filesystem
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

### NFS protocol
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        for i in range(1, int(No_of_Clones)+1):
            cloneName = prefixName + '%s' %(config['volDatasetname%d' %(x)]) + '%d' %(i)
            for filesystem in filesystems:
                filesystem_id = None
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    if filesystem_id is not None:
                        executeCmd('mkdir -p mount/%s' %(cloneName))
                        ### Mount
                        out = executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], cloneName, cloneName))
                        ### Check data Integrity of clone dataset 
                        if out[0] == "PASSED":
                            print "NFS Clone dataset %s mounted successfully" %(cloneName)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(cloneName, filename, filename))
                            diffoutput = executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                            endTime = ctime()
                            resultCollection("Checksum result on NFS Clone dataset %s is:" %(cloneName), diffoutput, startTime, endTime)
                            executeCmd('umount  mount/%s' %(cloneName))
                        else:
                            endTime = ctime()
                            print "Mount failed for NFS Clone dataset %s" %(cloneName)
                            resultCollection("Further Execution of TCs Skipped on NFS Clone dataset %s" %(cloneName), ('Due to Mount Failed', ' '), startTime, endTime)
                    else:
                        endTime = ctime()
                        print 'not able to take filesystem id'
                        resultCollection("Not able to get ID of NFS Clone dataset %s:" %(cloneName), ['FAILED', ''], startTime, endTime)

### ISCSI protocol
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        for i in range(1, int(No_of_Clones)+1):
            cloneName = prefixName + '%s' %(config['voliSCSIDatasetname%d' %(x)]) + '%d' %(i)
            for filesystem in filesystems:
                filesystem_id = None
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    if filesystem_id is not None:
                        ### trying to logout unnecessary iscsi LUNs
                        executeCmd('iscsiadm -m node -u')
                        executeCmd('mkdir -p mount/%s' %(cloneName))
                        ### Discovery 
                        iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)], cloneName))
                        print iqnname
                        if iqnname==[]:
                            print "no iscsi volumes discovered on the client"
                            endTime = ctime()
                            resultCollection("No iscsi volumes discovered on the client",["FAILED",""], startTime, endTime)
                            continue
                        ### Login to ISCSI
                        output = executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                        print output[0]
                        time.sleep(5)
                        ### Check for data integrity
                        if output[0] == "PASSED":
                            device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                            device2 = (device[0].split('\n'))[0]
                            ### mount
                            mountOutput = executeCmd('mount /dev/%s1  mount/%s' %(device2, cloneName))
                            if mountOutput[0] == "PASSED":
                                print "ISCSI Clone dataset %s mounted successfully" %(cloneName)
                                executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(cloneName, filename, filename))
                                diffoutput = executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                                endTime = ctime()
                                resultCollection("Checksum result on iSCSI Clone dataset %s is:" %(cloneName), diffoutput, startTime, endTime)
                                executeCmd('umount  mount/%s' %(cloneName))
                            else:
                                print "mount failed for ISCSI Clone dataset %s" %(cloneName)
                                endTime = ctime()
                                resultCollection("Mount of iSCSI Clone %s" %(cloneName), mountOutput, startTime, endTime)
                            ### Logout to ISCSI
                            output = executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                            if output == "FAILED":
                                endTime = ctime()
                                #resultCollection("Logout of iSCSI Clone dataset %s" %(cloneName), output, startTime, endTime)
                                print 'Logout of iSCSI dataset %s' %(cloneName)
                        else:
                            endTime = ctime()
                            resultCollection("Further Execution of TCs Skipped on iSCSI Clone dataset %s" %(cloneName), ('Due to Login Failed', ' '), startTime, endTime)

### CIFS protocol
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        for i in range(1, int(No_of_Clones)+1):
            cloneName = prefixName + '%s' %(config['volCifsDatasetname%d' %(x)]) + '%d' %(i)
            print cloneName
            for filesystem in filesystems:
                filesystem_id = None
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    if filesystem_id is not None:
                        executeCmd('mkdir -p mount/%s' %(cloneName))
                        ### Mount
                        out = executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], cloneName, cloneName, config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
                        ### Check data Integrity of clone dataset
                        if out[0] == "PASSED":
                            print "CIFS Clone dataset %s mounted successfully" %(cloneName)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(cloneName, filename, filename))
                            diffoutput=executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                            endTime = ctime()
                            resultCollection("Checksum result on CIFS Clone dataset %s is:" %(cloneName), diffoutput, startTime, endTime)
                            outUmount = executeCmd('umount  mount/%s' %(cloneName))
                            print outUmount[0]
                        else:
                            endTime = ctime()
                            print "mount failed for CIFS Clone dataset %s" %(cloneName)
                            resultCollection("Further Execution of TCs Skipped on CIFS Clone dataset %s" %(cloneName), ('Due to Mount Failed', ' '), startTime, endTime) 
                    else:
                        endTime = ctime()
                        print 'Not able to take filesystem id'
                        resultCollection("Not able to get ID of CIFS Clone dataset %s:" %(cloneName), ['FAILED', ''], startTime, endTime)

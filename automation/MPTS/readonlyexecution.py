import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput
config = configFile(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
########### TestCase Execution Starts.. 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 3:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python execution.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> <copy/delete/create>(optional) filename_for_copy(optional)" + bcolors.ENDC
    exit()

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
    print "Argument is not correct.. Correct way as below"
    print "python execution.py config.txt NFS"
    print "python execution.py config.txt NFS filename"
    print "python execution.py config.txt CIFS filename"
    print "python execution.py config.txt ISCSI filename"
    print "python execution.py config.txt ALL filename"
    print "python execution.py config.txt NFS CIFS filename -- This is not valid"
    print "python execution.py config.txt filename NFS CIFS  -- This is not valid"
    exit()

filename = "testfile"; write_mkfs = 0; copy = 0; delete = 0; 

if len(sys.argv) == 3:
    write_mkfs = 1
    copy = 1
    executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
elif len(sys.argv) == 4:
    if sys.argv[3] == 'create':
        write_mkfs = 1
        copy = 1
        executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
    elif sys.argv[3] == 'copy':
        copy = 1
        executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
    elif sys.argv[3] == 'delete':
        delete = 1
    else:
        print bcolors.FAIL + "Fourth element should be copy or delete or create" + bcolors.ENDC
        exit()
elif len(sys.argv) == 5:
    filename= sys.argv[4]
    if sys.argv[3] == 'create':
        write_mkfs = 1
        copy = 1
        executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
    elif sys.argv[3] == 'copy':
        copy = 1
        executeCmd('md5sum %s  | awk \'{print $1}\' > mount/%s_md5sum'%(filename, filename))
    elif sys.argv[3] == 'delete':
        delete = 1
    else:
        print  bcolors.FAIL + "Fourth element should be copy or delete or create" + bcolors.ENDC
        exit()
else:
    print  bcolors.FAIL + "Only five arguments are allowed, Please read the help" + bcolors.ENDC
    exit()

# exit()

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')

for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
        continue
    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))

### NFS
if nfsFlag == 1 or allFlag == 1:
    
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))

        ### Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        #resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
        
        ### Copy and Delete
        if output[0] == "PASSED":
            
            ### Copy
            if copy:
                print "Volume %s mounted successfully" %(config['volMountpoint%d' %(x)])
                q=getoutput('df -h | grep %s | awk \'{print $1}\' | sed s/G//' %(config['volMountpoint%d' %(x)]))
                executeCmd('cp %s  mount/%s' %(filename, config['volMountpoint%d' %(x)]))
                executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['volMountpoint%d' %(x)], filename, filename))
                diffoutput=executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                endTime = ctime()
                resultCollection("Checksum result on NFS Volume %s is:" %(config['volDatasetname%d' %(x)]), diffoutput, startTime, endTime)
                # print q[1]
                executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))
            
            ### delete
            if delete:
                # print 'Inside delete'
                out = executeCmd('rm  mount/%s/%s' %(config['volMountpoint%d' %(x)], filename))
                out2 = executeCmdNegative('ls mount/%s | grep %s' % (config['volMountpoint%d' %(x)], filename))
                endTime = ctime()
                resultCollection("Delete file \"%s\" operation on volume %s is:" %(filename, config['volDatasetname%d' %(x)]), out2, startTime, endTime)
                
                executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))

        else:
            endTime = ctime()
            print "Mount failed for volume %s" %(config['volDatasetname%d' %(x)])
            resultCollection("Further Execution of TCs Skipped on NFS Volume %s" %(config['volDatasetname%d' %(x)]), ('Due to Mount Failed', ' '), startTime, endTime) 

### ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        
        ### Discovery 
        executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
        iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
        print iqnname
        if iqnname==[]:
            print "no iscsi volumes discovered on the client"
            endTime = ctime()
            resultCollection("no iscsi volumes discovered on the client",["FAILED",""], startTime, endTime)
            continue

        ### Login to ISCSI
        output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        #resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
        print output[0]
        time.sleep(5)
    
        ### Make filesystem, Mount, Copy and delete
        if output[0] == "PASSED":
            device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
            device2 = (device[0].split('\n'))[0]
            ### mkfs
            if write_mkfs:
                executeCmd('fdisk /dev/%s < fdisk_response_file' %(device2))
                quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device2))
                q= int(quota[0])/(1024*1024*1024)
                # print q
                executeCmd('mkfs.ext3 /dev/%s1' %(device2))

            ### mount
            # executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
            
            #endTime = ctime()
            #resultCollection("Mount of ISCSI Volume %s is:" %(config['voliSCSIDatasetname%d' %(x)]), mountOutput, startTime, endTime)
                
            if mountOutput[0] == "PASSED":
                    
                ### Copy
                if copy:
                    print "volume %s mounted successfully" %(config['voliSCSIMountpoint%d' %(x)])
                    executeCmd('cp %s  mount/%s' %(filename, config['voliSCSIMountpoint%d' %(x)]))
                    executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['voliSCSIMountpoint%d' %(x)], filename, filename))
                    diffoutput=executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                    endTime = ctime()
                    resultCollection("Checksum result on ISCSI Volume %s is:" %(config['voliSCSIDatasetname%d' %(x)]), diffoutput, startTime, endTime)
                    q1=getoutput('df -h | grep /dev/%s1 | awk \'{print $2}\' | sed s/G//' %(device2))
                    # print q1[0]
                    executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                    
                ### Delete
                if delete:
                    print 'Inside Delete'
                    out = executeCmd('rm mount/%s/%s' %(config['voliSCSIMountpoint%d' %(x)], filename))
                    out2 = executeCmdNegative('ls mount/%s | grep %s' %(config['voliSCSIMountpoint%d' %(x)], filename))
                    endTime = ctime()
                    resultCollection("Delete file \"%s\" operation on volume %s is:" %(filename, config['voliSCSIDatasetname%d' %(x)]), out2, startTime, endTime)
                        
                    executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            else:
                print "mount failed for volume %s" %(config['voliSCSIDatasetname%d' %(x)])
                endTime = ctime()
                resultCollection("Mount of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), mountOutput, startTime, endTime)

            ### Logout to ISCSI
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
        else:
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' '), startTime, endTime)

### CIFS
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
        ### Mount
        executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))
        #resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output)
        
        ### Copy and Delete
        if output[0] == "PASSED":
            
            ### Copy
            if copy:
                print "volume %s mounted successfully" %(config['volCifsMountpoint%d' %(x)])
                # executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
                executeCmd('cp %s  mount/%s' %(filename, config['volCifsMountpoint%d' %(x)]))
                executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mount/%s_md5sum_mount' %(config['volCifsMountpoint%d' %(x)], filename, filename))
                diffoutput=executeCmd('diff mount/%s_md5sum mount/%s_md5sum_mount' %(filename, filename))
                endTime = ctime()
                resultCollection("Checksum result on CIFS Volume %s is:" %(config['volCifsDatasetname%d' %(x)]), diffoutput, startTime, endTime)
                
            ### Delete
            if delete:
                print 'Inside Delete'
                out = executeCmd('rm mount/%s/%s' %(config['volCifsMountpoint%d' %(x)], filename))
                out2 = executeCmdNegative('ls mount/%s | grep %s' %(config['volCifsMountpoint%d' %(x)], filename))
                endTime = ctime()
                resultCollection("Delete file \"%s\" operation on volume %s is:" %(filename, config['volCifsDatasetname%d' %(x)]), out2, startTime, endTime)
                
        else:
            endTime = ctime()
            print "mount failed for volume %s" %(config['volCifsMountpoint%d' %(x)])
            resultCollection("Further Execution of TCs Skipped on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), ('Due to Mount Failed', ' '), startTime, endTime) 

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')

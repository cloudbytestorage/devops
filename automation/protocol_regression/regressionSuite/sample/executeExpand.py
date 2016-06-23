import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, resultCollection, getoutput

config = configFile(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0

########### TestCase Execution Starts.. 
if len(sys.argv) < 3:
     print "Argument is not correct.. Correct way as below"
     print "python executeExpand.py config.txt NFS"
     print "python executeExpand.py config.txt ALL"
     print "python executeExpand.py config.txt NFS CIFS ISCSI"
     exit()
                        
for x in range(2, len(sys.argv)):
    if sys.argv[x].lower() == "%s" %("nfs"):
        nfsFlag = 1;
    elif sys.argv[x].lower() == "%s" %("cifs"):
        cifsFlag = 1;
    elif sys.argv[x].lower() == "%s" %("fc"):
        fcFlag = 1;
    elif sys.argv[x].lower() == "%s" %("iscsi"):
        iscsiFlag = 1;
    elif sys.argv[x].lower() == "%s" %("all"):
        allFlag == 1;
    else:
        print "Argument is not correct.. Correct way as below"
        print "python executeExpand.py config.txt NFS"
        print "python executeExpand.py config.txt ALL"
        print "python executeExpand.py config.txt NFS CIFS ISCSI"
        exit()




executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
        continue
    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))


###NFS
if nfsFlag == 1 or allFlag ==1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
        ######Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        #resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp testfile  mount/%s' %(config['volMountpoint%d' %(x)]))
            output=executeCmd('diff testfile mount/%s' %(config['volMountpoint%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Creation of File on NFS Volume %s" %(config['volDatasetname%d' %(x)]), output,startTime,endTime)
                continue

            q=getoutput('df -h | grep %s | awk \'{print $1}\' | sed s/G//' %(config['volMountpoint%d' %(x)]))
            print float(q[1])

            quota=config['volQuotasize%d' %(x)]
            print quota[:-1]
           
            if (q >= float(quota[:-1])):
                print "nfs volume expansion successfull on client"
                endTime = ctime()
                resultCollection(" %s volume expanded successfully on client" %(config['volDatasetname%d' %(x)]),["PASSED",""],startTime,endTime)
            else:
                print "nfs volume expansion unsuccesfull on client"
                endTime = ctime()
                resultCollection(" %s volume expansion failed on client" %(config['volDatasetname%d' %(x)]),["FAILED",""],startTime,endTime)
            executeCmd('umount %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))

        else:
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on NFS Volume %s" %(config['volDatasetname%d' %(x)]), ('Due to Mount Failed', ' '),startTime,endTime) 



###ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        executeCmd('mkdir -p expand/')
        ######Discovery 
        executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
        iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
        if iqnname==[]:
            resultCollection("Further Execution of TCs Skipped Couldn't discover the iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' '))
            continue
        ######Login to ISCSI
        output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        #resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
        #print output[0]
        time.sleep(5)

        ######Mount
        if output[0] == "PASSED":
            executeCmd('fdisk /dev/sdb < fdisk_response_file2' )
            time.sleep(5)
            quota=getoutput('fdisk -l | grep /dev/sdb: |  awk {\'print $5\'}')
            q= int(quota[0])/(1024*1024*1024)
            print q

            executeCmd('mkfs.ext3 /dev/sdb2')
            mountOutput1=executeCmd('mount /dev/sdb2  expand/' )
            mountOutput=executeCmd('mount /dev/sdb1  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            print mountOutput1[0]
            #####Copy
            if mountOutput1[0] == "PASSED":
                print "mount successfull"
                executeCmd('cp testfile  expand/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                output=executeCmd('diff testfile expand/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                if output == "FAILED":
                    endTime = ctime()
                    resultCollection("Creation of File on extended iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output,startTime,endTime)
                    continue
                q2=getoutput('df -h | grep /dev/sdb2 | awk \'{print $2}\' | sed s/G//')
                print float(q2[0])
                q1=getoutput('df -h | grep /dev/sdb1 | awk \'{print $2}\' | sed s/G//')
                print float(q1[0])
                q = float(q1[0]) + float(q2[0])
                print q
                quota=config['voliSCSIQuotasize%d' %(x)]
                print quota[:-1]

                if (q >= float(quota[:-1])):
                    print "iscsi volume expansion successfull on client"
                    endTime = ctime()
                    resultCollection(" %s volume expanded successfully on client" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""],startTime,endTime)

                else:
                    print "iscsi volume expansion unsuccesfull on client"
                    endTime = ctime()
                    resultCollection(" %s volume expansion failed on client" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""],startTime,endTime)

                executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                executeCmd('umount expand/')
            else:  
                print "mount failed"
                endTime = ctime()
                resultCollection("Mount of iSCSI Volume %s, expansion Failed" %(config['voliSCSIDatasetname%d' %(x)]), mountOutput,startTime,endTime)
                                                                                                                                                                                    ######Logout to ISCSI
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output,startTime,endTime)
    
        else: 
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' '),startTime,endTime)


###CIFS
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
        ######Mount
        executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))
        #resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output)
        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp testfile  mount/%s' %(config['volCifsMountpoint%d' %(x)]))
            output=executeCmd('diff testfile mount/%s' %(config['volCifsMountpoint%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Creation of File on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output,startTime,endTime)
                continue
            
            q=getoutput('df -h | grep %s | awk \'{print $1}\' | sed s/G//' %(config['volCifsMountpoint%d' %(x)]))
            print float(q[1])

            quota=config['volCifsQuotasize%d' %(x)]
            print quota[:-1]

            if (q >= float(quota[:-1])):
                print "cifs volume expansion successfull on client"
                endTime = ctime()
                resultCollection(" %s volume expanded successfully on client" %(config['volCifsDatasetname%d' %(x)]),["PASSED",""],startTime,endTime)
            else:
                print "cifs volume expansion unsuccesfull on client"
                endTime = ctime()
                resultCollection(" %s volume expansion failed on client" %(config['volCifsDatasetname%d' %(x)]),["FAILED",""],startTime,endTime)
                                                                                    
        else:
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), ('Due to Mount Failed', ' '),startTime,endTime) 


executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')



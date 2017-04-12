import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, resultCollection, getoutput, getControllerInfo
config = configFile(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python execution.py config.txt nodeIP nodePassword NFS"
    print "python execution.py config.txt nodeIP nodePassword ALL"
    print "python execution.py config.txt nodeIP nodePassword NFS CIFS ISCSI"
    exit()

if sys.argv[4].lower() == "nfs":
    nfsFlag = 1;
elif sys.argv[4].lower() == "cifs":
    cifsFlag = 1;
elif sys.argv[4].lower() == "fc":
    fcFlag = 1;
elif sys.argv[4].lower() == "iscsi":
    iscsiFlag = 1;
elif sys.argv[4].lower() == "all":
    allFlag = 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python execution.py config.txt nodeIP nodePassword NFS"
    print "python execution.py config.txt nodeIP nodePassword ALL"
    print "python execution.py config.txt nodeIP nodePassword NFS CIFS ISCSI"
    exit()



IP = sys.argv[2]
passwd = sys.argv[3]

########### TestCase Execution Starts..
executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')

for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
        continue
    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))


###NFS
if nfsFlag == 1 or allFlag ==1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
        ######Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        #resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
        q=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volMountpoint%d' %(x)]))
        print " used space of volume on client = %s after mount" %q[1].strip()
        size = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % (config['volDatasetname%d' %(x)]), "size.txt")
        print "size=%s" % size.strip()
    

        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp testfile  mount/%s' %(config['volMountpoint%d' %(x)]))
            time.sleep(5)
            output=executeCmd('diff testfile mount/%s' %(config['volMountpoint%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Creation of File on NFS Volume %s" %(config['volDatasetname%d' %(x)]), output,startTime,endTime)
                continue
            q1=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volMountpoint%d' %(x)]))
            print " used space of volume on client = %s after copying file" %q1[1].strip()
            
            newsize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['volDatasetname%d' %(x)], "size.txt")
            print "newsize=%s" % newsize.strip()
            
            ### deleting testfile
            executeCmd('rm  mount/%s/testfile' %(config['volMountpoint%d' %(x)]))
            time.sleep(5)
            q2=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volMountpoint%d' %(x)]))
            print " used space of volume on client = %s after deleting the volume" %q2[1].strip()
            cursize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['volDatasetname%d' %(x)], "size.txt")
            print "cursize=%s" % cursize.strip()
            
            ### verification of nfs volume size on client
            if q2[1]==q[1]:
                print " space reclaimation successfull on nfs volume on client"
                endTime = ctime()
                resultCollection(" space reclaimation successfull on nfs volume %s on client %s %s %s" %(config['volDatasetname%d' %(x)],q[1].strip(),q1[1].strip(),q2[1].strip()), ["PASSED"," "],startTime,endTime)
            else:
                print " space reclaimation unsuccessfull on nfs volume on client"
                endTime = ctime()
                resultCollection(" space reclaimation unsuccessfull on nfs volume %s on client %s %s %s" %(config['volDatasetname%d' %(x)],q[1].strip(),q1[1].strip(),q2[1]).strip(), ["FAILED"," "],startTime,endTime)
            
            ### verification of nfs volume size on controller
            if cursize == size:
                print " space reclaimation successfull on nfs volume on controller"
                endTime = ctime()
                resultCollection(" space reclaimation successfull on nfs volume %s on controller %s %s %s"  %(config['volDatasetname%d' %(x)],size.strip(),newsize.strip(),cursize.strip()), ["PASSED"," "],startTime,endTime)
            else:
                print "space reclaimation unsuccessfull on nfs volume on controller"
                endTime = ctime()
                resultCollection(" space reclaimation unsuccessfull on nfs volume %s on controller %s %s %s" %(config['volDatasetname%d' %(x)],size.strip(),newsize.strip(),cursize.strip()), ["FAILED"," "],startTime,endTime)
         
            executeCmd('umount  %s:/%s' %(config['volIPAddress%d' %(x)],config['volMountpoint%d' %(x)]))
        else:
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on NFS Volume %s" %(config['volDatasetname%d' %(x)]), ('Due to Mount Failed', ' '),startTime,endTime) 

'''
###ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
        ######Discovery 
        executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
        iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
        if iqnname == []:
            resultCollection("Further Execution of TCs Skipped Couldn't discover the iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' '))
            continue
        ######Login to ISCSI
        output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
        time.sleep(5)
    
        ######Mount
        if output[0] == "PASSED":
            executeCmd('fdisk /dev/sdb < fdisk_response_file' )
            executeCmd('mkfs.ext3 /dev/sdb1')
            mountOutput=executeCmd('mount /dev/sdb1  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            #####Copy
            if mountOutput[0] == "PASSED":
                print "mount successfull"
                q=getoutput('df -h | grep /dev/sdb1 | awk \'{print $2}\' | sed s/\[A-Z\]//')
                print " used space of volume on client = %s after mount" % q[1].strip()
                size = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % (config['voliSCSIDatasetname%d' %(x)]), "size.txt")
                print "size=%s" % size.strip()
                
                executeCmd('cp testfile  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                time.sleep(5)
                output=executeCmd('diff testfile mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                resultCollection("Creation of File on ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
                q1=getoutput('df -h | grep /dev/sdb1 | awk \'{print $2}\' | sed s/\[A-Z\]//')
                print " used space of volume on client = %s after copying file" %q1[1].strip()
                newsize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['voliSCSIDatasetname%d' %(x)], "size.txt")
                print "newsize=%s" % newsize.strip()

                ### deleting testfile
                executeCmd('rm  mount/%s/testfile' %(config['voliSCSIMountpoint%d' %(x)]))
                time.sleep(5)
                q2=getoutput('df -h | grep /dev/sdb1 | awk \'{print $2}\' | sed s/\[A-Z\]//')
                print " used space of volume on client = %s after deleting the volume" %q2[1].strip()
                cursize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['voliSCSIDatasetname%d' %(x)], "size.txt")
                print "cursize=%s" % cursize.strip()

                ### verification of iscsi volume size on client
                if q2[1]==q[1]:
                    print " space reclaimation successfull on iscsi volume on client"
                    resultCollection(" space reclaimation successfull on iscsi volume %s on client %s %s %s" %(config['voliSCSIDatasetname%d' %(x)],q[1],q1[1],q2[1]), ["PASSED"," "])
                else:
                    print "space reclaimation unsuccessfull on iscsi volume on controller"
                    resultCollection(" space reclaimation unsuccessfull on iscsi volume %s on controller %s %s %s" %(config['voliSCSIDatasetname%d' %(x)],size,newsize,cursize), ["FAILED"," "])
                executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            else:
                print "mount failed"
                resultCollection("Mount of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), mountOutput)

            ######Logout to ISCSI
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
        else:
            resultCollection("Further Execution of TCs Skipped on iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' ')) 
'''


###CIFS
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        executeCmd('mkdir -p mount/%s' %(config['volCifsMountpoint%d' %(x)]))
        ######Mount
        executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))
        #resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output)
        q=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volCifsMountpoint%d' %(x)]))
        print " used space of volume on client = %s after mount" %q[1].strip()
        size = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % (config['volCifsDatasetname%d' %(x)]), "size.txt")
        print "size=%s" % size.strip()
        
        
        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp testfile  mount/%s' %(config['volCifsMountpoint%d' %(x)]))
            time.sleep(5)
            output=executeCmd('diff testfile mount/%s' %(config['volCifsMountpoint%d' %(x)]))
            if output == "FAILED":
                endTime = ctime()
                resultCollection("Creation of File on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output,startTime,endTime)
                continue
            q1=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volCifsMountpoint%d' %(x)]))
            print " used space of volume on client = %s after copying file" %q1[1].strip()
            newsize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['volCifsDatasetname%d' %(x)], "size.txt")
            print "newsize=%s" % newsize.strip()

            ### deleting testfile
            executeCmd('rm  mount/%s/testfile' %(config['volCifsMountpoint%d' %(x)]))
            executeCmd('rm -r mount/%s/.recycle/'%(config['volCifsMountpoint%d' %(x)]))
            time.sleep(5)
            q2=getoutput('df -h | grep %s | awk \'{print $2}\' | sed s/\[A-Z\]//' %(config['volCifsMountpoint%d' %(x)]))
            print " used space of volume on client = %s after deleting the volume" %q2[1].strip()
            cursize = getControllerInfo(IP, passwd, " zfs list | grep %s | awk '{print $2}' | sed  s/\[A-Z\]//" % config['volCifsDatasetname%d' %(x)], "size.txt")
            print "cursize=%s" % cursize.strip()
            
            ### verification of cifs volume size on client
            if q2[1]==q[1]:
                print " space reclaimation successfull on cifs volume on client"
                endTime = ctime()
                resultCollection(" space reclaimation successfull on cifs volume %s on client %s %s %s" %(config['volCifsDatasetname%d' %(x)],q[1].strip(),q1[1].strip(),q2[1].strip()), ["PASSED"," "],startTime,endTime)
            else:
                print " space reclaimation unsuccessfull on cifs volume on client"
                endTime = ctime()
                resultCollection(" space reclaimation unsuccessfull on cifs volume %s on client %s %s %s" %(config['volCifsDatasetname%d' %(x)],q[1].strip(),q1[1].strip(),q2[1].strip()), ["FAILED"," "],startTime,endTime)
            
            ### verification of cifs volume size on controller
            if cursize == size:
                print " space reclaimation successfull on cifs volume on controller"
                endTime = ctime()
                resultCollection(" space reclaimation successfull on cifs volume %s on controller %s %s %s"  %(config['volCifsDatasetname%d' %(x)],size.strip(),newsize.strip(),cursize.strip()), ["PASSED"," "],startTime,endTime)
            else:
                print "space reclaimation unsuccessfull on cifs volume on controller"
                endTime = ctime()
                resultCollection(" space reclaimation unsuccessfull on cifs volume %s on controller %s %s %s" %(config['volCifsDatasetname%d' %(x)],size.strip(),newsize.strip(),cursize.strip()), ["FAILED"," "],startTime,endTime)
        else:
            endTime = ctime()
            resultCollection("Further Execution of TCs Skipped on CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), ('Due to Mount Failed', ' '),startTime,endTime) 


#executeCmd('umount -a -t cifs -l')
#executeCmd('umount -a')

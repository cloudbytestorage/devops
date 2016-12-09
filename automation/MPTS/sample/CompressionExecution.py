import json
import sys
import time
from time import sleep, ctime
from cbrequest import sendrequest, filesave, executeCmd, resultCollection, timetrack, queryAsyncJobResult, configFile ,getoutput, getControllerInfo
nfsFlag = cifsFlag = iscsiFlag =  fcFlag = allFlag = 0

############### TestCase Execution Starts  ###############
if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print "python CompressionExecution.py compressConfig.txt cifs/nfs/iscsi/fc/all on/off IP Password filename"
    exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
if  sys.argv[2].lower() == "%s" %("nfs"):
        nfsFlag = 1;
elif sys.argv[2].lower() == "%s" %("cifs"):
        cifsFlag = 1;
elif sys.argv[2].lower() == "%s" %("iscsi"):
        iscsiFlag = 1;
elif sys.argv[2].lower() == "%s" %("all"):
        allFlag = 1;
elif sys.argv[2].lower() == "%s" %("fc"):
        fcFlag = 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python CompressionExecution.py compressConfig.txt cifs/nfs/iscsi/fc/all on/off IP Password filename"
    exit()
compvalue = sys.argv[3]
IP=sys.argv[4]
password = sys.argv[5]
if len(sys.argv) == 7:
  testfile == sys.argv[6]
else:
  testfile = "textfile"
############### NFS EXECUTION STARTS  ###############
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        r1=executeCmd(' rm -rf  mount1/%s/* '%(config['volMountpoint%d' %(x)]))
        sleep(5)
        r2=executeCmd('umount mount1/%s'%(config['volMountpoint%d' %(x)]))
        r3=executeCmd (' rm -rf mount1/%s'%(config['volMountpoint%d' %(x)]))
        r4=executeCmd('mkdir -p mount1/%s ' %(config['volMountpoint%d' %(x)]))
###############  Mount  ###############
        executeCmd('mount -t nfs %s:/%s mount1/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep  %s' %(config['volMountpoint%d' %(x)]))
        endTime = ctime()
        resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output,startTime, endTime)
        print "mounting NFS volume %s is " %(config['volMountpoint%d' %(x)]),output[0] 
############### Before Copy ##############
        cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['volDatasetname%d' %(x)])    
        size1 = getControllerInfo(IP,password, cmd1, "backend_output_bc0.txt")
        print " Before copy used space of NFS volume %s is "%(config['volDatasetname%d' %(x)])
        print size1
        cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'"%(config['volDatasetname%d' %(x)])
        ratio1 =  getControllerInfo(IP,password, cmd2, "backend_output_cr0.txt")
        print " Before copy Compresion Ratio of volume %s is "%(config['volDatasetname%d' %(x)]),
        print ratio1
        cr1 = float(ratio1[0:-2])
        print cr1
###############  After Copy  ################
        if output[0] == "PASSED":
            copyResult=executeCmd('cp -v %s  mount1/%s' %(testfile,config['volMountpoint%d' %(x)]))
            print copyResult[0]
            sleep(5)
            cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['volDatasetname%d' %(x)])
            size2= getControllerInfo(IP,'test', cmd1, "backend_output0.txt")
            print " After copy used space of volume %s is "%(config['volDatasetname%d' %(x)])
            print size2
            cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'" %(config['volDatasetname%d' %(x)])
            ratio2 = getControllerInfo(IP,password, cmd2, "backend_output_ac0.txt")
            print " After copy compress Ratio is " 
            print ratio2
            cr2 = float(ratio2[0:-2])
            print cr2
            
           
###############  Compare size  ###############
            fs = getoutput(" du -b %s | awk '{print $1}' " %(testfile))
            print "testfile size is"
            print fs[0]
            filesize = float(fs[0])
            print filesize
            diffsize = float(size2) - float(size1)
            endTime=ctime()
            if diffsize < filesize and cr2 > cr1 and compvalue == "on":
                print "Compression is enabled on %s and working" %(config['volDatasetname%d' %(x)])
                resultCollection("Compression is enabled on %s and working" %(config['volDatasetname%d' %(x)]),["PASSED" ' '], startTime, endTime)
            elif diffsize >= filesize and cr2 == cr1 and compvalue == "off":
                print "Compression is disabled on %s and working" %(config['volDatasetname%d' %(x)])
                resultCollection("Compression is enabled on %s and working" %(config['volDatasetname%d' %(x)]),["PASSED" ' '], startTime, endTime)
            else:
                print "Compression Feature is not working on %s" %(config['volDatasetname%d' %(x)])
                resultCollection("Compression feature is not working on %s" %(config['volDatasetname%d' %(x)]),["FAILED" ' '], startTime, endTime)
        else:
             print "Test case execution aborted due to mount fail"
             endTime=ctime()
             resultCollection("Mounting of file %s got FAILED" %(config['volDatasetname%d' %(x)]),"FAILED", startTime, endTime)



###ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            startTime=ctime()
            ############$$$$$$$
            executeCmd('rm -rf mount1/%s/*'%(config['voliSCSIMountpoint%d' %(x)]))
            executeCmd('umount -rf mount1/%s'%(config['voliSCSIMountpoint%d' %(x)]))
            #output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --logout | grep Logout' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
            executeCmd('rm -rf mount1/%s'%(config['voliSCSIMountpoint%d' %(x)]))
            executeCmd('mkdir -p mount1/%s' %(config['voliSCSIMountpoint%d' %(x)]))
            #################********************
            ### Discovery 
            executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
            iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
            print iqnname
            if iqnname==[]:
               print "no iscsi volumes discovered on the client"
               endTime = ctime()
               resultCollection("no iscsi volumes discovered on the client",["FAILED", ' '], startTime, endTime)
               ### Login to ISCSI
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            #resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
            print output[0]
            time.sleep(5)
            ### Make filesystem, Mount, Copy and delete
            if output[0] == "PASSED":
                device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                device2 = (device[0].split('\n'))[0]
                device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                            device2 = (device[0].split('\n'))[0]
                                        ### mkfs
                                                    if write_mkfs:
                                                                        executeCmd('fdisk /dev/%s < fdisk_response_file' %(device2))
                                                                                        quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device2))
                                                                                                        q= int(quota[0])/(1024*1024*1024)
                                                                                                                        executeCmd('mkfs.ext3 /dev/%s1' %(device2))

            ### mkfs
               executeCmd('fdisk /dev/%s < fdisk_response_file' %(device2))
               quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device2))
               q= int(quota[0])/(1024*1024*1024)
               print q
               executeCmd('mkfs.ext3 /dev/%s1' %(device2))
               ### mount
               # executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
               mountOutput=executeCmd('mount /dev/%s1  mount1/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
               print  mountOutput
               ###############****************
               if mountOutput[0] == "PASSED":
                time.sleep(3)
                output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                 ###############$$$$$$$$$$$
                sleep(5)
                ####@@@@@@@@@ Before Copy
                cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['voliSCSIDatasetname%d' %(x)])
                size1 = getControllerInfo(IP,password, cmd1, "backend_output_bc0.txt")
                print " Before copy used space of NFS volume %s is "%(config['voliSCSIDatasetname%d' %(x)])
                print size1
                cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'"%(config['voliSCSIDatasetname%d' %(x)])
                ratio1 =  getControllerInfo(IP,password, cmd2, "backend_output_cr0.txt")
                print " Before copy Compresion Ratio of volume %s is "%(config['voliSCSIDatasetname%d' %(x)]),
                print ratio1
                cr1 = float(ratio1[0:-2])
                print cr1
                ###############  After Copy  ################
                if output[0] == "PASSED":
                 copyResult=executeCmd('cp -v %s  mount1/%s' %(testfile,config['voliSCSIMountpoint%d' %(x)]))
                 print copyResult[0]
                 sleep(5)
                 cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['voliSCSIDatasetname%d' %(x)])
                 size2= getControllerInfo(IP,'test', cmd1, "backend_output0.txt")
                 print " After copy used space of volume %s is "%(config['voliSCSIDatasetname%d' %(x)])
                 print size2
                 cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'" %(config['voliSCSIDatasetname%d' %(x)])
                 ratio2 = getControllerInfo(IP,password, cmd2, "backend_output_ac0.txt")
                 print " After copy compress Ratio is "
                 print ratio2
                 cr2 = float(ratio2[0:-2])
                 print cr2
                 ###############  Compare size  ###############
                 fs = getoutput('du -b %s | awk \'{print $1}\''%(testfile))
                 filesize = float(fs[0])
                 print "testfile size is"
                 print filesize
                 diffsize = float(size2) - float(size1)
                 endTime=ctime()
                 if diffsize < filesize and cr2 > cr1 and compvalue == "on":
                   print "Compression is enabled on %s and working" %(config['voliSCSIDatasetname%d' %(x)])
                   resultCollection("Compression is enabled on %s and working" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED" ' '], startTime, endTime)
                 elif diffsize >= filesize and cr2 == cr1 and compvalue == "off":
                   print "Compression is disabled on %s and working" %(config['voliSCSIDatasetname%d' %(x)])
                   resultCollection("Compression is enabled on %s and working" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED" ' '], startTime, endTime)
                 else:
                    print "Compression Feature is not working on %s" %(config['voliSCSIDatasetname%d' %(x)])
                    resultCollection("Compression feature is not working on %s" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED" ' '], startTime, endTime)
                ######@@@@@@@@@@@
######Logout to ISCSI
                output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                if output == "FAILED":
                   endTime = ctime()
                   resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
            else:
                endTime=ctime()
                resultCollection("Further Execution of TCs Skipped on iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), ('Due to Login Failed', ' '), startTime, endTime)

###CIFS
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime=ctime()
        r1=executeCmd(' rm -rf  mount1/%s/* ' %(config['volCifsMountpoint%d'  %(x)]))
        sleep(5)
        r2=executeCmd('umount -rf mount1/%s'  %(config['volCifsMountpoint%d' %(x)]))
        r3=executeCmd(' rm -rf mount1/%s'     %(config['volCifsMountpoint%d' %(x)]))
        umount=executeCmd('umount -a -t cifs -l')
        print umount
        endTime=ctime()
        resultCollection(" Un-mount  of Cifs volume %s is "%(config['volCifsDatasetname%d' %(x)]),umount, startTime, endTime)
        r1=executeCmd('mkdir -p mount1/%s' %(config['volCifsMountpoint%d' %(x)]))
        print r1
###################### Before Copy ##################
        cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['volCifsDatasetname%d' %(x)])
        size1 = getControllerInfo(IP,password, cmd1, "backend_output_bc0.txt")
        print " Before copy used space of NFS volume %s is "%(config['volCifsDatasetname%d' %(x)])
        print size1
        cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'"%(config['volCifsDatasetname%d' %(x)])
        ratio1 =  getControllerInfo(IP,password, cmd2, "backend_output_cr0.txt")
        print " Before copy Compresion Ratio of volume %s is "%(config['volCifsDatasetname%d' %(x)]),
        print ratio1
        cr1 = float(ratio1[0:-2])
        print cr1

############## Mount ################
        r2=executeCmd(' mount -t cifs //%s/%s mount1/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
        print r2
        output=executeCmd('mount | grep  %s' %(config['volCifsMountpoint%d' %(x)]))
        #print output[0]
        endTime=ctime()
        resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), r1, startTime, endTime)
    #############Copy
        if output[0] == "PASSED":
           copy=executeCmd('cp -v %s mount1/%s' %(testfile,config['volCifsMountpoint%d' %(x)]))
           sleep(5)
           cmd1 = " zfs get -Hp all | grep  %s | grep -w used | awk \'{print $3}\'"%(config['volCifsDatasetname%d' %(x)])
           size2= getControllerInfo(IP,'test', cmd1, "backend_output0.txt")
           print " After copy used space of volume %s is "%(config['volCifsDatasetname%d' %(x)])
           print size2
           cmd2 = " zfs get -Hp all | grep  %s | grep -w compressratio | awk \'{print $3}\'" %(config['volCifsDatasetname%d' %(x)])
           ratio2 = getControllerInfo(IP,password, cmd2, "backend_output_ac0.txt")
           print " After copy compress Ratio is "
           print ratio2
           cr2 = float(ratio2[0:-2])
           print cr2
           ###############  Compare size  ###############
           fs = getoutput('du -b %s | awk \'{print $1}\''%(testfile))
           print "testfile size is"
           filesize = float(fs[0])
           print filesize
           diffsize = float(size2) - float(size1)
           print diffsize
           endTime=ctime()
           if diffsize < filesize and cr2 > cr1 and compvalue == "on":
              print "Compression is enabled on %s and working" %(config['volCifsDatasetname%d' %(x)])
              resultCollection("Compression is enabled on %s and working" %(config['volCifsDatasetname%d' %(x)]), ("PASSED" ' '), startTime, endTime)
           elif diffsize >= filesize and cr2 == cr1 and compvalue == "off":
              print "Compression is disabled on %s and working" %(config['volCifsDatasetname%d' %(x)])
              resultCollection("Compression is enabled on %s and working" %(config['volCifsDatasetname%d' %(x)]),("PASSED" ' '), startTime, endTime)
           else:
              print "Compression Feature is not working on %s" %(config['volCifsDatasetname%d' %(x)])
              resultCollection("Compression feature is not working on %s" %(config['volCifsDatasetname%d' %(x)]),("FAILED" ' '), startTime, endTime)
           executeCmd('umount -a -t cifs -l')        
        else:
          print "Test case execution aborted due to mount fail"
          endTime=ctime()
          resultCollection("Mounting of file %s got FAILED" %(config['volCifsDatasetname%d' %(x)]),"FAILED", startTime, endTime)
#executeCmd('umount -a')
                                                                                          

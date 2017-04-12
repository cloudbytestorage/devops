import json
import requests
import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd, getoutput, getControllerInfo
#import setISCSIInitiatorGroup.py
if len(sys.argv) < 2:
        print "Argument is not correct.. Correct way as below"
        print "python IscsiSecurityExecution.py dedup.txt filename "
        exit()
config = configFile(sys.argv);
#print config
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
if len(sys.argv) == 3:
    testfile=sys.argv[2]
else:
    testfile="textfile"
#assign default access to all iscsi volumes
executeCmd('python setISCSIInitiatorGroup.py dedup.txt')
executeCmd('python setIscsiAuthMethod.py dedup.txt')
executeCmd('python setIscsiAuthGroup.py dedup.txt')
# for all iscsi volumes in config files
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
         PoolName = config['voliSCSIPoolName%d' %(x)]
         executeCmd('rm -rf mount/%s/*'%(config['voliSCSIMountpoint%d' %(x)]))
         executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
         executeCmd('rm -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
         startTime=ctime()
         executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
         #discovery iscsi volumes
         executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
         iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
         print iqnname
         if iqnname==[]:
              print "no iscsi volumes discovered on the client"
              endTime = ctime()
              resultCollection("no iscsi volumes discovered on the client when initiator group is ALL",["FAILED",""], startTime, endTime)
         else:
             output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
             time.sleep(30)
             print output
             if output[0]=="PASSED":
                device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                device2 = (device[0].split('\n'))[0]
                print device2
                ### mkfs
                executeCmd('fdisk /dev/%s < fdisk_response_file' %(device2))
                quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device2))
                #q= int(quota[0])/(1024*1024*1024)
                #print q
                executeCmd('mkfs.ext3 /dev/%s1' %(device2))
                time.sleep(10)
                ### mount
                mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                print  mountOutput
                endTime = ctime()
                if mountOutput[0] == "PASSED":
                   time.sleep(3)
                   output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                   executeCmd('rm -rf mount/%s/*' %(config['voliSCSIMountpoint%d' %(x)]))
                   executeCmd('cp -v %s mount/%s/' %(testfile,config['voliSCSIMountpoint%d' %(x)]))
                   #time.sleep(20)
                   executeCmd('md5sum mount/%s/%s | awk {\'print $1\'} > basemd5sum ' %(config['voliSCSIMountpoint%d' %(x)],testfile))
                   #unmount
                   executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                   #logout
                   output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                   time.sleep(30)
                   if output == "FAILED":
                      endTime = ctime()
                      resultCollection("Logout of iSCSI Volume %s when initiator group is ALL" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                else:
                   print " Mount Fail , Exiting......"
                   endTime=ctime()
                   resultCollection("Mounting the ISCSI volume %s got failed when initiator group is ALL"%(config['voliSCSIDatasetname%d' %(x)]),mountOutput[0],startTime, endTime)
                   output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                   time.sleep(30)
                   if output == "FAILED":
                      endTime = ctime()
                      resultCollection("Logout of iSCSI Volume %s when initiator group is ALL" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)

#end of iscsi initiator ALL
#change the iscsi initiator to iqn-based
                if mountOutput[0] == "PASSED":
                   executeCmd('python setISCSIInitiatorGroup.py dedup.txt iqn1')
                   #discovery iscsi volumes
                   executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
                   iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
                   print iqnname
                   if iqnname==[]:
                      print "no iscsi volumes discovered on the client"
                      endTime = ctime()
                      resultCollection("no iscsi volumes discovered on the client when initiator group is iqn1",["FAILED",""], startTime, endTime)
                   else:
                      output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                      time.sleep(30)
                      if output[0]=="PASSED":
                          device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                          device2 = (device[0].split('\n'))[0]
                          ### mount
                          time.sleep(10)
                          mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                          print  mountOutput
                          endTime = ctime()
                          if mountOutput[0] == "PASSED":
                            time.sleep(3)
                            output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                            time.sleep(20)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > initmd5sum ' %(config['voliSCSIMountpoint%d' %(x)], testfile))
                            endTime = ctime()
                            result=executeCmd('diff basemd5sum initmd5sum')
                            print result[0]
                            if result[0] == "PASSED":
                               print "Data is available after changing the initiator group"
                               resultCollection("Changing the initiator group to iqn-based on %s does not result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                            else:
                               print "Data is not available after changing the initiator group"
                               resultCollection("Changing the initiator group to iqn-based on %s is result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)
                         #unmount
                            executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                           #logout
                            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                            time.sleep(30)
                            if output == "FAILED":
                               endTime = ctime()
                               resultCollection("Logout of iSCSI Volume %s when initiator group is iqn1" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                          else:
                             print " Mount Fail , Exiting......"
                             endTime = ctime()
                             resultCollection("Mounting the ISCSI volume %s got failed when initiator group is iqn1"%(config['voliSCSIDatasetname%d' %(x)]),mountOutput[0],startTime, endTime)
                             endTime=ctime()
                             output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                             time.sleep(30)
                             if output == "FAILED":
                                endTime = ctime()
                                resultCollection("Logout of iSCSI Volume %s when initiator group is iqn1" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)

#end of iscsi initiator iqn_based
#start of iscsi Auth-Group,change the auth group to AuthGrp1
                if mountOutput[0] == "PASSED":
                   executeCmd('python setISCSIInitiatorGroup.py dedup.txt')
                   executeCmd('python setIscsiAuthGroup.py dedup.txt AuthGrp1')
                   #discovery iscsi volumes
                   executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
                   iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
                   time.sleep(30)
                   print iqnname
                   if iqnname==[]:
                      print "no iscsi volumes discovered on the client"
                      endTime = ctime()
                      resultCollection("no iscsi volumes discovered on the client when Auth-Group is AuthGrp1",["FAILED",""], startTime, endTime)
                   else:
                      output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                      time.sleep(30)
                      if output[0]=="PASSED":
                          device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                          device2 = (device[0].split('\n'))[0]
                          ### mount
                          time.sleep(10)
                          mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                          print  mountOutput
                          endTime = ctime()
                          if mountOutput[0] == "PASSED":
                            time.sleep(3)
                            output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                            time.sleep(20)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > authgrpmd5sum ' %(config['voliSCSIMountpoint%d' %(x)], testfile))
                            endTime = ctime()
                            result=executeCmd('diff basemd5sum authgrpmd5sum')
                            print result[0]
                            if result[0] == "PASSED":
                               print "Data is available after changing the AuthGroup to AuthGrp1"
                               resultCollection("Changing the Auth-group to AuthGrp1 on %s does not result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                            else:
                               print "Data is not available after changing the AuthGroup to AuthGrp1"
                               resultCollection("Changing the Auth-group to AuthGrp1 on %s is result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)
                         #unmount
                            executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                           #logout
                            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                            time.sleep(30)
                            if output == "FAILED":
                               endTime = ctime()
                               resultCollection("Logout of iSCSI Volume %s when Auth-Group is AuthGrp1" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                          else:
                             print " Mount Fail , Exiting......"
                             endTime = ctime()
                             resultCollection("Mounting the ISCSI volume %s got failed when Auth-Group is AuthGrp1"%(config['voliSCSIDatasetname%d' %(x)]),mountOutput[0],startTime, endTime)
                             endTime=ctime()
                             output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                             time.sleep(30)
                             if output == "FAILED":
                                endTime = ctime()
                                resultCollection("Logout of iSCSI Volume %s when Auth-Group is AuthGrp1" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)

#end of Auth-Group
#start of iscsi Auth-Method --CHAP
                if mountOutput[0] == "PASSED":
                   executeCmd('cp /etc/iscsi/iscsid.conf /etc/iscsi/iscsid.conf.bak')
                   time.sleep(10)
                   executeCmd('cp iscsiChap.conf /etc/iscsi/iscsid.conf')
                   print"iscsi conf file changed to iscsiChap.conf,waiting for 60 secs"
                   time.sleep(60)
                   executeCmd('python setIscsiAuthMethod.py dedup.txt chap')
                   #discovery iscsi volumes
                   executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
                   iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
                   print iqnname
                   if iqnname==[]:
                      print "no iscsi volumes discovered on the client"
                      endTime = ctime()
                      resultCollection("no iscsi volumes discovered on the client when Auth-Method is CHAP",["FAILED",""], startTime, endTime)
                   else:
                      output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                      time.sleep(30)
                      print output
                      if output[0]=="PASSED":
                          device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                          device2 = (device[0].split('\n'))[0]
                          ### mount
                          time.sleep(10)
                          mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                          print  mountOutput
                          endTime = ctime()
                          if mountOutput[0] == "PASSED":
                            time.sleep(3)
                            output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                            time.sleep(20)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > chapmd5sum ' %(config['voliSCSIMountpoint%d' %(x)], testfile))
                            endTime = ctime()
                            result=executeCmd('diff basemd5sum chapmd5sum')
                            print result[0]
                            if result[0] == "PASSED":
                               print "Data is available after changing the AuthMethod to CHAP "
                               resultCollection("Changing the Auth-Method to CHAP on %s does not result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                            else:
                               print "Data is not available after changing the AuthMethod to CHAP"
                               resultCollection("Changing the Auth-Method to CHAP on %s is result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)
                         #unmount
                            executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                           #logout
                            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                            time.sleep(30)
                            if output == "FAILED":
                               endTime = ctime()
                               resultCollection("Logout of iSCSI Volume %s when Auth-Method is CHAP" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                          else:
                             print " Mount Fail , Exiting......"
                             endTime = ctime()
                             resultCollection("Mounting the ISCSI volume %s got failed when Auth-Method is CHAP"%(config['voliSCSIDatasetname%d' %(x)]),mountOutput[0],startTime, endTime)
                             endTime=ctime()
                             output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                             time.sleep(30)
                             if output == "FAILED":
                                endTime = ctime()
                                resultCollection("Logout of iSCSI Volume %s when Auth-Method is CHAP" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)




#end of Auth-Method CHAP
#start of iscsi Auth-Method --MutualCHAP
                if mountOutput[0] == "PASSED":
                   executeCmd('cp iscsiMutualChap.conf /etc/iscsi/iscsid.conf')
                   print"iscsi conf file changed to iscsiMutualChap.conf,waiting for 60 secs"
                   time.sleep(60)
                   executeCmd('python setIscsiAuthMethod.py dedup.txt mutualchap')
                   #discovery iscsi volumes
                   executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
                   iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
                   print iqnname
                   if iqnname==[]:
                      print "no iscsi volumes discovered on the client"
                      endTime = ctime()
                      resultCollection("no iscsi volumes discovered on the client when Auth-Method is MutualCHAP",["FAILED",""], startTime, endTime)
                   else:
                      output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                      time.sleep(30)
                      print output
                      if output[0]=="PASSED":
                          device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                          device2 = (device[0].split('\n'))[0]
                          ### mount
                          time.sleep(10)
                          mountOutput=executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                          print  mountOutput
                          endTime = ctime()
                          if mountOutput[0] == "PASSED":
                            time.sleep(3)
                            output=executeCmd('mount | grep %s' %(config['voliSCSIMountpoint%d' %(x)]))
                            time.sleep(20)
                            executeCmd('md5sum mount/%s/%s | awk \'{print $1}\' > mutualchapmd5sum ' %(config['voliSCSIMountpoint%d' %(x)], testfile))
                            endTime = ctime()
                            result=executeCmd('diff basemd5sum mutualchapmd5sum')
                            print result[0]
                            if result[0] == "PASSED":
                               print "Data is available after changing the AuthMethod to MutualCHAP "
                               resultCollection("Changing the Auth-Method to MutualCHAP on %s does not result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                            else:
                               print "Data is not available after changing the AuthMethod to MutualCHAP"
                               resultCollection("Changing the Auth-Method to MutualCHAP on %s is result in DU  "%(config['voliSCSIDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)
                         #unmount
                            executeCmd('umount -rf mount/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                           #logout
                            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                            time.sleep(30)
                            if output == "FAILED":
                               endTime = ctime()
                               resultCollection("Logout of iSCSI Volume %s when Auth-Method is MutualCHAP" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                          else:
                             print " Mount Fail , Exiting......"
                             endTime = ctime()
                             resultCollection("Mounting the ISCSI volume %s got failed when Auth-Method is MutualCHAP"%(config['voliSCSIDatasetname%d' %(x)]),mountOutput[0],startTime, endTime)
                             endTime=ctime()
                             output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                             time.sleep(30)
                             if output == "FAILED":
                                endTime = ctime()
                                resultCollection("Logout of iSCSI Volume %s when Auth-Method is MutualCHAP" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)

executeCmd('cp /etc/iscsi/iscsid.conf.bak /etc/iscsi/iscsid.conf')

#assign back default access to all iscsi volumes
executeCmd('python setISCSIInitiatorGroup.py dedup.txt')
executeCmd('python setIscsiAuthMethod.py dedup.txt')
executeCmd('python setIscsiAuthGroup.py dedup.txt')

###############################################################################
import json
import requests
import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd, getoutput, getControllerInfo
nfsFlag = cifsFlag = iscsiFlag =  fcFlag = allFlag = 0
########### TestCase Execution Starts.. 
if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print "python PoolDedupExecution.py dedupconfig.txt nfs/cifs/iscsi/all IP PASSWD on/off filename "
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
         print "python PoolDedupExecution.py dedupconfig.txt nfs/cifs/iscsi/all  IP PASSWD on/off filename "
         exit()

ip= sys.argv[3]
print ip
dedupvalue = sys.argv[5]
passwd = sys.argv[4]
print passwd
if len(sys.argv) ==  7:
  testfile = sys.argv[6]
else:
  testfile = "textfile"
print "continuing"
executeCmd('mkdir -p mount1')
    ###NFS
if  nfsFlag == 1 or allFlag == 1:
    print "within nfs"
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
             print"found in config"
             PoolName = config['volPoolName%d' %(x)] 
             print"poolname in config"
             startTime=ctime()
             executeCmd('rm -rf mount1/%s/*'%(config['volMountpoint%d' %(x)]))
             executeCmd('umount -rf mount1/%s'%(config['volMountpoint%d' %(x)]))
             executeCmd('rm -rf mount1/%s'%(config['volMountpoint%d' %(x)]))
             executeCmd('mkdir -p mount1/%s' %(config['volMountpoint%d' %(x)]))
        ######  Mount and copy NFS ###############
             executeCmd('mount -t nfs %s:/%s mount1/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
             output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
             endTime=ctime()
             resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output,startTime, endTime)
             print"before mount"
             if output[0] == "PASSED":
                 print "mount passed"
                 #executeCmd('cp -v %s mount1/%s/%s' %(testfile, config['volMountpoint%d' %(x)],testfile))
                 time.sleep(3)
                 dedupRatio1 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                 print dedupRatio1
                 cmd1= 'zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\' ' %(config['volDatasetname%d' %(x)])
                 print cmd1
                 volused1= getControllerInfo(ip, passwd,cmd1,"output.txt")
                 print "used"+volused1
                 dr1=float(dedupRatio1[0:-2])
                 print dr1
                 for y in range (1, 2):
                   executeCmd("cp -v %s mount1/%s/%s"%(testfile,config['volMountpoint%d' %(x)], testfile +'%d' %(y)))
                   time.sleep(10)
                 dedupRatio2 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                 print dedupRatio2
                 dr2= float(dedupRatio2[0:-2])
                 print dr2
                 cmd2= ' zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\' ' %(config['volDatasetname%d' %(x)])
                 volused2=getControllerInfo(ip, passwd,cmd2,"output.txt")
                 print volused2
             endTime=ctime()
             executeCmd('umount -rf mount1/%s'%(config['volMountpoint%d' %(x)]))
             if  output[0] == "PASSED":
                 print"within pass"
                 if  dedupvalue == "on" and dr2 > dr1 and float(volused2) > float(volused1):
                     print "Dedup is ON and working"
                     resultCollection("Dedup is enabled and working on\'%s\' using %s " %(PoolName,config['volDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                 elif  dedupvalue == "off" and dr2 == dr1 and float(volused2) > float(volused1):
                      print "Dedup is OFF and working"
                      resultCollection("Dedup is Disabled and working on\'%s\' using %s " %(PoolName,config['volDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                 else:
                     resultCollection("Dedup Feature is not working on\'%s\' using %s " %(PoolName,config['volDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)

             else:
                  endTime=ctime()
                  resultCollection("Mounting the volume %s failed"%(config['volDatasetname%d' %(x)]),["Mount Failed", ''],startTime, endTime)
                  
          
             

#############  CIFS ###############
if  cifsFlag ==1 or allFlag ==1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
             PoolName = config['volCifsPoolName%d' %(x)]
             print PoolName
             startTime=ctime()
             executeCmd('rm -rf mount1/%s/*'%(config['volCifsMountpoint%d' %(x)]))
             executeCmd('umount -rf mount1/%s'%(config['volCifsMountpoint%d' %(x)]))
             executeCmd('rm -rf mount1/%s'%(config['volCifsMountpoint%d' %(x)]))
             startTime = ctime()
             executeCmd('mkdir -p mount1/%s' %(config['volCifsMountpoint%d' %(x)]))
        ###### Mount and Copy CIFS #################
             executeCmd(' mount -t cifs //%s/%s mount1/%s -o username=%suser -o password=%suser' %(config['volCifsIPAddress%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsAccountName%d' %(x)], config['volCifsAccountName%d' %(x)]))
             output=executeCmd('mount | grep %s' %(config['volCifsMountpoint%d' %(x)]))
             endTime=ctime()
             resultCollection("Mount of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), output,startTime, endTime)
             if  output[0]=="PASSED":
                 #executeCmd('cp -v %s mount1/%s/%s' %(testfile, config['volCifsMountpoint%d' %(x)],testfile))
                 #time.sleep(3)
                 dedupRatio1 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                 print "dedupRatio1"
                 print dedupRatio1
                 cmd1='zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\'' %(config['volCifsDatasetname%d' %(x)])
                 print cmd1
                 volused1=getControllerInfo(ip, passwd,cmd1,"output5.txt")
                 print "vol used "+volused1
                 dr1=float(dedupRatio1[0:-2])
                 print "dedupratio1"
                 print dr1

                 for y in range (1, 3):
                     executeCmd("cp -v %s mount1/%s/%s" %(testfile,config['volCifsMountpoint%d' %(x)], testfile +'%d' %(y)))
                     time.sleep(10)
                 dedupRatio2 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                 print dedupRatio2
                 dr2= float(dedupRatio2[0:-2])
                 print "dedup ratio2"
                 print dr2
                 cmd2=' zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\'' %(config['volCifsDatasetname%d' %(x)])
                 volused2=getControllerInfo(ip, passwd,cmd2,"output5.txt")
                 print "vol used2 "+volused2
             endTime=ctime()
             executeCmd('umount -rf mount1/%s'%(config['volCifsMountpoint%d' %(x)]))
             if  output[0] == "PASSED":
                   if  dedupvalue == "on" and dr2 > dr1 and float(volused2) > float(volused1):
                       print "Dedup is ON and working"
                       resultCollection("Dedup is enabled and working on\'%s\' using %s " %(PoolName,config['volCifsDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                   elif  dedupvalue == "off" and dr2 == dr1 and float(volused2) > float(volused1):
                       print "Dedup is OFF and working"
                       resultCollection("Dedup is Disabled and working on\'%s\'using %s " %(PoolName,config['volCifsDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                   else:
                      resultCollection("Dedup Feature is not working on\'%s\' using %s " %(PoolName,config['volCifsDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)
             else:
                  print " Mount Fail , Exiting......"
                  endTime=ctime()
                  resultCollection("Mounting the CIFS volume %s got failed"%(config['volCifsDatasetname%d' %(x)]),output,startTime, endTime)
                 

#####ISCSI
if  iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
             PoolName = config['voliSCSIPoolName%d' %(x)]
             executeCmd('rm -rf mount1/%s/*'%(config['voliSCSIMountpoint%d' %(x)]))
             executeCmd('umount -rf mount1/%s'%(config['voliSCSIMountpoint%d' %(x)]))
             #output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --logout | grep Logout' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
             executeCmd('rm -rf mount1/%s'%(config['voliSCSIMountpoint%d' %(x)]))
             startTime=ctime()
             executeCmd('mkdir -p mount1/%s' %(config['voliSCSIMountpoint%d' %(x)]))
             #################********************
              ### Discovery 
             executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
             iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
             print iqnname
             if iqnname==[]:
                print "no iscsi volumes discovered on the client"
                endTime = ctime()
                resultCollection("no iscsi volumes discovered on the client",["FAILED",""], startTime, endTime)
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
                   time.sleep(30)
                   #executeCmd('cp -v %s mount1/%s/%s' %(testfile, config['voliSCSIMountpoint%d' %(x)],sys.argv[3]))
                   dedupRatio1 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                   print dedupRatio1
                   dr1=float(dedupRatio1[0:-2])
                   cmd1='zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\'' %(config['voliSCSIDatasetname%d' %(x)])
                   volused1 = getControllerInfo(ip, passwd,cmd1,"output5.txt")
                   print volused1
                   for y in range (1, 3):
                     executeCmd("cp -v %s mount1/%s/%s" %(testfile,config['voliSCSIMountpoint%d' %(x)], testfile +'%d' %(y)))
                     time.sleep(30)
                   dedupRatio2 = getControllerInfo(ip, passwd,"zpool list %s | awk '{print $6}' | tail -n1" %(PoolName),"output.txt")
                   print dedupRatio2
                   dr2= float(dedupRatio2[0:-2])
                   cmd2=' zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\'' %(config['voliSCSIDatasetname%d' %(x)])
                   volused2 = getControllerInfo(ip, passwd,cmd2,"output5.txt")
                   print volused2
                   print "Comparing....."
                   endTime=ctime()
                 executeCmd('umount -rf mount1/%s'%(config['voliSCSIMountpoint%d' %(x)]))
                 if  mountOutput[0] == "PASSED":
                    if  dedupvalue == "on" and dr2 > dr1 and float(volused2) > float(volused1):
                      print "Dedup is ON and working"
                      resultCollection("Dedup is enabled and working on\'%s\' using %s "%(PoolName,config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                    elif  dedupvalue == "off" and dr2 == dr1 and float(volused2) > float(volused1):
                      print "Dedup is OFF and working"
                      resultCollection("Dedup is Disabled and working on\'%s\' using %s "%(PoolName,config['voliSCSIDatasetname%d' %(x)]),["PASSED", ' '],startTime, endTime)
                    else:
                      print "Dedup is not working"
                      resultCollection("Dedup Feature is not working on\'%s\' using %s "%(PoolName,config['voliSCSIDatasetname%d' %(x)]),["FAILED", ' '],startTime, endTime)

      ###### LOGOUT ISCSI from Luns ############
                    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                    if output == "FAILED":
                     endTime = ctime()
                     resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                 
                 else:
                  print " Mount Fail , Exiting......"
                  endTime=ctime()
                  output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
                  if output == "FAILED":
                     endTime = ctime()
                     resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output, startTime, endTime)
                  resultCollection("Mounting the ISCSI volume %s got failed"%(config['voliSCSIDatasetname%d' %(x)]),output[0],startTime, endTime)

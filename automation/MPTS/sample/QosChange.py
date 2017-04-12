import json
import requests
import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd, getoutput, getControllerInfo
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if len(sys.argv) < 5:
    print "Argument is not correct.. Correct way as below"
    print "python QosChange.py config.txt ISCSI/NFS/CIFS/FC/ALL 0(IOPS) 0(throughput)"
    exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if sys.argv[2].lower() == "%s" %("nfs"):
    nfsFlag = 1;
elif sys.argv[2].lower() == "%s" %("cifs"):
    cifsFlag = 1;
elif sys.argv[2].lower() == "%s" %("fc"):
    fcFlag = 1;
elif sys.argv[2].lower() == "%s" %("iscsi"):
    iscsiFlag = 1;
elif sys.argv[2].lower() == "%s" %("all"):
    allFlag = 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python QosChange.py dedup.txt NFS/CIFS/ISCSI/FC 0(IOPS) 0(throughput)"
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
volIops = sys.argv[3]
tpvalue = sys.argv[4]
ip = sys.argv[5]
passwd = sys.argv[6]

###### To Change the IOPS
#####List Filesystem
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
    filesystem_id = filesystem['groupid']
    filesystem_name = filesystem['name']
    ###NFS
    if nfsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_NFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                iopscontrolled = "%s" %(config['volIopscontrol%d' %(x)])
                throughputcontrolled = "%s" %(config['volTpcontrol%d' %(x)])
                datasetname = "%s" %(config['volDatasetname%d' %(x)])
                tsmname = "%s" %(config['volTSMName%d' %(x)])
                accountname = "%s" %(config['volAccountName%d' %(x)])
                searchname = datasetname + accountname + tsmname
                print datasetname
                print tsmname
                print accountname
                print searchname
                print "iopscontrolled = "+iopscontrolled
                print "throughputcontrolled = "+throughputcontrolled
                if iopscontrolled == "true" and throughputcontrolled == "false":
                  querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                  resp_updateNFS = sendrequest(stdurl, querycommand)
                  cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  iops= getControllerInfo(ip, passwd,cmd1,"output.txt")
                  print "volIops="+ volIops
                  print "rengiops="+ iops
                  endTime=ctime()
                  if int(volIops) == int(iops):
                   print "Changing IOPS updated in Reng list on "+ datasetname +": PASSED"
                   resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                  elif int(volIops) != int(rengiops):
                   print "Changing IOPS updated in Reng list on "+ datasetname +": FAILED" 
                   resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                  filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
                  print ">>>> NFS >>>>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                     querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                     resp_updateNFS = sendrequest(stdurl, querycommand)
                     cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     throughput= getControllerInfo(ip, passwd,cmd2,"output.txt")
                     print "throughput="+ tpvalue
                     print "rengthroughput="+ throughput
                     endTime=ctime()
                     if int(tpvalue) == int(throughput):
                      print "Changing throughput updated in Reng list on "+ datasetname +": PASSED"
                      resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(throughput) != int(rengthroughput):
                      print "Changing throughput updated in Reng list on "+datasetname +": FAILED"
                      resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
                     print ">>>> NFS >>>>updated %s" %(filesystem_name)
                else:
                    print "Volume %s has the problem in configuration" %s(config['volDatasetname%d' %(x)])
    ## #CIFS
    if cifsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                iopscontrolled = "%s" %(config['volCifsIopscontrol%d' %(x)])
                throughputcontrolled = "%s" %(config['volCifsTpcontrol%d' %(x)])
                print "iopscontrolled = "+iopscontrolled
                print "throughputcontrolled = "+throughputcontrolled
                datasetname = "%s" %(config['volCifsDatasetname%d' %(x)])
                tsmname = "%s" %(config['volCifsTSMName%d' %(x)])
                accountname = "%s" %(config['volCifsAccountName%d' %(x)])
                searchname = datasetname + accountname + tsmname
                print datasetname
                print tsmname
                print accountname
                print searchname
                if iopscontrolled == "true" and throughputcontrolled == "false":
                   querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                   resp_updateCIFS = sendrequest(stdurl, querycommand)
                   cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                   iops= getControllerInfo(ip, passwd,cmd1,"output.txt")
                   print "volIops="+ volIops
                   print "rengiops="+ iops
                   endTime=ctime()
                   if int(volIops) == int(iops):
                      print "Changing IOPS updated in Reng list on "+ datasetname +": PASSED"
                      resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                   elif int(volIops) != int(rengiops):
                      print "Changing IOPS updated in Reng list on "+ datasetname +": FAILED"
                      resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                   filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
                   print ">>>> CIFS >>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                    querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                    resp_updateCIFS = sendrequest(stdurl, querycommand)
                    cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                    throughput= getControllerInfo(ip, passwd,cmd2,"output.txt")
                    print "throughput="+ tpvalue
                    print "rengthroughput="+ throughput
                    endTime=ctime()
                    if int(tpvalue) == int(throughput):
                        print "Changing throughput updated in Reng list on "+ datasetname +": PASSED"
                        resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                    elif int(tpvalue) != int(rengthroughput):
                       print "Changing throughput updated in Reng list on "+datasetname +": FAILED"
                       resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                    filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
                    print ">>>> CIFS >>updated %s" %(filesystem_name)
                else:
                    print "Volume %s has the problem in configuration" %s(config['volCifsDatasetname%d' %(x)])

    ###ISCSI
    if iscsiFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                iopscontrolled = "%s" %(config['voliSCSIIopscontrol%d' %(x)])
                throughputcontrolled = "%s" %(config['voliSCSITpcontrol%d' %(x)])
                print "iopscontrolled = "+iopscontrolled
                print "throughputcontrolled = "+throughputcontrolled
                datasetname = "%s" %(config['voliSCSIDatasetname%d' %(x)])
                tsmname = "%s" %(config['voliSCSITSMName%d' %(x)])
                accountname = "%s" %(config['voliSCSIAccountName%d' %(x)])
                searchname = datasetname + accountname + tsmname
                print datasetname
                print tsmname
                print accountname
                print searchname
                print "iopscontrolled = "+iopscontrolled
                print "throughputcontrolled = "+throughputcontrolled
                if iopscontrolled == "true" and throughputcontrolled == "false":
                     querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                     resp_updateISCSI = sendrequest(stdurl, querycommand)
                     cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                     iops= getControllerInfo(ip, passwd,cmd1,"output.txt")
                     print "volIops="+ volIops
                     print "rengiops="+ iops
                     endTime=ctime()
                     if int(volIops) == int(iops):
                         print "Changing IOPS updated in Reng list on "+ datasetname +": PASSED"
                         resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(volIops) != int(rengiops):
                         print "Changing IOPS updated in Reng list on "+ datasetname +": FAILED"
                         resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
                     print ">>>> ISCSI >> >> updated %s" %(filesystem_name) 
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                     querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                     resp_updateISCSI = sendrequest(stdurl, querycommand)
                     cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     throughput= getControllerInfo(ip, passwd,cmd2,"output.txt")
                     print "throughput="+ tpvalue
                     print "rengthroughput="+ throughput
                     endTime=ctime()
                     if int(tpvalue) == int(throughput):
                        print "Changing throughput updated in Reng list on "+ datasetname +": PASSED"
                        resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(tpvalue) != int(rengthroughput):
                        print "Changing throughput updated in Reng list on "+datasetname +": FAILED"
                        resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
                     print ">>>> ISCSI >> >> updated %s" %(filesystem_name)
                else:
                    print "Volume %s has the problem in configuration" %s(config['voliSCSIDatasetname%d' %(x)])



    ###FC
    if fcFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                iopscontrolled = "%s" %(config['volfcIopscontrol%d' %(x)])
                throughputcontrolled = "%s" %(config['volfcTpcontrol%d' %(x)])
                datasetname = "%s" %(config['volfcDatasetname%d' %(x)])
                tsmname = "%s" %(config['volfcTSMName%d' %(x)])
                accountname = "%s" %(config['volfcAccountName%d' %(x)])
                searchname = datasetname + accountname + tsmname
                print datasetname
                print tsmname
                print accountname
                print searchname
                print "iopscontrolled = "+iopscontrolled
                print "throughputcontrolled = "+throughputcontrolled
                if iopscontrolled == "true" and throughputcontrolled == "false":
                     querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                     resp_updateFC = sendrequest(stdurl, querycommand)
                     cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                     iops= getControllerInfo(ip, passwd,cmd1,"output.txt")
                     print "volIops="+ volIops
                     print "rengiops="+ iops
                     endTime=ctime()
                     if int(volIops) == int(iops):
                        print "Changing IOPS updated in Reng list on "+ datasetname +": PASSED"
                        resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(volIops) != int(rengiops):
                        print "Changing IOPS updated in Reng list on "+ datasetname +": FAILED"
                        resultCollection("Changing IOPS updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                     print ">>>> FC >>>> updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                     querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                     resp_updateFC = sendrequest(stdurl, querycommand)
                     cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     throughput= getControllerInfo(ip, passwd,cmd2,"output.txt")
                     print "throughput="+ tpvalue
                     print "rengthroughput="+ throughput
                     endTime=ctime()
                     if int(tpvalue) == int(throughput):
                       print "Changing throughput updated in Reng list on "+ datasetname +": PASSED"
                       resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(tpvalue) != int(rengthroughput):
                       print "Changing throughput updated in Reng list on "+datasetname +": FAILED"
                       resultCollection("Changing throuhput updated in Reng list on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                     print ">>>> FC >>>> updated %s" %(filesystem_name)
                else:
                        print "Volume %s has the problem in configuration" %s(config['volfcDatasetname%d' %(x)])

print "done"





'''
cmd2= ' zfs get -Hp all | grep %s | grep -w used | awk \'{print $3}\' ' %(config['volDatasetname%d' %(x)])
      volused2=getControllerInfo(ip, passwd,cmd2,"output.txt")
   resultCollection("Dedup Feature is not working on\'%s\'" %(PoolName),["FAILED", ' '],startTime, endTime)
'''

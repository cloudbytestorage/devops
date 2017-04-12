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
    print "python QosDatasetDelete.py config.txt ISCSI/NFS/CIFS/FC/ALL nodeip password devmanip password"
    exit()

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
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
    print "python QosDatasetDelete.py dedup.txt NFS/CIFS/ISCSI/FC nodeip password devmanip password"
    
nodeip = sys.argv[3]
nodepasswd = sys.argv[4]
devip =  sys.argv[5]
devpasswd = sys.argv[6]
###### To Change the IOPS
#####List Filesystem

def poolfunction():
                 poolcmd = 'echo > dbfile'
                 pooluuidnull=getControllerInfo(devip, devpasswd,poolcmd,"output.txt")
                 poolcmd1 = 'mysql -uroot -ptest cloud -e "select name,uuid from cb_pool where removed is NULL" > dbfile'
                 allpooluuid = getControllerInfo(devip, devpasswd,poolcmd1,"output.txt")
                 poolcmd2 = 'cat dbfile | grep -w %s |awk \'{print $2}\'' % (poolname)
                 pooluuid = getControllerInfo(devip, devpasswd,poolcmd2,"output.txt")
                 print pooluuid
                 poolrengcmd1 =' reng list | grep -A 9 %s | grep \'Renegade IO remainder\' | awk \'{print$4}\' ' %(pooluuid[0:-1])
                 print poolrengcmd1
                 global poolrengiops
                 poolrengiops= getControllerInfo(nodeip, nodepasswd,poolrengcmd1,"output.txt")
                 print "poolrengremainediops= "+ poolrengiops
                 poolrengcmd2 = " reng list | grep -A 9 %s | grep 'Renegade throughput remainder' | awk '{print$4}'" %(pooluuid[0:-1])
                 print poolrengcmd2
                 global poolrengthroughput
                 poolrengthroughput= getControllerInfo(nodeip, nodepasswd,poolrengcmd2,"output.txt")
                 print "poolrengremained throughput="+ poolrengthroughput
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
    filesystem_id = filesystem['id']
    filesystem_name = filesystem['name']
    ###NFS
    if nfsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_NFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                poolname ="%s" %(config['volPoolName%d' %(x)])
                print poolname
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
                  print "inside iops loop"
                  poolfunction()
                  poolrengiops1 = poolrengiops
                  print "poolrengiops1= "+ poolrengiops1
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = int(voliops)
                  print "volumeusediops="
                  print volIops
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteNFS = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteNFS)
                  response = json.loads(resp_deleteNFS.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                   print errorstatus
                   resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                    print "Dataset \'%s\' deleted which had \'%s\' iops" %(datasetname,volIops)
                    poolfunction()
                    poolrengiops2= int(poolrengiops)
                    print "poolrengiops2= "
                    print poolrengiops2
                    endTime=ctime()
                    finalpoolrengiops= int(poolrengiops1) + volIops
                    print "finalpoolrengiops="
                    print finalpoolrengiops
                    if poolrengiops2 == finalpoolrengiops:
                        print "Pool QoS change Post Dataset Deletion passed"
                        resultCollection("Pool QoS change Post Dataset Deletion passed on iops controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                    else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on iops controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                elif iopscontrolled == "false" and throughputcontrolled == "true":         
                  print "inside throughput loop"
                  poolfunction()
                  poolrengthroughput1 =poolrengthroughput
                  print "poolrengthroughput1= "+ poolrengthroughput1
                  volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                  volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                  tpvalue = int(volthroughput)
                  print "volrengthroughput="
                  print tpvalue
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteNFS = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteNFS)
                  response = json.loads(resp_deleteNFS.text)
                  if 'errortext' in str(response):
                      errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                      print errorstatus
                      resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                     print "Dataset \'%s\' deleted which had  \'%s\' throughput" %(datasetname,tpvalue)
                     poolfunction()
                     poolrengthroughput2 = int(poolrengthroughput)
                     print "poolrengthroughput2="
                     print poolrengthroughput2
                     finalpoolrengthroughput = int(poolrengthroughput1) + tpvalue
                     print "finalpoolrengthroughput"
                     print finalpoolrengthroughput
                     endTime=ctime()
                     if poolrengthroughput2 == finalpoolrengthroughput:
                          print "Pool QoS change Post Dataset Deletion passed"
                          resultCollection("Pool QoS change Post Dataset Deletion passed on throughput controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                     else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on throughput controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)


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
                poolname ="%s" %(config['volCifsPoolName%d' %(x)])
                print poolname
                datasetname = "%s" %(config['volCifsDatasetname%d' %(x)])
                tsmname = "%s" %(config['volCifsTSMName%d' %(x)])
                accountname = "%s" %(config['volCifsAccountName%d' %(x)])
                searchname = datasetname + accountname + tsmname
                print datasetname
                print tsmname
                print accountname
                print searchname
                if iopscontrolled == "true" and throughputcontrolled == "false":
                  print "inside iops loop"
                  poolfunction()
                  poolrengiops1 = poolrengiops
                  print "poolrengiops1= "+ poolrengiops1
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = int(voliops)
                  print "volumeusediops="
                  print volIops
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteCIFS = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteCIFS)
                  response = json.loads(resp_deleteCIFS.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                   print errorstatus
                   resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                    print "Dataset \'%s\' deleted which had \'%s\' iops" %(datasetname,volIops)
                    poolfunction()
                    poolrengiops2= int(poolrengiops)
                    print "poolrengiops2= "
                    print poolrengiops2
                    endTime=ctime()
                    finalpoolrengiops= int(poolrengiops1) + volIops
                    print "finalpoolrengiops="
                    print finalpoolrengiops
                    if poolrengiops2 == finalpoolrengiops:
                        print "Pool QoS change Post Dataset Deletion passed"
                        resultCollection("Pool QoS change Post Dataset Deletion passed on iops controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                    else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on iops controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                elif iopscontrolled == "false" and throughputcontrolled == "true":         
                  print "inside throughput loop"
                  poolfunction()
                  poolrengthroughput1 =poolrengthroughput
                  print "poolrengthroughput1= "+ poolrengthroughput1
                  volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                  volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                  tpvalue = int(volthroughput)
                  print "volrengthroughput="
                  print tpvalue
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteCIFS = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteCIFS)
                  response = json.loads(resp_deleteCIFS.text)
                  if 'errortext' in str(response):
                      errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                      print errorstatus
                      resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                     print "Dataset \'%s\' deleted which had  \'%s\' throughput" %(datasetname,tpvalue)
                     poolfunction()
                     poolrengthroughput2 = int(poolrengthroughput)
                     print "poolrengthroughput2="
                     print poolrengthroughput2
                     finalpoolrengthroughput = int(poolrengthroughput1) + tpvalue
                     print "finalpoolrengthroughput"
                     print finalpoolrengthroughput
                     endTime=ctime()
                     if poolrengthroughput2 == finalpoolrengthroughput:
                          print "Pool QoS change Post Dataset Deletion passed"
                          resultCollection("Pool QoS change Post Dataset Deletion passed on throughput controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                     else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on throughput controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                else:
                    print "Volume %s has the problem in configuration" %s(config['volCifsDatasetname%d' %(x)])

    ###ISCSI
    if iscsiFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                poolname ="%s" %(config['voliSCSIPoolName%d' %(x)])
                print poolname
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
                  print "inside iops loop"
                  poolfunction()
                  poolrengiops1 = poolrengiops
                  print "poolrengiops1= "+ poolrengiops1
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = int(voliops)
                  print "volumeusediops="
                  print volIops
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteISCSI = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteISCSI)
                  response = json.loads(resp_deleteISCSI.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                   print errorstatus
                   resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                    print "Dataset \'%s\' deleted which had \'%s\' iops" %(datasetname,volIops)
                    poolfunction()
                    poolrengiops2= int(poolrengiops)
                    print "poolrengiops2= "
                    print poolrengiops2
                    endTime=ctime()
                    finalpoolrengiops= int(poolrengiops1) + volIops
                    print "finalpoolrengiops="
                    print finalpoolrengiops
                    if poolrengiops2 == finalpoolrengiops:
                        print "Pool QoS change Post Dataset Deletion passed"
                        resultCollection("Pool QoS change Post Dataset Deletion passed on iops controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                    else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on iops controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                elif iopscontrolled == "false" and throughputcontrolled == "true":         
                  print "inside throughput loop"
                  poolfunction()
                  poolrengthroughput1 =poolrengthroughput
                  print "poolrengthroughput1= "+ poolrengthroughput1
                  volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                  volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                  tpvalue = int(volthroughput)
                  print "volrengthroughput="
                  print tpvalue
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteISCSI = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteISCSI)
                  response = json.loads(resp_deleteISCSI.text)
                  if 'errortext' in str(response):
                      errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                      print errorstatus
                      resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                     print "Dataset \'%s\' deleted which had  \'%s\' throughput" %(datasetname,tpvalue)
                     poolfunction()
                     poolrengthroughput2 = int(poolrengthroughput)
                     print "poolrengthroughput2="
                     print poolrengthroughput2
                     finalpoolrengthroughput = int(poolrengthroughput1) + tpvalue
                     print "finalpoolrengthroughput"
                     print finalpoolrengthroughput
                     endTime=ctime()
                     if poolrengthroughput2 == finalpoolrengthroughput:
                          print "Pool QoS change Post Dataset Deletion passed"
                          resultCollection("Pool QoS change Post Dataset Deletion passed on throughput controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                     else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on throughput controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                else:
                    print "Volume %s has the problem in configuration" %s(config['voliSCSIDatasetname%d' %(x)])



    ###FC
    if fcFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                poolname ="%s" %(config['volPoolName%d' %(x)])
                print poolname
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
                  print "inside iops loop"
                  poolfunction()
                  poolrengiops1 = poolrengiops
                  print "poolrengiops1= "+ poolrengiops1
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = int(voliops)
                  print "volumeusediops="
                  print volIops
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteFC = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteFC)
                  response = json.loads(resp_deleteFC.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                   print errorstatus
                   resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                    print "Dataset \'%s\' deleted which had \'%s\' iops" %(datasetname,volIops)
                    poolfunction()
                    poolrengiops2= int(poolrengiops)
                    print "poolrengiops2= "
                    print poolrengiops2
                    endTime=ctime()
                    finalpoolrengiops= int(poolrengiops1) + volIops
                    print "finalpoolrengiops="
                    print finalpoolrengiops
                    if poolrengiops2 == finalpoolrengiops:
                        print "Pool QoS change Post Dataset Deletion passed"
                        resultCollection("Pool QoS change Post Dataset Deletion passed on iops controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                    else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on iops controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                elif iopscontrolled == "false" and throughputcontrolled == "true":         
                  print "inside throughput loop"
                  poolfunction()
                  poolrengthroughput1 =poolrengthroughput
                  print "poolrengthroughput1= "+ poolrengthroughput1
                  volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                  volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                  tpvalue = int(volthroughput)
                  print "volrengthroughput="
                  print tpvalue
                  querycommand='command=deleteFileSystem&id=%s' %(id)
                  resp_deleteFC = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_deleteFC)
                  response = json.loads(resp_deleteFC.text)
                  if 'errortext' in str(response):
                      errorstatus = str(response['deleteFileSystemResponse']['errortext'])
                      print errorstatus
                      resultCollection("Deletion of Dataset \'%s\' failed not able to test Pool QoS change Post Dataset Deletion " %(datasetname),["FAILED", ' '],startTime, endTime)
                  else:
                     print "Dataset \'%s\' deleted which had  \'%s\' throughput" %(datasetname,tpvalue)
                     poolfunction()
                     poolrengthroughput2 = int(poolrengthroughput)
                     print "poolrengthroughput2="
                     print poolrengthroughput2
                     finalpoolrengthroughput = int(poolrengthroughput1) + tpvalue
                     print "finalpoolrengthroughput"
                     print finalpoolrengthroughput
                     endTime=ctime()
                     if poolrengthroughput2 == finalpoolrengthroughput:
                          print "Pool QoS change Post Dataset Deletion passed"
                          resultCollection("Pool QoS change Post Dataset Deletion passed on throughput controlled \'%s\' and \'%s\'   " %(datasetname,poolname),["PASSED", ' '],startTime, endTime)
                     else:
                         print "Pool QoS change Post Dataset Deletion failed"
                         resultCollection("Pool QoS change Post Dataset Deletion failed on throughput controlled \'%s\' and \'%s\'  " %(datasetname,poolname),["FAILED", ' '],startTime, endTime)
                else:
                        print "Volume %s has the problem in configuration" %s(config['volfcDatasetname%d' %(x)])

print "done"






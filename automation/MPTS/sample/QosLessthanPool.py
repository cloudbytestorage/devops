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
    print "python QosChange.py config.txt ISCSI/NFS/CIFS/FC/ALL nodeip password devmanip password"
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
    print "python QosLessThanPool.py dedup.txt NFS/CIFS/ISCSI/FC nodeip password devmanip password"
    
nodeip = sys.argv[3]
nodepasswd = sys.argv[4]
devip =  sys.argv[5]
devpasswd = sys.argv[6]
####Get the uuid of pool to access the reng datails######
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
                #########end of pool reng#######33
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
                poolfunction() 
                if iopscontrolled == "true" and throughputcontrolled == "false":
                  print "inside iops loop"
                  #####volIops=====poolremainderiops+volumeusediops+1##########
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = 1 + int(poolrengiops) + int(voliops)
                  print volIops
                  querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                  resp_updateNFS = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_updateNFS)
                  response = json.loads(resp_updateNFS.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['updateqosresponse']['errortext'])
                   print errorstatus
                  cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  iops= getControllerInfo(nodeip, nodepasswd,cmd1,"output.txt")
                  print "volIops="
                  print volIops
                  print "rengiops="+ iops
                  endTime=ctime()
                  if int(volIops) != int(iops) and 'errortext' in str(response):
                    print "Changing IOPS more than pool failed on "+ datasetname +": PASSED"
                    resultCollection("Changing IOPS more than pool on\'%s\' failed." %(datasetname),["PASSED", ' '],startTime, endTime)
                  elif int(volIops) == int(iops) and 'errortext' not in str(response):
                    print "Changing IOPS more than pool Possible on "+ datasetname +": FAILED" 
                    resultCollection("Changing IOPS more than pool Possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                  filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
                  print ">>>> NFS >>>>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                     print "inside throughput loop"
                     volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                     tpvalue = 1 + int(poolrengthroughput) + int(volthroughput)
                     print tpvalue
                     querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                     resp_updateNFS = sendrequest(stdurl, querycommand)
                     filesave("logs/updateQosGroup.txt", "w",resp_updateNFS)
                     response = json.loads(resp_updateNFS.text)
                     if 'errortext' in str(response):
                         errorstatus = str(response['updateqosresponse']['errortext'])
                         print errorstatus
                     cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     throughput= getControllerInfo(nodeip, nodepasswd,cmd2,"output.txt")
                     print "throughput="
                     print tpvalue
                     print "rengthroughput="+ throughput
                     endTime=ctime()
                     if int(tpvalue) != int(throughput) and 'errortext' in str(response):
                      print "Changing throughput more than pool failed on "+ datasetname +": PASSED"
                      resultCollection("Changing throuhput  more than pool is failed on \'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(throughput) == int(rengthroughput) and 'errortext' not in str(response):
                      print "Changing throughput more than pool possible on  "+datasetname +": FAILED"
                      resultCollection("Changing throuhput more than pool is possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
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
                poolfunction() 
                if iopscontrolled == "true" and throughputcontrolled == "false":
                   volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                   voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                   volIops = 1 + int(poolrengiops) + int(voliops)
                   print volIops
                   querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                   resp_updateCIFS = sendrequest(stdurl, querycommand)
                   filesave("logs/updateQosGroup.txt", "w",resp_updateCIFS)
                   response = json.loads(resp_updateCIFS.text)
                   if 'errortext' in str(response):
                      errorstatus = str(response['updateqosresponse']['errortext'])
                      print errorstatus
                   cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                   iops= getControllerInfo(nodeip, nodepasswd,cmd1,"output.txt")
                   print "volIops="
                   print volIops
                   print "rengiops="+ iops
                   endTime=ctime()
                   if int(volIops) != int(iops) and 'errortext' in str(response):
                      print "Changing IOPS more than pool failed on "+ datasetname +": PASSED"
                      resultCollection("Changing IOPS more than pool on\'%s\' failed." %(datasetname),["PASSED", ' '],startTime, endTime)
                   elif int(volIops) == int(iops) and 'errortext' not in str(response):
                      print "Changing IOPS more than pool Possible on "+ datasetname +": FAILED"
                      resultCollection("Changing IOPS more than pool Possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                   filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
                   print ">>>> CIFS >>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                   volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                   volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                   tpvalue = 1 + int(poolrengthroughput) + int(volthroughput)
                   print tpvalue
                   querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                   resp_updateCIFS = sendrequest(stdurl, querycommand)
                   filesave("logs/updateQosGroup.txt", "w",resp_updateCIFS)
                   response = json.loads(resp_updateCIFS.text)
                   if 'errortext' in str(response):
                     errorstatus = str(response['updateqosresponse']['errortext'])
                     print errorstatus
                   cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                   throughput= getControllerInfo(nodeip, nodepasswd,cmd2,"output.txt")
                   print "throughput="
                   print tpvalue
                   print "rengthroughput="+ throughput
                   endTime=ctime()
                   if int(tpvalue) != int(throughput) and 'errortext' in str(response):
                     print "Changing throughput more than pool failed on "+ datasetname +": PASSED"
                     resultCollection("Changing throuhput  more than pool is failed on \'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                   elif int(throughput) == int(rengthroughput) and 'errortext' not in str(response):
                      print "Changing throughput more than pool possible on  "+datasetname +": FAILED"
                      resultCollection("Changing throuhput more than pool is possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
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
                poolfunction() 
                if iopscontrolled == "true" and throughputcontrolled == "false":
                    volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                    voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                    volIops = 1 + int(poolrengiops) + int(voliops)
                    print volIops
                    querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                    resp_updateISCSI = sendrequest(stdurl, querycommand)
                    filesave("logs/updateQosGroup.txt", "w",resp_updateISCSI)
                    response = json.loads(resp_updateISCSI.text)
                    if 'errortext' in str(response):
                        errorstatus = str(response['updateqosresponse']['errortext'])
                        print errorstatus
                    cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                    iops= getControllerInfo(nodeip, nodepasswd,cmd1,"output.txt")
                    print "volIops="
                    print volIops
                    print "rengiops="+ iops
                    endTime=ctime()
                    if int(volIops) != int(iops) and 'errortext' in str(response):
                       print "Changing IOPS more than pool failed on "+ datasetname +": PASSED"
                       resultCollection("Changing IOPS more than pool on\'%s\' failed." %(datasetname),["PASSED", ' '],startTime, endTime)
                    elif int(volIops) == int(iops) and 'errortext' not in str(response):
                       print "Changing IOPS more than pool Possible on "+ datasetname +": FAILED"
                       resultCollection("Changing IOPS more than pool Possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                       filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
                       print ">>>> ISCSI >>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                    volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                    volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                    tpvalue = 1 + int(poolrengthroughput) + int(volthroughput)
                    print tpvalue
                    querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                    resp_updateISCSI = sendrequest(stdurl, querycommand)
                    filesave("logs/updateQosGroup.txt", "w",resp_updateISCSI)
                    response = json.loads(resp_updateISCSI.text)
                    if 'errortext' in str(response):
                     errorstatus = str(response['updateqosresponse']['errortext'])
                     print errorstatus
                    cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                    throughput= getControllerInfo(nodeip, nodepasswd,cmd2,"output.txt")
                    print "throughput="
                    print tpvalue
                    print "rengthroughput="+ throughput
                    querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                    resp_updateISCSI = sendrequest(stdurl, querycommand)
                    if 'errortext' in str(response):
                        errorstatus = str(response['updateqosresponse']['errortext'])
                        print errorstatus
                    cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                    throughput= getControllerInfo(nodeip, nodepasswd,cmd2,"output.txt")
                    print "throughput="
                    print tpvalue
                    print "rengthroughput="+ throughput
                    endTime=ctime()
                    if int(tpvalue) != int(throughput) and 'errortext' in str(response):
                        print "Changing throughput more than pool failed on "+ datasetname +": PASSED"
                        resultCollection("Changing throuhput  more than pool is failed on \'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                    elif int(throughput) == int(rengthroughput) and 'errortext' not in str(response):
                        print "Changing throughput more than pool possible on  "+datasetname +": FAILED"
                        resultCollection("Changing throuhput more than pool is possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
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
                poolfunction() 
                if iopscontrolled == "true" and throughputcontrolled == "false":
                  volcmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  voliops= getControllerInfo(nodeip, nodepasswd,volcmd1,"output.txt")
                  volIops = 1 + int(poolrengiops) + int(voliops)
                  print volIops
                  querycommand='command=updateQosGroup&id=%s&iops=%s' %(id, volIops)
                  resp_updateFC = sendrequest(stdurl, querycommand)
                  filesave("logs/updateQosGroup.txt", "w",resp_updateFC)
                  response = json.loads(resp_updateFC.text)
                  if 'errortext' in str(response):
                   errorstatus = str(response['updateqosresponse']['errortext'])
                   print errorstatus
                  cmd1 ='reng list | grep -A 6 %s | grep \'Renegade IO limit\' | awk \'{print $4}\' ' %(searchname)
                  iops= getControllerInfo(nodeip, nodepasswd,cmd1,"output.txt")
                  print "volIops="
                  print volIops
                  print "rengiops="+ iops
                  endTime=ctime()
                  if int(volIops) != int(iops) and 'errortext' in str(response):
                    print "Changing IOPS more than pool failed on "+ datasetname +": PASSED"
                    resultCollection("Changing IOPS more than pool on\'%s\' failed." %(datasetname),["PASSED", ' '],startTime, endTime)
                  elif int(volIops) == int(iops) and 'errortext' not in str(response):
                    print "Changing IOPS more than pool Possible on "+ datasetname +": FAILED" 
                    resultCollection("Changing IOPS more than pool Possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                  filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                  print ">>>> FC >>>>updated %s" %(filesystem_name)
                elif iopscontrolled == "false" and throughputcontrolled == "true":
                     volcmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     volthroughput= getControllerInfo(nodeip, nodepasswd,volcmd2,"output.txt")
                     tpvalue = 1 + int(poolrengthroughput) + int(volthroughput) 
                     print tpvalue
                     querycommand='command=updateQosGroup&id=%s&throughput=%s' %(id, tpvalue)
                     resp_updateFC = sendrequest(stdurl, querycommand)
                     filesave("logs/updateQosGroup.txt", "w",resp_updateFC)
                     response = json.loads(resp_updateFC.text)
                     if 'errortext' in str(response):
                         errorstatus = str(response['updateqosresponse']['errortext'])
                         print errorstatus
                     cmd2 = 'reng list | grep -A 6 %s | grep \'Renegade throughput limit\' | awk \'{print $4}\' ' %(searchname)
                     throughput= getControllerInfo(nodeip, nodepasswd,cmd2,"output.txt")
                     print "throughput="
                     print tpvalue
                     print "rengthroughput="+ throughput
                     endTime=ctime()
                     if int(tpvalue) != int(throughput) and 'errortext' in str(response):
                      print "Changing throughput more than pool failed on "+ datasetname +": PASSED"
                      resultCollection("Changing throuhput  more than pool is failed on \'%s\'" %(datasetname),["PASSED", ' '],startTime, endTime)
                     elif int(throughput) == int(rengthroughput) and 'errortext' not in str(response):
                      print "Changing throughput more than pool possible on  "+datasetname +": FAILED"
                      resultCollection("Changing throuhput more than pool is possible on\'%s\'" %(datasetname),["FAILED", ' '],startTime, endTime)
                     filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                     print ">>>> FC >>>> updated %s" %(filesystem_name)
                else:
                        print "Volume %s has the problem in configuration" %s(config['volfcDatasetname%d' %(x)])

print "done"






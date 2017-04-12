import json
import requests
from hashlib import md5
import fileinput
import subprocess
import sys
import time
from time import ctime
from cbrequest import sendrequest,filesave, filesave1, timetrack, queryAsyncJobResult, resultCollection, configFile, executeCmd, createSFTPConnection, getControllerInfo

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python Compression.py config.txt CIFS/NFS/iSCSI/FC/ALL on/off"
    exit()

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
    print "python Compression.py config.txt CIFS/NFS/iSCSI/FC/ALL on/off"
    exit()

compvalue = sys.argv[3]

#####List Filesystem
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
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateNFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateNFS.text", "w", resp_updateNFS)
                response = json.loads(resp_updateNFS.text)
                #print response
                if "errortext" in str(response):
                    errorstatus = str(response['updateFileSystemResponse']['errortext'])
                    print errorstatus
                    endTime=ctime()
                    resultCollection("Failed to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volDatasetname%d' %(x)]),["FAILED", ''],startTime,endTime)
                else:
                    print "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volDatasetname%d' %(x)])
                    endTime=ctime()
                    resultCollection("Compression value on  %s updated as\'%s\'" %(config['volDatasetname%d' %(x)],compvalue), ('PASSED', ' '), startTime, endTime)
                
    ###CIFS
    if cifsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateCIFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateCIFS.text", "w", resp_listFileSystem)
                response = json.loads(resp_updateCIFS.text)
                #print response
                if "errortext" in str(response):
                    errorstatus = str(response['updateFileSystemResponse']['errortext'])
                    print errorstatus
                    endTime=ctime()
                    resultCollection("Failed to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volCifsDatasetname%d' %(x)]),["FAILED", ''],startTime,endTime)
                else:
                    print "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volCifsDatasetname%d' %(x)])
                    endTime=ctime()
                    resultCollection("Compression value on  %s updated as\'%s\'" %(config['volCifsDatasetname%d' %(x)],compvalue), ('PASSED', ' '), startTime, endTime)



    ###ISCSI
    if iscsiFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                id = filesystem_id
                startTime=ctime()
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateISCSI = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateISCSI.text", "w", resp_listFileSystem)
                response = json.loads(resp_updateISCSI.text)
                #print response
                if "errortext" in str(response):
                    errorstatus = str(response['updateFileSystemResponse']['errortext'])
                    print errorstatus
                    endTime=ctime()
                    resultCollection("Failed to update Compression as \"%s\" on Dataset %s" %(compvalue,config['voliSCSIDatasetname%d' %(x)]),["FAILED", ''],startTime,endTime)
                else:
                    print "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['voliSCSIDatasetname%d' %(x)])
                    endTime=ctime()
                    resultCollection("Compression value on  %s updated as\'%s\'" %(config['voliSCSIDatasetname%d' %(x)],compvalue), ('PASSED', ' '), startTime, endTime)
'''
   ###FC
    if fcFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateFC = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateFC.text", "w", resp_listFileSystem)
                response = json.loads(resp_updateFC.text)
                #print response
                if "errortext" in str(response):
                    errorstatus = str(response['updateFileSystemResponse']['errortext'])
                    print errorstatus
                    endTime=ctime()
                    resultCollection("Failed to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volfcDatasetname%d' %(x)]),["FAILED", ''],startTime,endTime)
                else:
                    print "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volfcDatasetname%d' %(x)])
                    endTime=ctime()
                    resultCollection("Compression value on  %s updated as\'%s\'" %(config['volfcDatasetname%d' %(x)],compvalue), ('PASSED', ' '), startTime, endTime)
'''

print "done"







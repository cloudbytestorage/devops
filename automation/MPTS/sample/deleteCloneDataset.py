import json
import sys
import fileinput
from time import ctime
import time
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend, queryAsyncJobResult


###
# Provide configuration file storage protocol and IP address of controller as parameter
###
### for deleting clones use deleteCloneDataset.txt config file

#config = configFile(sys.argv);
#configfilename = configFileName(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = createSnp = deleteSnp = create = delete = 0;
prefixName = ''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 6:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python deleteCloneDataset.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> No_of_Clones Node_IP Password prefix_name(Optional)" + bcolors.ENDC
    exit()

config = configFile(sys.argv);


if sys.argv[2].lower() == "nfs":
    nfsFlag = 1
elif sys.argv[2].lower() == "cifs":
    cifsFlag = 1
elif sys.argv[2].lower() == "iscsi":
    iscsiFlag = 1
elif sys.argv[2].lower() == "fc":
    fcFlag = 1
elif sys.argv[2].lower() == "all":
    allFlag = 1
else:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python cloneDataset.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> snapshot_name No_of_Clones Node_IP Password prefix_name(Optional)" + bcolors.ENDC
    exit()

    
No_of_Clones = sys.argv[3]
IP = sys.argv[4]
passwd = sys.argv[5]

if len(sys.argv) == 7:
    prefixName = sys.argv[6]

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]


### Cifs
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        for i in range(1, int(No_of_Clones)+1):
            startTime = ctime()
            for filesystem in filesystems:
                filesystem_id = None
                cloneName = prefixName + '%s' %(config['volCifsDatasetname%d' %(x)]) + '%d' %(i)
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    filesystem_name = filesystem['name']
                    if filesystem_id is not None:
                        querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                        deleteCloneResp = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",deleteCloneResp)
                        data2 = json.loads(deleteCloneResp.text)
                        job_id = data2["deleteFileSystemResponse"]["jobid"]
                        rstatus=queryAsyncJobResult(stdurl, job_id);
                        print rstatus
                        endTime = ctime()
                        resultCollection("CIFS Clones %s Deletion" %(cloneName), rstatus,startTime,endTime)
                        print "\n%s is deleted\n" %(filesystem_name)
    print "All CIFS Clones are Deleted"
    time.sleep(2);

### NFS
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        for i in range(1, int(No_of_Clones)+1):
            startTime = ctime()
            for filesystem in filesystems:
                filesystem_id = None
                cloneName = prefixName + '%s' %(config['volDatasetname%d' %(x)]) + '%d' %(i)
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    filesystem_name = filesystem['name']
                    if filesystem_id is not None:
                        querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                        deleteCloneResp = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",deleteCloneResp)
                        data2 = json.loads(deleteCloneResp.text)
                        job_id = data2["deleteFileSystemResponse"]["jobid"]
                        rstatus=queryAsyncJobResult(stdurl, job_id);
                        print rstatus
                        endTime = ctime()
                        resultCollection("NFS Clones %s Deletion" %(cloneName), rstatus,startTime,endTime)
                        print "\n%s is deleted\n" %(filesystem_name)
    print "All NFS Clones are Deleted"
    time.sleep(2);


# iscsi
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        for i in range(1, int(No_of_Clones)+1):
            startTime = ctime()
            for filesystem in filesystems:
                filesystem_id = None
                cloneName = prefixName + '%s' %(config['voliSCSIDatasetname%d' %(x)]) + '%d' %(i)
                if filesystem['name'] == cloneName:
                    filesystem_id = filesystem['id']
                    filesystem_name = filesystem['name']
                    if filesystem_id is not None:
                        querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                        deleteCloneResp = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",deleteCloneResp)
                        data2 = json.loads(deleteCloneResp.text)
                        job_id = data2["deleteFileSystemResponse"]["jobid"]
                        rstatus=queryAsyncJobResult(stdurl, job_id);
                        print rstatus
                        endTime = ctime()
                        resultCollection("ISCSI Clones %s Deletion" %(cloneName), rstatus,startTime,endTime)
                        print "\n%s is deleted\n" %(filesystem_name)
    print "All ISCSI Clones are Deleted"
    time.sleep(2);

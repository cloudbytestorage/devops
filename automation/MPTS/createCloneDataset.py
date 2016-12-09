import json
import sys
import fileinput
import string
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend


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

if len(sys.argv) < 7:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python cloneDataset.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> snapshot_name No_of_Clones Node_IP Password Prefix_Name_For_Clone(Optional)" + bcolors.ENDC
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
    print bcolors.WARNING + "python cloneDataset.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> snapshot_name No_of_Clones Node_IP Password Prefix_Name_For_Clone(Optional)" + bcolors.ENDC
    exit()

    
snapshotName = sys.argv[3]
No_of_Clones = sys.argv[4]
IP = sys.argv[5]
passwd = sys.argv[6]

if len(sys.argv) == 8:
    prefixName = sys.argv[7]

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]


### Cifs
if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        startTime = ctime()
        for filesystem in filesystems:
            filesystem_id = None
            if filesystem['name'] == "%s" %(config['volCifsDatasetname%d' %(x)]):
                filesystem_id = filesystem['id']
                filesystem_name = filesystem['name']
                if filesystem_id is not None:
                    for i in range(1, int(No_of_Clones)+1):
                        #cloneName = prefixName + '%s' %(config['volCifsDatasetname%d' %(x)]) + '_%d' %(i)
                        cloneName = prefixName + '%s' %(config['volCifsDatasetname%d' %(x)]) + '%d' %(i)
                        path = None
                        querycommand = 'command=listStorageSnapshots&id=%s' %(filesystem_id)
                        respListSnapshot = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",respListSnapshot)
                        data2 = json.loads(respListSnapshot.text)
                        snapshots = data2["listDatasetSnapshotsResponse"]["snapshot"]
                        for snapshot in snapshots:
                            if snapshot['name'] == snapshotName:
                                path = snapshot['path'] ### path is the zfs name of the snapshot
                                break
                        if path == None:
                            endTime = ctime()
                            resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(filesystem_name), "FAILED", startTime, endTime)
                            print 'No snapshot is available'
                        
                        # create clone dataset
                        else:
                            querycommand = 'command=cloneDatasetSnapshot&id=%s&path=%s&clonename=%s&mountpoint=%s' %(filesystem_id, path, cloneName, cloneName)
                            out = sendrequest(stdurl, querycommand)
                            filesave("logs/ListSnapshot.txt", "w",out)
                            data3 = json.loads(out.text)
                            fsAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(filesystem_name), "dataset_result.txt")
                            cloneAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(cloneName), "clone_result.txt")
                            if not "errortext" in str(data3):
                                #endTime = ctime()
                                #resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["PASSED", ""], startTime, endTime)
                                #if fsAvlSpace == cloneAvlSpace:
                                endTime = ctime()
                                #resultCollection("Availavle space of clone dataset \"%s\" is same as parent dataset \"%s\": " %(cloneName, filesystem_name), ["PASSED", ""], startTime, endTime)
                                resultCollection("Creation of Clone \"%s\" is: " %(cloneName), ["PASSED", ""], startTime, endTime)
                                #else:
                                #    endTime = ctime()
                                #    resultCollection("Availavle space of clone dataset \"%s\" is different from parent dataset \"%s\": " %(cloneName, filesystem_name), ["FAILED", ""], startTime, endTime)
                            else:
                                errorstatus = str(data3['cloneDatasetSnapshot']['errortext'])
                                endTime = ctime()
                                resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["FAILED", errorstatus], startTime, endTime)

### NFS
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        startTime = ctime()
        for filesystem in filesystems:
            filesystem_id = None
            if filesystem['name'] == "%s" %(config['volDatasetname%d' %(x)]):
                filesystem_id = filesystem['id']
                filesystem_name = filesystem['name']
                if filesystem_id is not None:
                    for i in range(1, int(No_of_Clones)+1):
                        cloneName = prefixName + '%s' %(config['volDatasetname%d' %(x)]) + '%d' %(i)
                        path = None
                        querycommand = 'command=listStorageSnapshots&id=%s' %(filesystem_id)
                        respListSnapshot = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",respListSnapshot)
                        data2 = json.loads(respListSnapshot.text)
                        snapshots = data2["listDatasetSnapshotsResponse"]["snapshot"]
                        for snapshot in snapshots:
                            if snapshot['name'] == snapshotName:
                                path = snapshot['path']
                                break
                        if path == None:
                            endTime = ctime()
                            resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)
                            print 'No snapshot is available'
                        else:
                            querycommand = 'command=cloneDatasetSnapshot&id=%s&path=%s&clonename=%s&mountpoint=%s' %(filesystem_id, path, cloneName, cloneName)
                            out = sendrequest(stdurl, querycommand)
                            filesave("logs/ListSnapshot.txt", "w",out)
                            data3 = json.loads(out.text)
                            fsAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(filesystem_name), "dataset_result.txt")
                            cloneAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(cloneName), "clone_result.txt")
                            if not "errortext" in str(data3):
                                #resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["PASSED", ""])
                                #if fsAvlSpace == cloneAvlSpace:
                                #    endTime = ctime()
                                #    resultCollection("Availavle space of clone dataset \"%s\" is same as parent dataset \"%s\": " %(cloneName, filesystem_name), ["PASSED", ""], startTime, endTime)
                                #else:
                                endTime = ctime()
                                #    resultCollection("Availavle space of clone dataset \"%s\" is different from parent dataset \"%s\": " %(cloneName, filesystem_name), ["FAILED", ""], startTime, endTime)
                                resultCollection("Creation of Clone \"%s\" is: " %(cloneName), ["PASSED", ""], startTime, endTime)
                            else:
                                errorstatus = str(data3['cloneDatasetSnapshot']['errortext'])
                                endTime = ctime()
                                resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["FAILED", errorstatus], startTime, endTime)


# iscsi
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        for filesystem in filesystems:
            filesystem_id = None
            if filesystem['name'] == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                filesystem_id = filesystem['id']
                filesystem_name = filesystem['name']
                if filesystem_id is not None:
                    for i in range(1, int(No_of_Clones)+1):
                        cloneName = prefixName + '%s' %(config['voliSCSIDatasetname%d' %(x)]) + '%d' %(i)
                        path = None
                        querycommand = 'command=listStorageSnapshots&id=%s' %(filesystem_id)
                        respListSnapshot = sendrequest(stdurl, querycommand)
                        filesave("logs/ListSnapshot.txt", "w",respListSnapshot)
                        data2 = json.loads(respListSnapshot.text)
                        snapshots = data2["listDatasetSnapshotsResponse"]["snapshot"]
                        for snapshot in snapshots:
                            if snapshot['name'] == snapshotName:
                                path = snapshot['path']
                                break
                        if path == None:
                            endTime = ctime()
                            resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(filesystem_name), ["FAILED", ""], startTime, endTime)
                            print 'No snapshot is available'
                        else:
                            querycommand = 'command=cloneDatasetSnapshot&id=%s&path=%s&clonename=%s&mountpoint=%s' %(filesystem_id, path, cloneName, cloneName)
                            out = sendrequest(stdurl, querycommand)
                            filesave("logs/ListSnapshot.txt", "w",out)
                            data3 = json.loads(out.text)
                            fsAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(filesystem_name), "dataset_result.txt")
                            cloneAvlSpace = getControllerInfo(IP, passwd, "zfs list | grep %s | awk \'{print $3}\'" %(cloneName), "clone_result.txt")
                            if not "errortext" in str(data3):
                                #resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["PASSED", ""])
                                #if fsAvlSpace == cloneAvlSpace:
                                #    endTime = ctime()
                                #    resultCollection("Availavle space of clone dataset \"%s\" is same as parent dataset \"%s\": " %(cloneName, filesystem_name), ["PASSED", ""], startTime, endTime)
                                #else:
                                endTime = ctime()
                                #    resultCollection("Availavle space of clone dataset \"%s\" is different from parent dataset \"%s\": " %(cloneName, filesystem_name), ["FAILED", ""], startTime, endTime)
                                resultCollection("Creation of Clone \"%s\" is: " %(cloneName), ["PASSED", ""], startTime, endTime)
                            else:
                                errorstatus = str(data3['cloneDatasetSnapshot']['errortext'])
                                endTime = ctime()
                                resultCollection("Result for clone  \"%s\" creation on volume %s is: " %(cloneName, filesystem_name), ["FAILED", errorstatus], startTime, endTime)

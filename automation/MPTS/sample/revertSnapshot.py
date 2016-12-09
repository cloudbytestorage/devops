import json
import sys
import fileinput
from time import ctime
from cbrequest import configFile, executeCmd, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend


###
# Provide configuration file storage protocol and IP address of controller as parameter
###

config = configFile(sys.argv);
#configfilename = configFileName(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 4:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python revertSnapshot.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all)> Snapshot_name" + bcolors.ENDC
    exit()

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
    print "Argument is not correct.. Correct way as below"
    print "python createSnapshot.py config.txt NFS filename"
    print "python createSnapshot.py config.txt CIFS filename"
    print "python createSnapshot.py config.txt ISCSI filename"
    print "python createSnapshot.py config.txt ALL filename"
    print "python createSnapshot.py config.txt NFS CIFS filename -- This is not valid"
    print "python createSnapshot.py config.txt filename NFS CIFS  -- This is not valid"
    exit()

Name = sys.argv[3]
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
                    #Name = 's14_' + filesystem_name
                    querycommand = 'command=listStorageSnapshots&id=%s' %filesystem_id
                    resp_list_snapshot = sendrequest(stdurl, querycommand)
                    #filesave("logs/ListFileSystem.txt", "w", resp_list_snapshot)
                    data = json.loads(resp_list_snapshot.text)
                    snapshots = data['listDatasetSnapshotsResponse']['snapshot']
                    path = None
                    for snapshot in snapshots:
                        path = None
                        # Name concept of snapshot is not good enough, So it will revert only one snapshot of a volume
                        if snapshot['name'] == Name:
                            path = snapshot['path']
                            break
                    if path == None:
                        endTime = ctime()
                        resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)
                        print 'No snapshot available with this name'
                        #exit()
                    else:
                        querycommand = 'command=rollbackToSnapshot&id=%s&path=%s' %(filesystem_id, path)
                        out = sendrequest(stdurl, querycommand)
                        #resultCollection("Result for rollback snapshot:", out)
            
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
                    #Name = 's14_' + filesystem_name
                    querycommand = 'command=listStorageSnapshots&id=%s&name=' %filesystem_id
                    resp_list_snapshot = sendrequest(stdurl, querycommand)
                    #filesave("logs/create_snapshot.txt", "w",resp_list_snapshot)
                    data = json.loads(resp_list_snapshot.text)
                    snapshots = data['listDatasetSnapshotsResponse']['snapshot']
                    path = None
                    for snapshot in snapshots:
                        path = None
                        if snapshot['name'] == Name:
                            path = snapshot['path']
                            break

                    if path == None:
                        endTime = ctime()
                        resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)
                        print 'No snapshot available with this name'
                        #exit()
                    else:
                        querycommand = 'command=rollbackToSnapshot&id=%s&path=%s' %(filesystem_id, path)
                        out = sendrequest(stdurl, querycommand)
                        #resultCollection("Result for rollback snapshot:", out)

### ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        startTime = ctime()
        for filesystem in filesystems:
            filesystem_id = None
            if filesystem['name'] == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                filesystem_id = filesystem['id']
                filesystem_name = filesystem['name']
                if filesystem_id is not None:
                    #Name = 's14_' + filesystem_name
                    querycommand = 'command=listStorageSnapshots&id=%s&name=' %filesystem_id
                    resp_list_snapshot = sendrequest(stdurl, querycommand)
                    #filesave("logs/create_snapshot.txt", "w",resp_list_snapshot)
                    data = json.loads(resp_list_snapshot.text)
                    snapshots = data['listDatasetSnapshotsResponse']['snapshot']
                    path = None
                    for snapshot in snapshots:
                        path = None
                        if snapshot['name'] == Name:
                            path = snapshot['path']
                            break

                    if path == None:
                        endTime = ctime()
                        resultCollection("No snapshot is available for volume \"%s\" with provided name:" %(config['volDatasetname%d' %(x)]), ["FAILED", ""], startTime, endTime)
                        print 'No snapshot available with this name'
                        #exit()
                    else:
                        querycommand = 'command=rollbackToSnapshot&id=%s&path=%s' %(filesystem_id, path)
                        out = sendrequest(stdurl, querycommand)
                        #resultCollection("Result for rollback snapshot:", out)

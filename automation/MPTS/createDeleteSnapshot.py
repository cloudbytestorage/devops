import json
import sys
import fileinput
import string
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend

###
# Provide configuration file storage protocol and IP address of controller as parameter
###
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = tsmFlag = createSnp = deleteSnp = 0;
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 7:
    print bcolors.WARNING + "python createDeleteSnapshot.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all or tsm)> create/delete snapshot_name Node_IP Node_Passwd" + bcolors.ENDC
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
elif sys.argv[2].lower() == "tsm":
    tsmFlag = 1
else:
    print bcolors.WARNING + "python createDeleteSnapshot.py config.txt <storage_protocol(nfs/cifs/fc/iscsi/all or tsm)> create/delete snapshot_name Node_IP Node_Passwd" + bcolors.ENDC
    exit()

Name = sys.argv[4]
IP = sys.argv[5]
passwd = sys.argv[6]
if sys.argv[3].lower() == 'create':
    createSnp = 1
elif sys.argv[3].lower() == 'delete':
    deleteSnp = 1
else:
    print bcolors.FAIL + 'PARAMETER ERROR: '+ bcolors.ENDC + bcolors.WARNING + 'Fourth parameter should be \"create or delete\"...' + bcolors.ENDC
    exit()

# exit()
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

if tsmFlag == 1:
    #print tsmFlag
    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/ListTsm.txt", "w", resp_listTsm)
    dataTsm = json.loads(resp_listTsm.text)
    tsms = dataTsm['listTsmResponse']['listTsm']
    for x in range(1, int(config['Number_of_TSMs'])+1):
        startTime = ctime()
        for listTsm in tsms:
            tsmid = None
            if listTsm['name'] == "%s" %(config['tsmName%d' %(x)]):
                tsm_name = listTsm['name']
                tsm_dataset_id = listTsm['datasetid']
                if tsm_dataset_id is not None:
                    ### Create TSM level snapshot
                    if createSnp:
                        querycommand = 'command=createStorageSnapshot&id=%s&name=%s' %(tsm_dataset_id, Name)
                        resp_tsm_create_snp = sendrequest(stdurl, querycommand)
                        filesave("logs/create_tsm_snapshot.txt", "w",resp_tsm_create_snp)
                        tsmSnpResp = json.loads(resp_tsm_create_snp.text)
                        if 'errortext' in str(tsmSnpResp):
                            endTime = ctime()
                            errorstatus = str(tsmSnpResp['createStorageSnapshotResponse']['errortext'])

                            resultCollection("Result for snapshot \"%s\" creation on TSM %s is: " %(Name, config['tsmName%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                            
                        else:
                            getControllerInfo(IP, passwd, 'zfs list -t snapshot | grep %s' %(Name), "tsm_snapshot_result.txt")

                            ## verifying snapshot for cifs volumes
                            for p in range(1, int(config['Number_of_CIFSVolumes'])+1):
                                cifsresult = executeCmd('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['volCifsDatasetname%d' %(p)], Name))
                                if cifsresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volCifsDatasetname%d' %(p)]), cifsresult, startTime, endTime)

                            ## verifying snapshot for nfs volumes
                            for q in range(1, int(config['Number_of_NFSVolumes'])+1):
                                nfsresult = executeCmd('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['volDatasetname%d' %(q)], Name))
                                if nfsresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volDatasetname%d' %(q)]), nfsresult, startTime, endTime)

                            ## verifying snapshot for iscsi volumes
                            for r in range(1, int(config['Number_of_ISCSIVolumes'])+1):
                                iscsiresult = executeCmd('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['voliSCSIDatasetname%d' %(r)], Name))
                                if iscsiresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(r)]), iscsiresult, startTime, endTime)
                            if tsmFlag:
                                endTime = ctime()
                                resultCollection("Result for snapshot \"%s\" creation on TSM %s is: " %(Name, config['tsmName%d' %(x)]), ['PASSED', ''], startTime, endTime)

                    ### delete TSM level snapshot
                    if deleteSnp:
                        querycommand = 'command=deleteSnapshot&id=%s&name=%s' %(tsm_dataset_id, Name)
                        resp_tsm_delete_snp = sendrequest(stdurl, querycommand)
                        filesave("logs/delete_tsm_snapshot.txt", "w",resp_tsm_delete_snp)
                        tsmdelete = json.loads(resp_tsm_delete_snp.text)
                        if 'errortext' in str(tsmdelete):
                            endTime = ctime()
                            errorstatus = str(tsmdelete['deleteSnapshotResponse']['errortext'])
                            #testout = string.find(errorstatus, sub[, 'has a'[,'clone']])
                            #print testout
                            resultCollection("Result for snapshot \"%s\" deletion on TSM %s is: " %(Name, config['tsmName%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                        else:
                            getControllerInfo(IP, passwd, 'zfs list -t snapshot | grep %s' %(Name), "tsm_snapshot_result.txt")

                            ## Verifying for cifs snapshot deletion
                            for p in range(1, int(config['Number_of_CIFSVolumes'])+1):
                                cifsresult = executeCmdNegative('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['volCifsDatasetname%d' %(p)], Name))
                                if cifsresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volCifsDatasetname%d' %(p)]), cifsresult, startTime, endTime)

                            ## Verifying for nfs snapshot deletion
                            for q in range(1, int(config['Number_of_NFSVolumes'])+1):
                                nfsresult = executeCmdNegative('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['volDatasetname%d' %(q)], Name))
                                if nfsresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volDatasetname%d' %(q)]), nfsresult, startTime, endTime)

                            ## Verifying for iscsi snapshot deletion
                            for r in range(1, int(config['Number_of_ISCSIVolumes'])+1):
                                iscsiresult = executeCmdNegative('cat tsm_snapshot_result.txt | grep %s@%s > tsm_snapshot_result2.txt' %(config['voliSCSIDatasetname%d' %(r)], Name))
                                if iscsiresult[0] == 'FAILED':
                                    tsmFlag = 0
                                    endTime = ctime()
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(r)]), iscsiresult, startTime, endTime)
                            if tsmFlag:
                                endTime = ctime()
                                resultCollection("Result for snapshot \"%s\" deletion on TSM %s is: " %(Name, config['tsmName%d' %(x)]), ['PASSED', ''], startTime, endTime)
                        
                else:
                    endTime = ctime()
                    resultCollection("Not able to get tsm dataset_id of TSM %s is: " %(config['tsmName%d' %(x)]), ['FAILED', ''], startTime, endTime)
    
else:
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
                        
                        ## Create snapshot
                        if createSnp:
                            querycommand = 'command=createStorageSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_create_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_create_snapshot)
                            createSnpResp = json.loads(resp_create_snapshot.text)
                            if 'errortext' in str(createSnpResp):
                                endTime = ctime()
                                errorstatus = str(createSnpResp['createStorageSnapshotResponse']['errortext'])
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volCifsDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                            else:
                                endTime = ctime()
                                getControllerInfo(IP, passwd, 'zfs list -t snapshot | grep %s' %(Name), "snapshot_result.txt")
                                out = executeCmd('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['volCifsDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volCifsDatasetname%d' %(x)]), out, startTime, endTime)
                        
                        ## Delete Snapshot
                        if deleteSnp:
                            querycommand = 'command=deleteSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_delete_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_delete_snapshot)
                            data3 = json.loads(resp_delete_snapshot.text)
                            if 'errortext' in str(data3):
                                endTime = ctime()
                                errorstatus = str(data3['deleteSnapshotResponse']['errortext'])
                                hasClone = string.find(errorstatus, 'has a clone')
                                if hasClone == -1:
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volCifsDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                                else:
                                    resultCollection("Snapshot \"%s\" on volume %s has a clone : " %(Name, config['volCifsDatasetname%d' %(x)]), ['PASSED', 'Not able to delete because it has a clone'], startTime, endTime)
                            else:
                                endTime = ctime()
                                cmd = 'zfs list -t snapshot | grep %s' %(Name)
                                getControllerInfo(IP, passwd, cmd, "snapshot_result.txt")
                                out = executeCmdNegative('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['volCifsDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volCifsDatasetname%d' %(x)]), out, startTime, endTime)
                    else:
                        endTime = ctime()
                        resultCollection("Not able to get filesystem_id of volume %s is: " %(config['volCifsIDatasetname%d' %(x)]), ['FAILED', ''], startTime, endTime)


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

                        ## Create snapshot on NFS volumes
                        if createSnp:
                            querycommand = 'command=createStorageSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_create_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_create_snapshot)
                            createSnpResp = json.loads(resp_create_snapshot.text)
                            if 'errortext' in str(createSnpResp):
                                endTime = ctime()
                                errorstatus = str(createSnpResp['createStorageSnapshotResponse']['errortext'])
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                            else:
                                endTime = ctime()
                                getControllerInfo(IP, passwd, 'zfs list -t snapshot | grep %s' %(Name), "snapshot_result.txt")
                                out = executeCmd('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['volDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['volDatasetname%d' %(x)]), out, startTime, endTime)

                        ## Delete snapshot on NFS volumes
                        if deleteSnp:
                            querycommand = 'command=deleteSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_delete_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_delete_snapshot)
                            data3 = json.loads(resp_delete_snapshot.text)
                            if 'errortext' in str(data3):
                                endTime = ctime()
                                errorstatus = str(data3['deleteSnapshotResponse']['errortext'])
                                hasClone = string.find(errorstatus, 'has a clone')
                                #print hasClone
                                if hasClone == -1:
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                                else:
                                    resultCollection("Snapshot \"%s\" on volume %s has a clone : " %(Name, config['volDatasetname%d' %(x)]), ['PASSED', 'Not able to delete because it has a clone'], startTime, endTime)
                            else:
                                endTime = ctime()
                                cmd = 'zfs list -t snapshot | grep %s' %(Name)
                                getControllerInfo(IP, passwd, cmd, "snapshot_result.txt")
                                out = executeCmdNegative('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['volDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['volDatasetname%d' %(x)]), out, startTime, endTime)
                    else:
                        endTime = ctime()
                        resultCollection("Not able to get filesystem_id of volume %s is: " %(config['volDatasetname%d' %(x)]), ['FAILED', ''], startTime, endTime)


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

                        ## Create Snapshot on ISCSI volumes
                        if createSnp:
                            querycommand = 'command=createStorageSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_create_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_create_snapshot)
                            createSnpResp = json.loads(resp_create_snapshot.text)
                            if 'errortext' in str(createSnpResp):
                                endTime = ctime()
                                errorstatus = str(createSnpResp['createStorageSnapshotResponse']['errortext'])
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                            else:
                                endTime = ctime()
                                getControllerInfo(IP, passwd, 'zfs list -t snapshot | grep %s' %(Name), "snapshot_result.txt")
                                out = executeCmd('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['voliSCSIDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" creation on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(x)]), out, startTime, endTime)
                        
                        ## Delete Snapshot on ISCSI volumes
                        if deleteSnp:
                            querycommand = 'command=deleteSnapshot&id=%s&name=%s' %(filesystem_id, Name)
                            resp_delete_snapshot = sendrequest(stdurl, querycommand)
                            filesave("logs/create_snapshot.txt", "w",resp_delete_snapshot)
                            data3 = json.loads(resp_delete_snapshot.text)
                            if 'errortext' in str(data3):
                                endTime = ctime()
                                errorstatus = str(data3['deleteSnapshotResponse']['errortext'])
                                hasClone = string.find(errorstatus, 'has a clone')
                                if hasClone == -1:
                                    resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(x)]), ['FAILED', errorstatus], startTime, endTime)
                                else:
                                    resultCollection("Snapshot \"%s\" on volume %s has a clone : " %(Name, config['voliSCSIDatasetname%d' %(x)]), ['PASSED', 'Not able to delete because it has a clone'], startTime, endTime)
                            else:
                                endTime = ctime()
                                cmd = 'zfs list -t snapshot | grep %s' %(Name)
                                getControllerInfo(IP, passwd, cmd, "snapshot_result.txt")
                                out = executeCmdNegative('cat snapshot_result.txt | grep %s@%s > snapshot_result2.txt' %(config['voliSCSIDatasetname%d' %(x)], Name))
                                resultCollection("Result for snapshot \"%s\" deletion on volume %s is: " %(Name, config['voliSCSIDatasetname%d' %(x)]), out, startTime, endTime)
                    else:
                        endTime = ctime()
                        resultCollection("Not able to get filesystem_id of volume %s is: " %(config['voliSCSIDatasetname%d' %(x)]), ['FAILED', ''], startTime, endTime)

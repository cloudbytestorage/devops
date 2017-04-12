import sys
import os
from time import ctime
import json
from cbrequest import sendrequest, getURL, configFile, listVolume, resultCollection, filesave, queryAsyncJobResult, mountCIFS, umountVolume, enabledDisableCIFS, listVolumeWithTSMId

### CIFS volume using snapshot.txt should be created before running this test case

if len(sys.argv) < 2:
    print 'Please provide correct arguments, as follows...'
    print 'python verifyAuthOnSubFilesystem.py configurationfole.txt'
    exit()

startTime = ctime()
config = configFile(sys.argv)
stdurl = getURL(config)
volumes = listVolume(config)
subVolName = None
tsm_id = None

if volumes[0] == 'BLOCKED':
    endTime = ctime()
    resultCollection('There is no CIFS filesystem to run \"Verify authentication on sub filesystem\" test case: ', ['BLOCKED', ''], startTime, endTime)
elif volumes[0] == 'FAILED':
    endTime = ctime()
    resultCollection('Failed to list filesystem, \"Verify authentication on sub filesystem\" test case:', ['BLOCKED', volumes[1]])
else:
    volumes = volumes[1]
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        for volume in volumes:
            if volume['name'] == "%s" %(config['volCifsDatasetname%d' %(x)]):
                try:
                    vol_id = volume['id']
                    tsm_id = volume['Tsmid']
                except: 
                    endTime = ctime()
                    print 'Not able to get tsm id or volume id'
                    resultCollection('Not able to get tsm id or volume id, So skipping \"Verify authentication on sub filesystem\" test case: ', ['BLOCKED', ''], startTime, endTime)
                    exit()
                startTime = ctime()
                ### creating sub filesystem
                subVolName = 'sub' + "%s" %(config['volCifsDatasetname%d' %(x)])
                iops = 0
                print subVolName
                ### Adding Qosgroup
                querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s' %(tsm_id, subVolName, config['volCifsLatency%d' %(x)], config['volCifsBlocksize%d' %(x)], config['volCifsTpcontrol%d' %(x)], config['volCifsThroughput%d' %(x)], config['volCifsIopscontrol%d' %(x)], iops, config['volCifsGraceallowed%d' %(x)], config['volCifsMemlimit%d' %(x)], config['volCifsNetworkspeed%d' %(x)])
                resp_addQosGroup = sendrequest(stdurl, querycommand)
                filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
                addQoSResp = json.loads(resp_addQosGroup.text)
                if 'errorcode' in str(addQoSResp):
                    endTime = ctime()
                    errormsg = str(addQoSResp['addqosgroupresponse']['errortext'])
                    resultCollection('Failed to addQoSGroup due to \"%s\"' %(errormsg), ['FAILED', ''], startTime, endTime)
                    exit()
                qosGroupId = addQoSResp['addqosgroupresponse']['qosgroup']['id']
                # calling ceateVolume command
                querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s&' %(qosGroupId, tsm_id, subVolName, config['volCifsQuotasize%d' %(x)], vol_id, config['volCifsDeduplication%d' %(x)], config['volCifsCompression%d' %(x)],config['volCifsSync%d' %(x)],config['volCifsRecordSize%d' %(x)],config['volCifsBlocklength%d' %(x)], subVolName, config['volCifsProtocoltype%d' %(x)])
                respCreateVolume = sendrequest(stdurl, querycommand)
                filesave("logs/createVolume.txt", "w", respCreateVolume)
                resultCreateVolume = json.loads(respCreateVolume.text)
                if 'errortext' in str(resultCreateVolume):
                    endTime = ctime()
                    errormsg = resultCreateVolume['createvolumeresponse']['errortext']
                    resultCollection('Not able to createVolume', ['FAILED', errormsg], startTime, endTime)
                    exit()
                job_id = resultCreateVolume["createvolumeresponse"]["jobid"]
                rstatus = queryAsyncJobResult(stdurl, job_id);
                endTime = ctime()
                if rstatus[0] == 'FAILED':
                    resultCollection('Creation of CIFS sub filesystem %s is failed:' %(subVolName), ['FAILED', rstatus[1]], startTime, endTime)
                    exit()
                elif rstatus[0] == 'NotSure':
                    resultCollection('Creation of CIFS sub filesystem %s is failed:' %(subVolName), ['FAILED', rstatus[1]], startTime, endTime)
                    exit()
                else:
                    resultCollection('Creation of CIFS sub filesystem %s is passed' %(subVolName), ['PASSED', ''], startTime, endTime)
                subVol = {'name': subVolName, 'mountPoint': subVolName, 'TSMIPAddress': "%s" %(config['volCifsIPAddress%d' %(x)]), 'AccountName': "%s" %(config['volCifsAccountName%d' %(x)])}
                
                # mounting of CIFS sub filesystem
                startTime = ctime()
                mountResult = mountCIFS(subVol)
                endTime = ctime()
                if mountResult == 'FAILED':
                    resultCollection('Mount of CIFS sub filesystem %s is failed' %(subVolName), ['FAILED', ''], startTime, endTime)
                else:
                    resultCollection('Mount of CIFS sub filesystem %s is passed' %(subVolName), ['PASSED', ''], startTime, endTime)
                
                # umounting CIFS sub filesystem
                startTime = ctime()
                umountResult = umountVolume(subVol)
                endTime = ctime()
                if umountResult == 'FAILED':
                    resultCollection('Umount of CIFS sub filesystem %s is failed' %(subVolName), ['FAILED', ''], startTime, endTime)
                else:
                    resultCollection('Umount of CIFS sub filesystem %s is passed' %(subVolName), ['PASSED', ''], startTime, endTime)

                # getting id of newly created sub filesystem
                startTime = ctime()
                subVolumes = listVolume(config)
                endTime = ctime()
                if subVolumes[0] == 'FAILED':
                    resultCollection('Not getting volume list', ['FAILED', subVolumes[1]], startTime, endTime)
                    exit()
                else:
                    subVolumes = subVolumes[1]
                    for volume in subVolumes:
                        if volume['name'] == "%s" %(subVolName):
                            try:
                                subVolId = volume['id']
                            except:
                                print 'Not able to get tsm id or volume id'
                                resultCollection('Not able to get tsm id or volume id, So skipping \"disable CIFS on sub filesystem\" test case: ', ['FAILED', ''], startTime, endTime)
                                exit()

                print subVolId
                # Disabling CIFS on sub filesystem
                startTime = ctime()
                disableCIFS = enabledDisableCIFS(config, subVolId, 'false')
                endTime = ctime()
                if disableCIFS[0] == 'FAILED':
                    resultCollection('Disable cifs protocol on CIFS sub filesystem %s is failed' %(subVolName), ['FAILED', disableCIFS[1]], startTime, endTime)
                    exit()
                else:
                    resultCollection('Disable cifs protocol on CIFS sub filesystem %s is passed' %(subVolName), ['PASSED', ''], startTime, endTime)

                # Enable NFS on CIFS sub filesystem(that is disable right now)
                startTime = ctime()
                querycommand = 'command=updateFileSystem&id=%s&nfsenabled=%s' %(subVolId, 'true')
                respUpdateFileSystem = sendrequest(stdurl, querycommand)
                filesave("logs/UpdateFileSystem.txt", "w", respUpdateFileSystem)
                respUpdateFileSystem = json.loads(respUpdateFileSystem.text)
                endTime = ctime()
                if "errorcode" in str(respUpdateFileSystem['updatefilesystemresponse']):
                    errormsg = str(respUpdateFileSystem['updatefilesystemresponse']['errortext'])
                    resultCollection('Enable NFS on CIFS sub filesystem %s' %(subVolName), ['FAILED', errormsg], startTime, endTime)
                else:
                    resultCollection('Enable NFS on CIFS sub filesystem %s' %(subVolName), ['PASSED', ''], startTime, endTime)

                # try to mount CIFS sub filesystem(right now cifs is disabled and nfs is enabled)
                startTime = ctime()
                mountResult = mountCIFS(subVol)
                endTime = ctime()
                print mountResult
                if mountResult == 'FAILED':
                    resultCollection('Not able to mount \"CIFS sub filesystem %s\" as cifs share when cifs protocol is disablle' %(subVolName), ['PASSED', ''], startTime, endTime)
                else:
                    resultCollection('Able to mount \"CIFS sub filesystem %s\" as cifs share even when cifs protocol is disablle' %(subVolName), ['FAILED', ''], startTime, endTime)
        if subVolName:
            startTime = ctime()
            subVol_id = None
            ### getting id of newly created sub filesystem
            volumes = listVolumeWithTSMId(config, tsm_id)
            if volumes[0] == 'PASSED':
                volumes = volumes[1]
                for  volume in volumes:
                    if volume['name'] == subVolName:
                        subVol_id = volume.get('id')
            else:
                endTime = ctime()
                resultCollection('Delete sub filesystem is', ['BLOCKED', volume[1]], startTime, endTime)
            if subVol_id is not None:
                querycommand = 'command=deleteFileSystem&id=%s' %(subVol_id)
                respDeleteSubFilesystem = sendrequest(stdurl, querycommand)
                filesave("logs/deleteSubFilesystem.txt", "w", respDeleteSubFilesystem)
                respDeleteSubFilesystem = json.loads(respDeleteSubFilesystem.text)
                endTime = ctime()
                if 'jobid' in str(respDeleteSubFilesystem['deleteFileSystemResponse']):
                    jobid = respDeleteSubFilesystem['deleteFileSystemResponse']['jobid']
                    rstatus = queryAsyncJobResult(stdurl, jobid)
                    resultCollection('Deletion of sub filesystem is', rstatus, startTime, endTime)
                else:
                    resultCollection('Not able to delete sub filesystem', ['FAILED', str(respDeleteSubFilesystem['deleteFileSystemResponse'])], startTime, endTime)

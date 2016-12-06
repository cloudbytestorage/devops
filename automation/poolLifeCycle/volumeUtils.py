import subprocess
from time import ctime
import time
import subprocess
import sys
import os
import json
import logging
from cbrequest import configFile, sendrequest, getControllerInfo , getoutput, \
        executeCmd, getControllerInfo, queryAsyncJobResult
logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

def get_qos_default_params():
    qos_def_params = {'name': '', 'tsmid': '', 'iops': 2, 'throughput': 0, \
            'blocksize': '4k', 'graceallowed': 'false', 'latency':15, \
            'iopscontrol': 'true', 'tpcontrol': 'false', 'memlimit': 0, \
            'networkspeed': 0}
    return qos_def_params

def get_iscsi_fc_default_params():
    vol_def_params = {'quotasize': '10G', 'compression': 'off', 'name': '', \
            'sync': 'always', 'recordsize': '32k', 'blocklength': '512B', \
            'datasetid': '', 'tsmid': '', 'accesstime': 'on', \
            'protocoltype': ''}
    return vol_def_params

def get_nfs_cifs_default_params():
    vol_def_params = {'quotasize': '10G', 'compression': 'off', 'name': '', \
            'sync': 'always', 'recordsize': '32k', 'blocklength': '512B', \
            'datasetid': '', 'tsmid': '', 'accesstime': 'on', \
            'protocoltype': '', 'mountpoint': ''}
    return vol_def_params

#Overwriting some default values by new values given by user in 'volume' 
#dictionary
def get_params(def_params, volume):
    for key in volume:
        if key in def_params:
            def_params[key] = volume[key]
    return def_params

def get_querycommand(command, QoSParams, type):
    querycommand = '%s' %(command)
    for key, value in QoSParams.iteritems():
        if key == 'name' and type == 'qosgroup':
            querycommand = querycommand + '&%s=QoS_%s' %(key, value)
        else:
            querycommand = querycommand + '&%s=%s' %(key, value)
    return querycommand

def listVolume_new(stdurl):
    querycommand = 'command=listFileSystem'
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing volume: %s', str(rest_api))
    resplistVolumes = sendrequest(stdurl, querycommand)
    data = json.loads(resplistVolumes.text)
    logging.debug('REST API for listing volume: %s', str(rest_api))
    if 'filesystem' in str(data['listFilesystemResponse']):
        volumes = data['listFilesystemResponse']['filesystem']
        result = ['PASSED', volumes]
        return result
    elif not 'errorcode' in str(data['listFilesystemResponse']):
        print 'There is no volume'
        result = ['BLOCKED', 'There is no volume to list']
        return result
    else:
        errormsg = str(data['listFilesystemResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result

def listVolumeWithTSMId_new(stdurl, tsm_id):
    querycommand = 'command=listFileSystem&tsmid=%s' %(tsm_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing volume with Tsm ID: %s', str(rest_api))
    resp_listVolumes = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listVolumes.text)
    logging.debug('REST API for listing volume with Tsm ID: %s', str(rest_api))
    if 'filesystem' in str(data['listFilesystemResponse']):
        volumes = data['listFilesystemResponse']['filesystem']
        result = ['PASSED', volumes]
        return result
    elif not 'errorcode' in str(data['listFilesystemResponse']):
        print 'There is no volume'
        result = ['BLOCKED', 'There is no volume to list']
        return result
    else:
        errormsg = str(data['listFilesystemResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result

###list_vol = listVolumeWithTSMId_new(stdurl, tsm_id)
def get_volume_info(list_vol, volume_name):
    for filesystem in list_vol:
        if volume_name == filesystem.get('name'):
            vol_name = filesystem.get('name')
            vol_id = filesystem.get('id')
            vol_mountPoint = filesystem.get('mountpoint')
            vol_iqnName = filesystem.get('iqnname')
            vol_grpID = filesystem.get('groupid')
            vol_quota = filesystem.get('quota')
            result = ['PASSED', vol_name, vol_id, vol_mountPoint, vol_iqnName,\
                    vol_grpID, vol_quota]
            return result
    else:
        return ['FAILED', 'Not able to get volume details']

def ToExecuteCmdOnShellAndReturnOutput(cmdToBeExecuted):
    output = subprocess.Popen(cmdToBeExecuted, shell=True, stdout=subprocess.PIPE)
    return output.stdout.readlines()

def getDiskAllocatedToISCSI(VSMIP,MountPoint):
    logging.info('Function execution starts')
    #config = configFileAccess()
    toGetIpList = 'iscsiadm -m session'
    toGetAttachedScsiDisk = "iscsiadm -m session -P3 | grep 'Attached scsi disk'"
    time.sleep(2)
    strlist = ToExecuteCmdOnShellAndReturnOutput(toGetIpList)
    scsiAssociatedDisk = ToExecuteCmdOnShellAndReturnOutput(toGetAttachedScsiDisk)
    ipList = [i.split(' ')[2].split(':')[0] for i in strlist]
    accountName = [i.split(' ')[3].split(':')[1].split('\n')[0] for i in strlist]
    diskAllocatedToScsi = [i.split(' ')[3].split('\t')[0] for i in scsiAssociatedDisk]
    indexDict = {}
    for x in range (0,1,1):
        for i in range(0,len(ipList),1):
            for j in range(0,len(accountName),1):
                logging.debug(ipList[i] + " and " + accountName[j])
                if ipList[i] == VSMIP and accountName[j] == MountPoint:
                    indexDict = {accountName[j]:accountName.index(accountName[j])}
    for k in indexDict:
        indexDict = {k:diskAllocatedToScsi[indexDict[k]]}
        result = ['PASSED', indexDict]
        return result

#fs_extension stands for filesystem e.g ext3/ext4
#volumeToBeFormated device name to be formated e.g. /dev/sdc
def toCreateExt4FileSystem(volumeToBeFormated, fs_extension):
    dict1 = getDiskAllocatedToISCSI('20.10.83.8','Account1iscsivol1')
    for i in dict1:
        if i == volumeToBeFormated:
            print dict1[i]
            executeCmd("fdisk /dev/%s < fdisk_response_file" %(dict1[i]))
            executeCmd("mkfs.%s /dev/%s1" %(fs_extension,dict[i]))
            #print "mkfs.%s /dev/%s1" %(fs_extension,dict[i])
            return "The extension is created successfully"

#dummy volume dictionary for example
#mendatory paramrs for user_params are as follows...
#name, tsmid, datasetid, protocoltype, mountpoint, stdurl
#for NFS and CIFS we need mountpoint, you can send any string
def create_volume(user_params, stdurl):
    logging.info('inside create_volume method...') 
    logging.debug('getting default parameters for creating QoS group')
    qos_def_params = get_qos_default_params()
    logging.debug('default parameters for creating QoS group: %s', str(qos_def_params))
    logging.debug('getting final parametrs for creating QoS group')
    qos_params = get_params(qos_def_params, user_params)
    #logging.debug('final parameters for creating QoS group: %s', str(qos_params))
    command = 'command=addQosGroup'
    logging.debug('getting REST API for creating QoS group...')
    querycommand = get_querycommand(command, qos_params, 'qosgroup')
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for creating QoS group: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    data = json.loads(resp_addQosGroup.text)
    logging.debug('response for add QoS group: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['addqosgroupresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('FAILED: %s', errormsg)
        return result
    logging.info('Getting qosgroupid...')
    qosgroup_id = data["addqosgroupresponse"]["qosgroup"]["id"]
    logging.debug('qosgroupid: %s', str(qosgroup_id))
    command = 'command=createVolume&qosgroupid=%s' %(qosgroup_id)
    logging.info('getting defaults parameters for create volume...')
    if user_params.get('protocoltype') is not None:
        if user_params['protocoltype'] == 'ISCSI' or user_params['protocoltype'] == 'FC':
            vol_def_params = get_iscsi_fc_default_params()
        elif user_params['protocoltype'] == 'NFS' or user_params['protocoltype'] == 'CIFS':
            vol_def_params = get_nfs_cifs_default_params()
        else:
            logging.error('protocol type is not correct, please specify correct...')
    else:
        vol_def_params = get_iscsi_fc_default_params()
    logging.debug('defaults parameters for create volume: %s', str(vol_def_params))
    logging.info('getting final parametrs for creating volume...')
    vol_params = get_params(vol_def_params, user_params)
    #logging.info('final parametrs for creating volume: %s', str(vol_params))
    querycommand = get_querycommand(command, vol_params, 'volume')
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for creating volume: %s', str(rest_api))
    resp_createVolume = sendrequest(stdurl, querycommand)
    data = json.loads(resp_createVolume.text)
    logging.debug('response for create volume: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['createvolumeresponse'].get('errortext'))
        logging.error('Not able to create volume due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result
    logging.info('getting create volume job id...')
    job_id = data['createvolumeresponse']['jobid']
    logging.debug('create volume job id: %s', job_id)
    logging.info('calling queryAsyncJobResult method...')
    create_volume_status = queryAsyncJobResult(stdurl, job_id)
    logging.debug('create_volume_status: %s', create_volume_status)
    if create_volume_status[0] == 'PASSED':
        result = ['PASSED', 'Volume created successfuly']
    else:
        result = ['FAILED', create_volume_status]
    logging.debug('result of create_volume: %s', str(result))
    return result

def delete_volume(id, stdurl):
    # id is volume id
    logging.info('Inside the delete_volume method...')
    querycommand = 'command=deleteFileSystem&id=%s' %(id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for deleting volume: %s', str(rest_api))
    resp_deleteFileSystem = sendrequest(stdurl, querycommand)
    data = json.loads(resp_deleteFileSystem.text)
    logging.debug('response for deleting volume: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['deleteFileSystemResponse'].get('errortext'))
        result = ['FAILED', 'Not able to delete volume due to: %s', errormsg]
        logging.error('Not able to delete volume due to: %s', errormsg)
        return result
    logging.info('getting job_id for deleting volume...')
    job_id = data['deleteFileSystemResponse']['jobid']
    logging.debug('job_id for delet volume: %s', job_id)
    logging.info('calling queryAsyncJobResult method...')
    delete_volume_status = queryAsyncJobResult(stdurl, job_id)
    logging.debug('delete_volume_status: %s', delete_volume_status)
    if delete_volume_status[0] == 'PASSED':
        result = ['PASSED', 'Volume deleted successfuly']
    else:
        result = ['FAILED', delete_volume_status]
    logging.debug('result of delete_volume: %s', str(result))
    return result

###To add NFS client..
##CLient can be 'ALL' or "IP"
def addNFSclient(stdurl, filesystemID, Client):
    logging.info('Adding NFS Client method...') 
    querycommand = 'command=nfsService&datasetid=%s&authnetwork=%s&'\
            'managedstate=true&alldirs=Yes&mapuserstoroot=No&readonly=No&'\
            'response=json' %(filesystemID, Client)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for adding NFS client: %s', str(rest_api))
    set_NFSService = sendrequest(stdurl, querycommand)
    data = json.loads(set_NFSService.text)
    logging.debug('response for add nfs client: %s', str(data))
    if "errorcode" in data["nfsserviceprotocolresponse"]:
        errormsg = str(data["nfsserviceprotocolresponse"].get("errortext"))
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result 
    else:
        logging.info('Getting nfs id')
        nfs_id = data["nfsserviceprotocolresponse"]["nfs"]["id"]
        logging.debug('nfs id : "%s"', nfs_id)
        logging.info('Getting controller id')
        ctrl_id = data["nfsserviceprotocolresponse"]["nfs"]["controllerid"]
        logging.debug('controller id : "%s"', ctrl_id)
        querycommand = 'command=updateController&nfsid=%s&type=configurenfs'\
                '&id=%s&response=json' %(nfs_id, ctrl_id)
        rest_api = str(stdurl) + str(querycommand)
        logging.debug('REST API for updating controller: %s', str(rest_api))
        UpadateNFSService = sendrequest(stdurl, querycommand)
        data = json.loads(UpadateNFSService.text)
        logging.debug('response for updating controller: %s', str(data))
        if "errorcode" in data["updateControllerResponse"]:
            errormsg = str(data["updateControllerResponse"].get("errortext"))
            logging.error('%s', errormsg)
            result1 = ['FAILED', errormsg]
            return result1
        result = ['PASSED', 'NFS client added successfully']
        return result

##To change the Throughput value
def edit_qos_tp(groupid, tpvalue, stdurl):
    logging.info('.....inside edit_qos_tp method....')
    logging.debug('getting REST API for editing QoS group THROUGHPUT  properties...')
    querycommand = 'command=updateQosGroup&id=%s&throughput=%s' %(groupid, tpvalue)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing QoS group THROUGHPUT  properties: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_updateQOS = sendrequest(stdurl, querycommand)
    upddata = json.loads(resp_updateQOS.text)
    logging.debug('Response for editing QoS group THROUGHPUT properties: %s', str(upddata))
    if 'errorcode' in str(upddata):
        errormsg = str(upddata['updateqosresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('FAILED: %s', errormsg)
        return result
    else:
        logging.info('Getting  new throuhput  value')
        tp = upddata['updateqosresponse']['qosgroup'][0]['throughput']
        logging.debug('new  throughput value is %s', (tp))
        vol_nametp = upddata['updateqosresponse']['qosgroup'][0]['name']
        if int(tpvalue) == int(tp):
            print "Throughput is  updated in "+vol_nametp+" is "+tp
            result = ['PASSED', upddata]
            logging.debug('PASSED: %s', upddata)
            return result
        else:
            errormsg =  "Throughput is not updated in "+vol_nametp
            result = ['FAILED', errormsg]
            logging.error('FAILED: %s', errormsg)
            return result

## To change the Iops value
def edit_qos_iops(group_id, iops_value, stdurl):
    logging.info('.....inside edit_qos_iops method....')
    logging.debug('getting REST API for editing QoS group IOPS properties...')
    querycommand = 'command=updateQosGroup&id=%s&iops=%s' %(group_id, iops_value)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing QoS group IOPS properties: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_updateQOS = sendrequest(stdurl, querycommand)
    upddata = json.loads(resp_updateQOS.text)
    logging.debug('Response for editing QoS group IOPS properties: %s', str(upddata))
    if 'errorcode' in str(upddata):
        errormsg = str(upddata['updateqosresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('FAILED: %s', errormsg)
        return result
    else:
        logging.info('Getting  new ipos value')
        iops = upddata['updateqosresponse']['qosgroup'][0]['iops']
        logging.debug('new  iops value is %s', (iops))
        vol_name = upddata['updateqosresponse']['qosgroup'][0]['name']
        if int(iops_value) == int(iops):
            msg =  "Updated Iops in "+vol_name+" is "+iops
            print msg
            result = ['PASSED', upddata]
            logging.debug('PASSED: %s', upddata)
            return result
        else:
            errormsg =  "IOPS not updated in "+vol_name
            result =['FAILED', errormsg]
            logging.error('FAILED: %s', errormsg)
            return result

def edit_qos_readonly(stdurl, volid, condition):
    ##condition refers to true or false
    #print "condition ="+condition
    logging.info('Inside edit_qos_readonly method....')
    logging.debug('getting REST API for editing QoS group readonly property...')
    querycommand = 'command=updateFileSystem&id=%s&readonly=%s' %(volid, condition)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing QoS group read only property: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_updateQOS = sendrequest(stdurl, querycommand)
    upddata = json.loads(resp_updateQOS.text)
    logging.debug('Response for editing QoS group readonly property: %s', str(upddata))
    if 'errorcode' in str(upddata):
        errormsg = str(upddata['updatefilesystemresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result
    logging.info('Getting  new read only condition...')
    value = upddata['updatefilesystemresponse']['filesystem'][0]['readonly']
    new_value = str(value).lower()
    logging.debug('new  read only condition  is %s', (new_value))
    if condition == new_value:
        result = ['PASSED', 'Read only condition is updated to %s ' %(new_value)]
        return result
    else:
        result = ['FAILED', 'New condition is not updated']
        return result

def edit_qos_compression(stdurl, volid, condition):
    ##condition here compression is on or off
    logging.info('Inside edit_qos_compressionmethod....')
    logging.debug('getting REST API for editing QoS group compression property...')
    querycommand = 'command=updateFileSystem&id=%s&compression=%s' %(volid, condition)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing QoS group compression property: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_updateQOS = sendrequest(stdurl, querycommand)
    upddata = json.loads(resp_updateQOS.text)
    logging.debug('Response for editing QoS group compression property: %s', str(upddata))
    if 'errorcode' in str(upddata):
        errormsg = str(upddata['updatefilesystemresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result
    logging.info('Getting  new compression condition...')
    value = upddata['updatefilesystemresponse']['filesystem'][0]['compression']
    new_value = str(value).lower()
    logging.debug('new  compression condition  is %s', (new_value))
    if condition == new_value:
        result = ['PASSED', 'compression condition is updated to %s ' %(new_value)]
        return result
    else:
        result = ['FAILED', 'compression condition is not updated']
        return result

def edit_qos_syncronization(stdurl, volid, condition):
    ## Here condition refers to always or standard
    logging.info('Inside edit_qos_syncronization method....')
    logging.debug('getting REST API for editing QoS group syncronization property...')
    querycommand = 'command=updateFileSystem&id=%s&sync=%s' %(volid, condition)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing QoS group syncronization property: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_updateQOS = sendrequest(stdurl, querycommand)
    upddata = json.loads(resp_updateQOS.text)
    logging.debug('Response for editing QoS group syncronization property: %s', str(upddata))
    if 'errorcode' in str(upddata):
        errormsg = str(upddata['updatefilesystemresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result
    logging.info('Getting  new syncronization condition...')
    value = upddata['updatefilesystemresponse']['filesystem'][0]['sync']
    new_value = str(value).lower()
    logging.debug('new  syncronization condition  is %s', (new_value))
    if condition == new_value:
        result = ['PASSED', 'syncronization condition is updated to %s ' %(new_value)]
        return result
    else:
        result = ['FAILED', 'syncronization condition is not updated']
        return result

def mount_iscsi(device, vol_name):
    #this method will work only when you create a partion to your iscsi LUN
    executeCmd('mkdir -p mount/%s' %(vol_name))
    mount_result = executeCmd('mount /dev/%s1 mount/%s' %(device, vol_name))
    if mount_result[0] == 'PASSED':
        logging.debug('mounted %s at mount/%s successfully', vol_name, vol_name)
        return ['PASSED', '']
    logging.error('Not able to mount iscsi LUN: %s', mount_result)
    return ['FAILED', mount_result]

def create_snapshot(stdurl, vol_id, vol_name, snp_name, node_ip, passwd):
    logging.debug('Inside create_snapshot method...')
    querycommand = 'command=createStorageSnapshot&id=%s&name=%s' \
            %(vol_id, snp_name)
    resp_create_snapshot = sendrequest(stdurl, querycommand)
    createSnpResp = json.loads(resp_create_snapshot.text)
    if 'errortext' in str(createSnpResp):
        errormsg = createSnpResp['createStorageSnapshotResponse'].get('errortext')
        logging.debug('Not able create snapshot %s, %s', snp_name, errormsg)
        return ['FAILED', '']
    logging.debug('createStorageSnapshot executed successfully')
    getControllerInfo(node_ip, passwd, 'zfs list -t snapshot | grep %s' \
            %(snp_name), 'snp_result.txt')
    out = executeCmd('cat snp_result.txt | grep %s@%s > snp_result2.txt' \
            %(vol_name, snp_name))
    if out[0] == 'FAILED':
        logging.debug('Snapshot %s is not created at Controller', snp_name)
        return ['FAILED', '']
    logging.debug('snapshot %s created successfully at Controller', snp_name)
    return ['PASSED', '']

def revert_snapshot(stdurl, volid, snp_name):
    logging.debug('Inside revert_snapshot...')
    querycommand = 'command=listStorageSnapshots&id=%s' %volid
    logging.debug('Executing listStorageSnapshots method...')
    resp_list_snapshot = sendrequest(stdurl, querycommand)
    data = json.loads(resp_list_snapshot.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listDatasetSnapshotsResponse']['errortext'])
        logging.error('Failed to list snapshot Error: %s', errormsg)
        return ['PASSED', '']
    if 'snapshot' not in str(data):
        logging.debug('There is no snapshot to revert')
        return ['FAILED', 'There is no snapshot to revert']
    snapshots = data['listDatasetSnapshotsResponse']['snapshot']
    path = None
    for snapshot in snapshots:
        path = None
        if snapshot['name'] == snp_name:
            path = snapshot.get('path')
            break
    if path is None:
        logging.error('Not able to get snapshot path for reverting it')
        return ['FAILED', 'Not able to get snapshot path']
    querycommand = 'command=rollbackToSnapshot&id=%s&path=%s' %(volid, path)
    logging.debug('Executing rollbackToSnapshot method...')
    resp_rollbackToSnapshot = sendrequest(stdurl, querycommand)
    data = json.loads(resp_rollbackToSnapshot.text)
    if 'errorcode' in str(data):
        errormsg = str(data['']['errortext'])
        logging.debug('Failed to revert snp %s Error: %s', snp_name, errormsg)
        return ['FAILED', '']
    logging.debug('snapshot %s reverted successfully', snp_name)
    return ['PASSED', '']

def edit_vol_quota(volid, quota, stdurl):
    logging.debug('Inside edit volume quota method...')
    querycommand='command=updateFileSystem&id=%s&quotasize=%s' %(volid, quota)
    rest_api = stdurl + querycommand
    logging.debug('REST API for editing quota: %s', (rest_api))
    edit_volQuota = sendrequest(stdurl, querycommand)
    data = json.loads(edit_volQuota.text)
    logging.debug('response for editing volume quota: %s', str(data))
    if 'errorcode' in str(data['updatefilesystemresponse']):
        errormsg = str(data['updatefilesystemresponse'].get('errortext'))
        print errormsg
        logging.error('%s', errormsg)
        return ['FAILED', errormsg]
    else:
        result = ['PASSED', 'Successfully updated volume quota size']
        return result

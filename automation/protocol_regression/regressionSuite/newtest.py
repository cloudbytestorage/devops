import sys
import os
import time
import json
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench
from haUtils import change_node_state, ping_machine
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_node_ip 
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        getControllerInfo, executeCmd, get_apikey, executeCmdNegative, \
        getoutput, mountNFS

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

##logging.info('------------------------------create, run iops delete tes case (NFS)'\
#        'started------------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python newtest.py conf.txt'
FOOTER_MSG = 'create, run iops delete tes case (NFS) completed'
BLOCKED_MSG = 'create run iops delete test case(NFS) is blocked'

#check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNTAX, FOOTER_MSG, \
#        BLOCKED_MSG, startTime)

conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
VSM_IP = conf['ipVSM1']
APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)
logging.debug('DEVMAN_IP: %s', DEVMAN_IP)
logging.debug('USER: %s', USER)
logging.debug('PASSWORD: %s', PASSWORD)
logging.debug('VSM_IP: %s', VSM_IP)
logging.debug('APIKEY: %s', APIKEY)
logging.debug('STDURL: %s', STDURL)

def getTsmInfo(tsms):
    if tsms[0] == 'PASSED':
        tsm = tsms[1]
        return tsm[0].get('name'), tsm[0].get('id'), tsm[0].get('datasetid'), \
                tsm[0].get('controllerid'), tsm[0].get('accountname'), \
                tsm[0].get('hapoolname')
    logging.error('create, run iops delete tes case (NFS) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('create, run iops delete tes case (NFS) is blocked Volume '\
            'creation failed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_list_volumes(volumes):
    if volumes[0] == 'PASSED':
        logging.debug('volumes listed successfullly')
        return volumes[1]
    logging.error('Not able to list volumes due to %s', volumes[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def get_vol_id(volumes, vol_name):
    volid = None
    voliqn = None
    accountid = None
    mntpoint = None
    for volume in volumes:
        if volume['name'] != vol_name:
            continue
        volid = volume.get('id')
        accountid = volume.get('accountid')
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or accountid is None or mntpoint is None:
        logging.error('create, run iops delete tes case (NFS) is blocked getting volid:'\
                '%s, accountid: %s, and mntpoint: %s', \
                volid, accountid, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, accountid, mntpoint

def verify_ddNFSclient(add_client_result, network, vol_name):
    if add_client_result[0] == 'PASSED':
        logging.debug('added clent <%s> to volume  %s successfully', \
                network, vol_name)
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_mountNFS(mount_result, volume_dir):
    if mount_result == 'PASSED':
        logging.debug('Volume %s mounted at mount/%s successfully', \
                volume_dir['name'], volume_dir['mountPoint'])
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_umount_result(umount_result, mount_dir):
    if umount_result[0] == 'PASSED':
        logging.debug('umounted %s successfully', mount_dir)
        return
    logging.error('Not able to umount %s Error:%s', mount_dir, umount_result)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def mountPointDetails(mount_dir):
    cmd = 'df -m | grep %s | awk {\'print $2\'}' %(mount_dir)
    used = str(getoutput(cmd))
    used = (used[2:-4])
    return used

logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
#logging.debug('tsms... %s', str(tsms))
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id, controllerid, accName, poolName = getTsmInfo(tsms)
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, controllerid:%s, '\
        'accName:%s, poolName:%s', tsm_name, tsm_id, dataset_id, \
        controllerid, accName, poolName)

volumeDict = {'name': 'createDelNFS1', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'NFS', 'iops': 100}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s, and mountpoint: %s', vol_id, \
        account_id, mnt_point)
volume_dir = {'mountPoint': mnt_point, 'TSMIPAddress': VSM_IP, 'name': \
        volumeDict['name']}
add_client_result = addNFSclient(STDURL, vol_id, 'ALL')
verify_ddNFSclient(add_client_result, 'ALL', volumeDict['name'])
mount_result = mountNFS(volume_dir)
verify_mountNFS(mount_result, volume_dir)

mount_dir = 'mount/%s' %(mnt_point)

mount_dir2 = {'name': volumeDict['name'], 'mountPoint': volumeDict['name']}
logging.info('...executing vdbench....')
executeVdbenchFile(mount_dir2, 'filesystem_nfs')

time.sleep(15)
pidCheck = is_vdbench_alive('filesystem_nfs')
print pidCheck
isIOAlive = True
while True:
    Used = mountPointDetails(mount_dir)
    if int(Used) >= 1000 :
        logging.debug('vdbench has successfully created 1 GB file of the')
        logging.debug('going to stop vdbench after 10 seconds...')
        time.sleep(10)
        break
    #else:
    #    pidCheck = is_vdbench_alive('filesystem_nfs')
    #    if pidCheck:
    #        continue
    #    else:
    #        logging.error('Vdbench has terminated unexpectedly without '\
    #                'creating initial file')
    #        logging.debug('The file written by vdbench is of %sM', Used)
    #        print 'Vdbench has terminated unexpectedly'
    #        isIOAlive = False
    #        break

#going to kill vdbench
kill_vdbench()
time.sleep(20)
#if not isIOAlive:
#    endTime = ctime()
#    print('create run io delete test case is blocked due to iops are not running')
#    logging.error('create run io delete test case is blocked due to iops are not running')
#    resultCollection('create run io delete test case is: ', ['BLOCKED', ''], startTime, endTime)

#exit()

umount_result = executeCmd('umount %s' %(mount_dir))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete '\
            'the NFS share', mount_dir)
else:
    logging.debug('NFS share %s umounted successfully', mount_dir)

logging.debug('removing configuration...')
logging.debug('Going to delete the volume')
delete_result = delete_volume(vol_id, STDURL)
endTime = ctime()
if 'FAILED' in str(delete_result):
    print 'Not able to delete NFS share %s' %(volumeDict['name'])
    resultCollection('create run io delete test case (NFS) is: ', ['FAILED', ''], startTime, endTime)
    logging.error('Not able to delete NFS share due to %s', delete_result[1])
else:
    print 'NFS share %s deleted successfully' %(volumeDict['name'])
    logging.debug('create run io delete test case is passed due to iops are not running')
    resultCollection('create run io delete test case (NFS) is: ', ['PASSED', ''], startTime, endTime)
    get_logger_footer('create, run iops delete tes case (NFS) completed')

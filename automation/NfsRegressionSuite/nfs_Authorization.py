import sys
import os
import time
import json
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_node_ip 
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        umountVolume_new, get_apikey, mountNFS_new, get_ntwInterfaceAndIP

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('---------------------NFS Authorization All/None/'\
        'Perticular Netwok started--------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python nfs_Authorization.py conf.txt'
FOOTER_MSG = 'NFS Authorization (ALL, None, Network) test case completed'
BLOCKED_MSG = 'NFS Authorization (All, None, Netwok) test case blocked'

check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
VSM_IP = conf['ipVSM1']
APIKEY = get_apikey(conf)
NODE1_IP = None
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

logging.debug('DEVMAN_IP: %s', DEVMAN_IP)
logging.debug('VSM_IP: %s', VSM_IP)
logging.debug('APIKEY: %s', APIKEY)
logging.debug('STDURL: %s', STDURL)

def getTsmInfo(tsms):
    if tsms[0] == 'PASSED':
        tsm = tsms[1]
        return tsm[0].get('name'), tsm[0].get('id'), tsm[0].get('datasetid')
    logging.error('NFS Authorization (All, None, Netwok) test case blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('NFS Authorization (All, None, Netwok) test case is '\
            'blocked Volume creation failed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_list_volumes(volumes):
    if volumes[0] == 'PASSED':
        logging.debug('volumes listed successfullly')
        return volumes[1]
    logging.error('Not able to list volumes due to %s', volumes[1])
    logging.error('NFS Authorization (All, None, Netwok) test case is blocked')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def get_vol_id(volumes, vol_name):
    volid = None
    mntpoint = None
    for volume in volumes:
        if volume['name'] != vol_name:
            continue
        volid = volume.get('id')
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or mntpoint is None:
        logging.error('NFS Authorization (All, None, Netwok) test case is blocked getting volid:'\
                '%s and mntpoint: %s', volid, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, mntpoint

def verify_ddNFSclient(add_client_result, network, vol_name):
    if add_client_result[0] == 'PASSED':
        logging.debug('added clent <%s> to volume  %s successfully', \
                network, vol_name)
        return
    logging.error('NFS Authorization (All, None, Netwok) test case is blocked')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id  = getTsmInfo(tsms)
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s', tsm_name, tsm_id, \
        dataset_id)

volumeDict = {'name': 'nfs_auth_one', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'NFS', 'iops': 100}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s and mountpoint: %s', vol_id, mnt_point)
volume_dir = {'mountPoint': mnt_point, 'TSMIPAddress': VSM_IP, 'name': \
        volumeDict['name']}

#setp 1: set Network to None---------------------------------------------------
mount_result = mountNFS_new(volume_dir)
endTime = ctime()
if mount_result[0] == 'FAILED' and 'access denied' in str(mount_result[1]):
    print 'Mount NFS when Network set to None: Not able to mount, PASSED'
    logging.debug('Mount NFS when Network set to None: Not able to mount, '\
            'PASSED')
    resultCollection('Mount NFS when Network set to None test case:', \
            ['PASSED', ''], startTime, endTime)
elif mount_result[0] == 'FAILED' and 'access denied' not in str(mount_result[1]):
    print 'Mount NFS when Network set to None: Not able to mount, FAILED'
    logging.debug('Mount NFS when Network set to None: Not able to mount, '\
            'FAILED, Error: %s', mount_result[1])
    resultCollection('Mount NFS when Network set to None test case:', \
            ['FAILED',''], startTime, endTime)
else:
    print 'Mount NFS when Network set to None: Able to mount, FAILED'
    logging.debug('Mount NFS when Network set to None: Able to mount, FAILED')
    resultCollection('Mount NFS when Network set to None test case:', \
            ['FAILED', ''], startTime, endTime)
#------------------------------------------------------------------------------

#step 2: set perticular Network------------------------------------------------
STEP2 = True
get_ip = get_ntwInterfaceAndIP(VSM_IP)
if get_ip[0] == 'PASSED':
    LOCAL_MACHINE_IP = get_ip[1]
else:
    print 'Given VSM IP is not reachable from local client, please provide '\
            'reachable VSM IP address'
    logging.error('Given VSM IP is not reachable from local client, please '\
            'provide reachable VSM IP address')
    logging.debug('Mount NFS when Network set to perticular N/W is blocked')
    resultCollection('Mount NFS when Network set to perticular N/W test '\
            'case:', ['BLOCKED', ''], startTime, endTime)
    STEP2 = False

if STEP2:
    add_client_result = addNFSclient(STDURL, vol_id, LOCAL_MACHINE_IP)
    verify_ddNFSclient(add_client_result, LOCAL_MACHINE_IP, volumeDict['name'])
    mount_result = mountNFS_new(volume_dir)
    endTime = ctime()
    if mount_result[0] == 'PASSED':
        print 'Mount NFS when Network set to perticular N/W: Able to mount, '\
                'PASSED'
        logging.debug('Mount NFS when Network set to perticular N/W: Able to '\
                'mount, PASSED')
        resultCollection('Mount NFS when Network set to perticular N/W test '\
                'case:', ['PASSED', ''], startTime, endTime)
        time.sleep(5)
        logging.debug('Going to umount the NFS share...')
        result = umountVolume_new(volume_dir)
    else:
        print 'Mount NFS when Network set to perticular N/W: FAILED'
        logging.error('Mount NFS when Network set to perticular N/W: Not '\
                'Able to mount, FAILED')
        resultCollection('Mount NFS when Network set to perticular N/W test '\
                'case:', ['FAILED', ''], startTime, endTime)

print 'going to delete NFS share created for initial test for Authorization'
logging.debug('going to delete NFS share %s created for initial test for '\
        'Authorization', volumeDict['name'])
delete_volume(vol_id, STDURL)
#------------------------------------------------------------------------------

#step 3 set Network to ALL-----------------------------------------------------
volumeDict = {'name': 'nfs_auth_all', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'NFS', 'iops': 100}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s and mountpoint: %s', vol_id, mnt_point)
volume_dir = {'mountPoint': mnt_point, 'TSMIPAddress': VSM_IP, 'name': \
        volumeDict['name']}

add_client_result = addNFSclient(STDURL, vol_id, 'ALL')
verify_ddNFSclient(add_client_result, 'ALL', volumeDict['name'])
mount_result = mountNFS_new(volume_dir)
if mount_result[0] == 'PASSED':
    print 'Mount NFS when Network set to ALL: Able to mount, PASSED'
    logging.debug('Mount NFS when Network set ALL: Able to mount, PASSED')
    resultCollection('Mount NFS when Network set to ALL test case:', \
            ['PASSED', ''], startTime, endTime)
else:
    print 'Mount NFS when Network set to ALL: Not able to mount, FAILED'
    logging.error('Mount NFS when Network set to ALL: Not Able to mount, '\
            'FAILED')
    resultCollection('Mount NFS when Network set to ALL test case:', \
            ['FAILED', ''], startTime, endTime)

logging.debug('Going to umount the NFS share...%s', volumeDict['name'])
time.sleep(5)
result = umountVolume_new(volume_dir)
print 'going to delete NFS share created for final test for Authorization(ALL)'
logging.debug('going to delete NFS share %s created for final test for '
'Authorization (ALL)', volumeDict['name'])
delete_volume(vol_id, STDURL)
#------------------------------------------------------------------------------

get_logger_footer('NFS Authorization (ALL, None, Network) test case completed')

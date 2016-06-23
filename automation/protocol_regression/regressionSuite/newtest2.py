import sys
import os
import time
import json
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench
from haUtils import change_node_state, ping_machine
from volumeUtils import create_volume, delete_volume, getDiskAllocatedToISCSI, \
        mount_iscsi, listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        assign_iniator_gp_to_LUN, discover_iscsi_lun, iscsi_login_logout, \
        get_iscsi_device, execute_mkfs, get_node_ip 
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        getControllerInfo, executeCmd, get_apikey, executeCmdNegative, getoutput

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------------create run io delete test case(iSCSI)'\
        'started------------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python newtest2.py conf.txt'
FOOTER_MSG = 'create run io delete test case(iSCSI) completed'
BLOCKED_MSG = 'create run io delete test case(iSCSI) is blocked'

check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

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
    logging.error('create run io delete test case(iSCSI) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('create run io delete test case(iSCSI) is blocked Volume '\
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
        voliqn = volume.get('iqnname')
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or accountid is None or voliqn is None or mntpoint is None:
        logging.error('create run io delete test case(iSCSI) is blocked getting volid:'\
                '%s, accountid: %s, voliqn: %sand mntpoint: %s', \
                volid, accountid, voliqn, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, voliqn, accountid, mntpoint

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('create run io delete test case(iSCSI) is blocked '\
            'getting iqn is None')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_add_auth_gp(add_auth_group, auth_gp):
    if add_auth_group[0] == 'FAILED':
        logging.debug('create run io delete test case(iSCSI) is blocked Not able to '\
                'assign auth group %s to LUN', auth_gp)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return

def verify_iscsi_operation(result, vol_name, action):
    if result[0] == 'PASSED':
        logging.debug('%s successfully for iSCSI LUN %s', action, vol_name)
        return
    if 'already exists' in str(result[1]):
        logging.debug('iscsi LUN %s is already logged in, lets go ahead and' \
                'get the iscsi device name', vol_name)
        return
    logging.error('create run io delete test case(iSCSI) is blocked Not able to %s '\
            '%s, Error: %s', action, vol_name, str(result[1]))
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_iscsi_device(iscsi_device, iqn, VSM_IP):
    if iscsi_device[0] == 'PASSED':
        device = iscsi_device[1]
        return device
    logging.debug('executing iscsi logout, since not able to get iscsi device')
    result = iscsi_login_logout(iqn, VSM_IP, 'logout')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_node_ip(result):
    if result[0] == 'PASSED':
        return result[1]
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_getDiskAllocatedToISCSI(result, mountpoint):
    if result[0] == 'PASSED' and mountpoint in str(result[1]):
        logging.debug('iscsi logged device... %s', result[1][mountpoint])
        return result[1][mountpoint]
    logging.error('Not able to get iscsi legged device')
    exit()

def verify_execute_mkfs(result):
    if result[0] == 'PASSED':
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_mount(mount_result):
    if mount_result[0] == 'PASSED':
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def mountPointDetails(mount_dir):
    cmd = 'df -m | grep %s | awk {\'print $3\'}' %(mount_dir)
    used = str(getoutput(cmd))
    used = (used[2:-4])
    return used

logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id, controllerid, accName, poolName = getTsmInfo(tsms)
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, controllerid:%s, '\
        'accName:%s, poolName:%s', tsm_name, tsm_id, dataset_id, \
        controllerid, accName, poolName)

volumeDict = {'name': 'createDliSCSI1', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'ISCSI', 'iops': 500, 'size': '5G'}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, vol_iqn, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s, mountpoint: %s and vol_iqn: %s', \
        vol_id, account_id, mnt_point, vol_iqn)

add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'ALL')
verify_add_auth_gp(add_auth_group, 'ALL')

logging.debug('getting iqn for volume %s', volumeDict['name'])
iqn = discover_iscsi_lun(VSM_IP, vol_iqn)
iqn = verify_iqn(iqn)
logging.debug('iqn for discovered iSCSI LUN... %s', iqn)

login_result = iscsi_login_logout(iqn, VSM_IP, 'login')
verify_iscsi_operation(login_result, volumeDict['name'], 'login')
time.sleep(2)
result = getDiskAllocatedToISCSI(VSM_IP, mnt_point)
iscsi_device = verify_getDiskAllocatedToISCSI(result, mnt_point)
result = execute_mkfs(iscsi_device, 'ext3')
verify_execute_mkfs(result)
mount_result = mount_iscsi(iscsi_device, volumeDict['name'])
verify_mount(mount_result)
mount_dir = {'name': volumeDict['name'], 'mountPoint': volumeDict['name']}
logging.info('...executing vdbench....')

executeVdbenchFile(mount_dir, 'filesystem_iscsi')
time.sleep(15)
pidCheck = is_vdbench_alive('filesystem_iscsi')
print pidCheck
isIOAlive = True

while True:
    Used = mountPointDetails(mount_dir['mountPoint'])
    print 'Mount Dir %s' %(mount_dir['mountPoint'])
    time.sleep(1)
    print 'Used------- %s' %(Used)
    if int(Used) >= 1000 :
        logging.debug('vdbench has successfully created 1 GB file of the')
        logging.debug('going to stop vdbench after 10 seconds...')
        time.sleep(10)
        break

kill_vdbench()
time.sleep(20)

umount_result = executeCmd('umount /dev/%s1' %(iscsi_device))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount /dev/%s1, still go ahead and logout '\
            'the iSCSI LUN, since test case is complete', iscsi_device)
else:
    logging.debug('LUN /dev/%s1 umounted successfully', iscsi_device)
logout_result = iscsi_login_logout(iqn, VSM_IP, 'logout')
if logout_result[0] == 'FAILED':
    logging.error('Not able to logged out iSCSI LUN, still go ahead and '\
            'set auth group to None, since test case is complete')
else:
    logging.debug('iSCSI LUN logged out successfully')

logging.debug('create run io delete test case(iSCSI) completed, removing '\
        'configuration')
add_auth_grup = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')

endTime = ctime()
if add_auth_grup[0] == 'FAILED':
    logging.error('Not able to set auth group to None, do not delete volume')
    resultCollection('create run io delete test case (iSCSI) is: ', ['FAILED', ''], startTime, endTime)
    get_logger_footer('create run io delete test case(iSCSI) completed')
else:
    logging.debug('Go and delete the volume')
    delete_result = delete_volume(vol_id, STDURL)
    if 'FAILED' in str(delete_result):
        print 'Not able to delete iSCSI LUN %s' %(volumeDict['name'])
        resultCollection('create run io delete test case (iSCSI) is: ', ['FAILED', ''], startTime, endTime)
        logging.error('Not able to delete iSCSI LUN due to %s', delete_result[1])
    else:
        print 'iSCSI LUN %s deleted successfully' %(volumeDict['name'])
        logging.debug('create run io delete test case is passed due to iops are not running')
        resultCollection('create run io delete test case (iSCSI) is: ', ['PASSED', ''], startTime, endTime)
        get_logger_footer('create run io delete test case(iSCSI) completed')

import sys
import os
import json
import time
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from cbrequest import configFile, sendrequest, resultCollection, get_apikey, \
        get_url, getoutput, executeCmd, executeCmdNegative
from volumeUtils import create_volume, delete_volume, mount_iscsi, \
        create_snapshot, getDiskAllocatedToISCSI, revert_snapshot, \
        listVolumeWithTSMId_new
from utils import get_logger_footer, assign_iniator_gp_to_LUN, \
        discover_iscsi_lun, iscsi_login_logout, get_iscsi_device, execute_mkfs, \
        copy_file, get_node_ip

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------------snapshot on iSCSI LUN test started'\
        '------------------------------')
#please make sure you have a file name as 'textfile' for executing this test
if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows...'
    print 'python snpISCSIVol.py conf.txt'
    logging.error('Arguments are not correct...')
    get_logger_footer('snapshot on iSCSI LUN test completed')
    exit()

startTime = ctime()
#getting configuration file
conf = configFile(sys.argv)
#in future, if required will change it as given parameter
FILE_TO_COPY = 'textfile' 
#FILE_TO_COPY = 'copy1.txt'
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
VSM_IP = conf['ipVSM1']
APIKEY = get_apikey(conf)
NODE_IP = None
PASSWD = 'test' # node password

def is_blocked():
    endTime = ctime()
    get_logger_footer('snapshot on iSCSI test completed')
    resultCollection('Snapshot functionality on iSCSI LUN test case is',\
            ['BLOCKED', ''], startTime, endTime)
    exit()

if APIKEY[0] == 'FAILED':
    errormsg = str(APIKEY[1])
    logging.error('Snapshot functionality on iSCSI LUN test case blocked due '\
            'to: %s', errormsg)
    is_blocked()

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
        return tsm[0]['name'], tsm[0]['id'], tsm[0]['datasetid'], \
                tsm[0]['controllerid']
    logging.error('Snapshot functionality on iSCSI LUN test case blocked '\
            'due to %s', tsms[1])
    is_blocked()

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('Snapshot functionality on iSCSI LUN test case is blocked '\
            'Volume creation failed')
    is_blocked()

def verify_list_volumes(volumes):
    if volumes[0] == 'PASSED':
        logging.debug('volumes listed successfullly')
        return volumes[1]
    logging.error('Not able to list volumes due to %s', volumes[1])
    is_blocked()

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
        logging.error('Snapshot functionality on iSCSI LUN test case is '\
                'blocked getting volid: %s, accountid: %s, voliqn: %s' \
                'and mntpoint: %s', volid, accountid, voliqn, mntpoint)
        is_blocked()
    return volid, voliqn, accountid, mntpoint

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('Snapshot functionality on iSCSI LUN test case is blocked '\
            'getting iqn is None')
    is_blocked()

def verify_add_auth_gp(add_auth_group, auth_gp):
    if add_auth_group[0] == 'FAILED':
        logging.debug('Snapshot functionality on iSCSI LUN test case is '\
                'blocked Not able to assign auth group %s to LUN', auth_gp)
        is_blocked()
    return

def verify_iscsi_operation(result, vol_name, action):
    if result[0] == 'PASSED':
        logging.debug('%s successfully for iSCSI LUN %s', action, vol_name)
        return
    if 'already exists' in str(result[1]):
        logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
                'get the iscsi device name', vol_name)
        return
    logging.error('Snapshot functionality on iSCSI LUN test case is blocked '\
            'Not able to %s %s, Error: %s', action, vol_name, str(result[1]))
    is_blocked()

def verify_iscsi_device(iscsi_device, iqn, VSM_IP):
    if iscsi_device[0] == 'PASSED':
        device = iscsi_device[1]
        return device
    logging.debug('executing iscsi logout, since not able to get iscsi device')
    result = iscsi_login_logout(iqn, VSM_IP, 'logout')
    is_blocked()

def verify_execute_mkfs(result):
    if result[0] == 'PASSED':
        return
    is_blocked()

def verify_mount(mount_result):
    if mount_result[0] == 'PASSED':
        return
    is_blocked()

def verify_copy_file(copy_result):
    if copy_result[0] == 'PASSED':
        return str(copy_result[1])
    is_blocked()

def verify_get_node_ip(result):
    if result[0] == 'PASSED':
        return result[1]
    is_blocked()

def verify_create_snapshot(create_snp_result):
    if create_snp_result[0] == 'PASSED':
        endTime = ctime()
        resultCollection('Snapshot created successfully on iSCSI LUN', 
                ['PASSED', ''], startTime, endTime)
        return
    is_blocked()

def verify_getDiskAllocatedToISCSI(result, mountpoint):
    if result[0] == 'PASSED' and mountpoint in str(result[1]):
        logging.debug('iscsi logged device... %s', result[1][mountpoint])
        return result[1][mountpoint]
    logging.error('Not able to get iscsi legged device')
    exit()

def verify_mkdir_result(mkdir_result):
    if mkdir_result[0] == 'PASSED':
        logging.debug('New directory created successfully')
        return
    logging.error('Not able to create directory after creating snapshot')
    is_blocked()

def verify_rm_file_result(rm_file_result, mount_dir):
    if rm_file_result[0] == 'PASSED':
        logging.debug('%s file removed successfully from %s' \
                %(FILE_TO_COPY, mount_dir))
        return
    logging.debug('Not able to remove file %s from %s after snapshot creation'\
            %(FILE_TO_COPY, mount_dir))
    is_blocked()

def verify_umount_result(umount_result, iscsi_device):
    if umount_result[0] == 'PASSED':
        logging.debug('umounted %s successfully', iscsi_device)
        return
    logging.error('Not able to umount %s Error:%s', iscsi_device, umount_result)
    is_blocked()

def verify_revert_snapshot(result):
    if result[0] == 'PASSED':
        return
    is_blocked()

def snapshot_conclusion(condition, ls1, ls2, mkdir1, msg):
    endTime = ctime()
    logging.debug('files or directory created before taking snapshot should '\
            'be there: %s', ls1)
    logging.debug('files or directory created after taking snapshot should '\
            'not be be there: %s', ls2)
    logging.debug('files or directory create after revert snapshot should '\
            'create: %s', mkdir1)
    logging.debug('%s', msg)
    if condition == 'PASSED':
        resultCollection('snapshot functionality on iSCSI LUN is working '
        'fine...', ['PASSED', ''], startTime, endTime)
    else:
        resultCollection('Snapshot functionality is not working...', \
                ['FAILED', ''], startTime, endTime)

logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
#logging.debug('tsms... %s', str(tsms))
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id, controllerid = getTsmInfo(tsms)
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s', tsm_name, tsm_id, \
        dataset_id)

result = get_node_ip(STDURL, controllerid)
NODE_IP = verify_get_node_ip(result)

volumeDict = {'name': 'snpiSCSI9', 'tsmid': tsm_id, 'datasetid': dataset_id, \
        'protocoltype': 'ISCSI', 'iops': 500}
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
#iscsi_device = get_iscsi_device()
#iscsi_device = verify_iscsi_device(iscsi_device, iqn, VSM_IP)
result = getDiskAllocatedToISCSI(VSM_IP, mnt_point)
iscsi_device = verify_getDiskAllocatedToISCSI(result, mnt_point)
result = execute_mkfs(iscsi_device, 'ext3')
verify_execute_mkfs(result)
mount_result = mount_iscsi(iscsi_device, volumeDict['name'])
verify_mount(mount_result)
mount_dir = 'mount/%s' %(volumeDict['name'])
copy_result = copy_file(FILE_TO_COPY, mount_dir)
md5_of_src_file = verify_copy_file(copy_result)
snp_name = 'snp1_%s' %(volumeDict['name'])
logging.debug('sleeping for 20 seconds before taking snapshot...')
time.sleep(60)
create_snp_result = create_snapshot(STDURL, vol_id, volumeDict['name'], \
        snp_name, NODE_IP, PASSWD)
verify_create_snapshot(create_snp_result)
logging.debug('creating new directory at %s after snapshot creation', mount_dir)
mkdir_result = executeCmd('mkdir -p %s/after_create_snp_dir' %(mount_dir))
verify_mkdir_result(mkdir_result)
rm_file_result = executeCmd('rm -rf %s/%s' %(mount_dir, FILE_TO_COPY))
verify_rm_file_result(rm_file_result, mount_dir)
logging.debug('umount and iscsi logout commads before snapshot restore')
umount_result = executeCmd('umount /dev/%s1' %(iscsi_device))
verify_umount_result(umount_result, iscsi_device)
logout_result = iscsi_login_logout(iqn, VSM_IP, 'logout')
verify_iscsi_operation(logout_result, volumeDict['name'], 'logout')
logging.debug('sleeping for 1 second before setting initiator group to None...')
time.sleep(1)
logging.debug('setting iscsi initiator group to None before restoring snapshot')
add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')
verify_add_auth_gp(add_auth_group, 'None')
result = revert_snapshot(STDURL, vol_id, snp_name)
verify_revert_snapshot(result)
time.sleep(5)
logging.debug('setting iscsi initiator group to All...')
add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'ALL')
login_result = iscsi_login_logout(iqn, VSM_IP, 'login')
verify_iscsi_operation(login_result, volumeDict['name'], 'login')
time.sleep(3)
result = getDiskAllocatedToISCSI(VSM_IP, mnt_point)
iscsi_device = verify_getDiskAllocatedToISCSI(result, mnt_point)
mount_result = mount_iscsi(iscsi_device, volumeDict['name'])
verify_mount(mount_result)
ls1 = executeCmd('ls %s/%s' %(mount_dir, FILE_TO_COPY))
ls2 = executeCmdNegative('ls %s/%s' %(mount_dir, 'after_create_snp_dir'))
mkdir1 = executeCmd('mkdir -p %s/after_revert_snp_dir' %(mount_dir))
if ls1[0] == 'FAILED' or ls2[0] == 'FAILED' or mkdir1[0] == 'FAILED':
    msg = 'snapshot functionality is not working...'
    snapshot_conclusion('FAILED', ls1[0], ls2[0], mkdir1[0], msg)
else:
    msg = 'snapshot functionality on iSCSI LUN is working fine...' 
    snapshot_conclusion('PASSED', ls1[0], ls2[0], mkdir1[0], msg)
logging.debug('snapshot execution done: going to umount, logged out, set '\
        'initiator group to None and delete the iSCSI LUN')
umount_result = executeCmd('umount /dev/%s1' %(iscsi_device))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount /dev/%s1, still go ahead and logout '\
            'the iSCSI LUN, since test case is complete', iscsi_device)
else:
    logging.debug('LUN /dev/%s1 umounted successfully', iscsi_device)
logout_result = iscsi_login_logout(iqn, VSM_IP, 'logout')
if logout_result[0] == 'FAILED':
    logging.error('Not able to logged out iSCSI LUN, still go ahead and set '\
            'auth group to None, since test case is complete')
else:
    logging.debug('iSCSI LUN logged out successfully')
logging.debug('sleeping for 1 second before setting initiator group to None...')
time.sleep(1)
add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')
if add_auth_group[0] == 'FAILED':
    logging.error('Not able to set auth group to None, do not delete volume')
    get_logger_footer('snapshot on iSCSI test completed')
    exit()
else:
    logging.debug('Go and delete the volume')
delete_volume(vol_id, STDURL)
get_logger_footer('snapshot on iSCSI test completed')


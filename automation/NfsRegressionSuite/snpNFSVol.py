import sys
import os
import json
import time
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from cbrequest import configFile, sendrequest, resultCollection, get_apikey, \
        get_url, getoutput, executeCmd, executeCmdNegative, mountNFS
from volumeUtils import create_volume, delete_volume, create_snapshot, \
        revert_snapshot, addNFSclient, listVolumeWithTSMId_new
from utils import get_logger_footer, copy_file, get_node_ip

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------------snapshot on NFS share test started'\
        '------------------------------')
#please make sure you have a file name as 'textfile' for executing this test
if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows...'
    print 'python snpNFSVol.py conf.txt'
    logging.error('Arguments are not correct...')
    get_logger_footer('snapshot on NFS share test completed')
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
    get_logger_footer('snapshot on NFS share test completed')
    resultCollection('Snapshot functionality on NFS share test case is',\
            ['BLOCKED', ''], startTime, endTime)
    exit()

if APIKEY[0] == 'FAILED':
    errormsg = str(APIKEY[1])
    logging.error('Snapshot functionality on NFS share test case blocked due '\
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
    logging.error('Snapshot functionality on NFS share test case blocked '\
            'due to %s', tsms[1])
    is_blocked()

def verify_create_volume(result) :
    if result[0] == 'PASSED':
        return
    logging.error('Snapshot functionality on NFS share test case is blocked '\
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
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or accountid is None or mntpoint is None:
        logging.error('Snapshot functionality on NFS share test case is '\
                'blocked getting volid: %s and accountid: %s and mntpoint: %s',\
                volid, accountid, mntpoint)
        is_blocked()
    return volid, accountid, mntpoint

def verify_ddNFSclient(add_client_result, network, vol_name):
    if add_client_result[0] == 'PASSED':
        logging.debug('added clent <%s> to volume  %s successfully', \
                network, vol_name)
        return
    is_blocked()

def verify_mountNFS(mount_result, volume_dir):
    if mount_result == 'PASSED':
        logging.debug('Volume %s mounted at mount/%s successfully', \
                volume_dir['name'], volume_dir['mountPoint'])
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
        resultCollection('Snapshot created successfully on NFS share', 
                ['PASSED', ''], startTime, endTime)
        return
    is_blocked()

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

def verify_umount_result(umount_result, mount_dir):
    if umount_result[0] == 'PASSED':
        logging.debug('umounted %s successfully', mount_dir)
        return
    logging.error('Not able to umount %s Error:%s', mount_dir, umount_result)
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
        resultCollection('snapshot functionality on NFS share is working '
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

volumeDict = {'name': 'snpNFS1', 'tsmid': tsm_id, 'datasetid': dataset_id, \
        'protocoltype': 'NFS', 'iops': 500}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s, mountpoint: %s', \
        vol_id, account_id, mnt_point)
volume_dir = {'mountPoint': mnt_point, 'TSMIPAddress': VSM_IP, 'name': \
        volumeDict['name']}
add_client_result = addNFSclient(STDURL, vol_id, 'ALL')
verify_ddNFSclient(add_client_result, 'ALL', volumeDict['name'])
mount_result = mountNFS(volume_dir)
verify_mountNFS(mount_result, volume_dir)
mount_dir = 'mount/%s' %(mnt_point)
copy_result = copy_file(FILE_TO_COPY, mount_dir)
md5_of_src_file = verify_copy_file(copy_result)
snp_name = 'snp1_%s' %(volumeDict['name'])
logging.debug('sleeping for 60 seconds before taking snapshot...')
time.sleep(60)
create_snp_result = create_snapshot(STDURL, vol_id, volumeDict['name'], \
        snp_name, NODE_IP, PASSWD)
verify_create_snapshot(create_snp_result)
logging.debug('creating new directory at %s after snapshot creation', mount_dir)
mkdir_result = executeCmd('mkdir -p %s/after_create_snp_dir' %(mount_dir))
verify_mkdir_result(mkdir_result)
rm_file_result = executeCmd('rm -rf %s/%s' %(mount_dir, FILE_TO_COPY))
verify_rm_file_result(rm_file_result, mount_dir)
logging.debug('umount NFS share before snapshot restore')
umount_result = executeCmd('umount %s' %(mount_dir))
verify_umount_result(umount_result, mount_dir)
logging.debug('sleeping for 1 second before reverting snapshot...')
time.sleep(1)
result = revert_snapshot(STDURL, vol_id, snp_name)
verify_revert_snapshot(result)
time.sleep(3)
mount_result = mountNFS(volume_dir)
verify_mountNFS(mount_result, volume_dir)
logging.debug('After restoring the snapshot, volume mounted successfully')
ls1 = executeCmd('ls %s/%s' %(mount_dir, FILE_TO_COPY))
ls2 = executeCmdNegative('ls %s/%s' %(mount_dir, 'after_create_snp_dir'))
mkdir1 = executeCmd('mkdir -p %s/after_revert_snp_dir' %(mount_dir))
if ls1[0] == 'FAILED' or ls2[0] == 'FAILED' or mkdir1[0] == 'FAILED':
    msg = 'snapshot functionality is not working...'
    snapshot_conclusion('FAILED', ls1[0], ls2[0], mkdir1[0], msg)
else:
    msg = 'snapshot functionality on NFS share is working fine...' 
    snapshot_conclusion('PASSED', ls1[0], ls2[0], mkdir1[0], msg)

logging.debug('snapshot execution done: going to umount, delete the NFS share')
umount_result = executeCmd('umount %s' %(mount_dir))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete the NFS '\
            'share since test case is complete', mount_dir)
else:
    logging.debug('NFS share %s umounted successfully going to delete it', \
            mount_dir)

delete_volume(vol_id, STDURL)
get_logger_footer('snapshot on NFS share test completed')

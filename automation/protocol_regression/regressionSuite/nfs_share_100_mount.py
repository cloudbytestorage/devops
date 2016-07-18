import os
import sys
import time
import json
import logging
from time import ctime
from tsmUtils import create_tsm
from accountUtils import get_account_id
from tsmUtils import create_tsm, delete_tsm, listTSMWithIP_new
from poolUtils import get_pool_info, listPool, getFreeDisk, getDiskToAllocate, \
        create_pool, listDiskGroup
from volumeUtils import create_volume, addNFSclient, delete_volume, \
        listVolumeWithTSMId_new
from haUtils import get_controller_info, list_controller, get_value, \
        get_node_IP
from utils import check_mendatory_arguments, is_blocked, get_logger_footer
from cbrequest import configFile, sendrequest, mountNFS_new, umountVolume, \
        get_url, get_apikey, queryAsyncJobResult, resultCollection, \
        umount_with_dir

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------mount/umount 100 NFS volumes test case'\
        'started--------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python  nfs_share_100_mount.py conf.txt pool_name(optional) '\
        'account_name(optional)'
FOOTER_MSG = 'mount/umount 100 NFS volumes test case completed'
BLOCKED_MSG = 'mount/umount 100 NFS volumes test case is'

check_mendatory_arguments(sys.argv,2, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

conf = configFile(sys.argv)
if len(sys.argv) == 2:
    pool_name = None
    account_name = None
elif len(sys.argv) == 3:
    pool_name = sys.argv[2]
    account_name = None
else:
    pool_name = sys.argv[2]
    account_name = sys.argv[3]

try:
    DEVMAN_IP = conf['host']
    USER = conf['username']
    PASSWORD = conf['password']
except KeyError:
    print 'Please provide correct information in config file'

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

POOL_NAME = 'mountPL1'
POOL_IOPS = '100000'
POOL_DISK_TYPE = 'SAS'
NUM_POOL_DISKS = '3'
POOL_TYPE = 'raidz1'
account_name = None

TSM_IPs = ['None', 'None', 'None', 'None', 'None']
TSM_interface = ['None', 'None', 'None', 'None', 'None']
TSM_dnsserver = ['None', 'None', 'None', 'None', 'None']
TSM_IDs = ['None', 'None', 'None', 'None', 'None']
DATASET_IDs = ['None', 'None', 'None', 'None', 'None']
VOLUME_IDs = []
MNT_POINTS = []
MOUNT_SUCCESS = True
UMOUNT_SUCCESS = True
MOUNTED_SHARE = []
VOL_REMOVE = True
TSM_REMOVE = True

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('mount/umount 100 NFS volumes test case is blocked Volume '\
            'creation failed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_list_controller(list_cntrl, startTime):
    if list_cntrl[0] == 'PASSED':
        return list_cntrl[1]
    logging.error('mount/umount 100 NFS volumes test case is blocked due to: %s', list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    ogging.error('mount/umount 100 NFS volumes test case is blocked due to: %s', get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def update_volid_mntpoint(volumes):
    for volume in volumes:
        vol_id = volume.get('id')
        mntpoint = volume.get('mountpoint')
        if vol_id is not None and mntpoint is not None:
            VOLUME_IDs.append(vol_id)
            MNT_POINTS.append(mntpoint)
        else:
            print 'vol id or mountpoint is None...'
            logging.debug('vol id or mountpoint is None...')
            logging.debug('mount/umount 100 NFS volumes test case is blocked')
            is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

for x in range(0, 5):
        #try:
        TSM_IPs[x] = conf['ipVSM%s' %(x+1)]
        TSM_interface[x] = conf['interfaceVSM%s' %(x+1)]
        TSM_dnsserver[x] = conf['dnsVSM%s' %(x+1)]
        if TSM_IPs[x] == '' and TSM_interface[x] == '' and TSM_dnsserver[x] \
                == '':
                    print 'Value for ipVSM/interfaceVSM/dnsVSM getting None'
                    logging.debug('Value for key ipVSM/interfaceVSM/dnsVSM '\
                            'is None, specify correct values in config file')
                    logging.debug('mount/umount 100 NFS volumes test case '\
                            'is blocked')
                    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
        logging.debug('Value foe key \'ipVSM%s\' is: %s', (x+1), \
                conf['ipVSM%s' %(x+1)])
        logging.debug('Value foe key \'interfaceVSM%s\' is: %s', (x+1), \
                conf['interfaceVSM%s' %(x+1)])
        logging.debug('Value foe key \'dnsVSM%s\' is: %s', (x+1), \
                conf['dnsVSM%s' %(x+1)])
        #except KeyError:
        #print 'There is KeyError in config file, specify correct keys'
        #logging.debug('mount/umount 100 NFS volumes test case is blocked...')
        #logging.error('There is KeyError in configuration file, specify as '\
        #        'follows... interfaceVSM, ipVSM, dnsVSM etc.')
        #is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

###---getting pool id----------------------------------------------------------
startTime = ctime()
list_cntrl = list_controller(STDURL)
controllers = verify_list_controller(list_cntrl, startTime)
controllers_ip, num_of_Nodes = get_node_IP(controllers)

if num_of_Nodes == 1:
    NODE1_IP = controllers_ip[0]
elif num_of_Nodes == 2:
    NODE1_IP = controllers_ip[0]
    NODE2_IP = controllers_ip[1]
else:
    logging.debug('No support yet for clusters with greater than 2 nodes')
    exit()

get_info = get_controller_info(NODE1_IP, controllers)
verify_get_controller_info(get_info, startTime)
status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
        site_id = get_value(get_info)

if status.lower() == 'maintenance' and num_of_Nodes == 2:
    logging.debug('Node1 is in maintenance, checking status of Node2')
    get_info = get_controller_info(NODE2_IP, controllers)
    verify_get_controller_info(get_info, startTime)
    status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
            site_id = get_value(get_info)
    if status.lower() == 'maintenance':
        logging.error('Both nodes are in maintenance, testcase cannot proceed')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
elif status.lower() == 'maintenance' and num_of_Nodes == 1:
    logging.error('The single node in HAgroup is in maintenance, testcase '\
            'cannot proceed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Steps to get free disk list for pool creation
freedisk = getFreeDisk(ctrl_disks)
if freedisk[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, freedisk[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
freedisk = freedisk[1]

# Steps to get allocatable disks for pool (based on size, type etc..,)
allocatable_diskidlist = getDiskToAllocate(freedisk, NUM_POOL_DISKS, POOL_DISK_TYPE)
if allocatable_diskidlist[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, allocatable_diskidlist[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
allocatable_diskidlist = allocatable_diskidlist[1]
# Get params for pool creation (Needs controller, pool info etc..,)
pool_params = {'name': POOL_NAME, 'siteid': site_id, 'clusterid': \
        ctrl_cluster_id, 'controllerid': ctrl_id, 'iops': POOL_IOPS, \
        'diskslist': allocatable_diskidlist, 'grouptype': POOL_TYPE}
pool_creation = create_pool(pool_params, STDURL)
if pool_creation[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ' : %s', tcName, pool_creation[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

pool_result = listPool(STDURL)
if pool_result[0] == 'FAILED':
    print 'Not able to get Pools...'
    logging.error('mount/umount 100 NFS volumes test case is blocked...')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
elif pool_result[0] == 'BLOCKED':
    print 'There is no pool...'
    logging.debug('mount/umount 100 NFS volumes test case is')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
else:
    pools = pool_result[1]

pool_info = get_pool_info(pools, pool_name)
if pool_info[0] == 'FAILED':
    print 'Not able to get pool ID...'
    logging.error('Not able to get pool ID, Error: %s', pool_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
pool_id = pool_info[1]
print pool_id
#------------------------------------------------------------------------------

###---getiing account id-------------------------------------------------------
account_id = get_account_id(STDURL, account_name)
if account_id[0] == 'PASSED':
    account_id = account_id[1]
else:
    print 'Not able to get account id...'
    logging.error('mount/umount 100 NFS volumes test case is blocked, '\
            'Error: %s', account_id[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
print account_id
#------------------------------------------------------------------------------

###creating 5 TSM--------------------------------------------------------------
for x in range(1, 6):
    tsm_dict = {'name': 'T200%s' %(x), 'accountid': account_id, 'poolid': \
            pool_id, 'totaliops': '2000', 'quotasize': '1T', 'tntinterface': \
            str(TSM_interface[x-1]), 'dnsserver': str(TSM_dnsserver[x-1]), \
            'ipaddress': str(TSM_IPs[x-1]), 'totalthroughput': '8000'}
    #calling create TSM method...
    result = create_tsm(tsm_dict, STDURL)
    if result[0] == 'FAILED':
        print 'Not able to create VSM/TSM %s' %(tsm_dict.get('name'))
        logging.error('Not able to create VSM/TSM %s', result[1])
        logging.debug('mount/umount 100 NFS volumes test case is blocked...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
#------------------------------------------------------------------------------

###Getting TSMs ID and dasetids------------------------------------------------
for x in range(1, 6):
    tsm = listTSMWithIP_new(STDURL, str(TSM_IPs[x-1]))
    if tsm[0] == 'FAILED':
        print 'Not able to get TSM/VSM with IP: %s' %(TSM_IPs[x-1])
        logging.error('Not able to list TSM/VSM with IP: %s', TSM_IPs[x-1])
        logging.debug('mount/umount 100 NFS volumes test case is blocked...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    elif tsm[0] == 'BLOCKED':
        print 'There is no TSM/VSM with IP: %s' %(TSM_IPs[x-1])
        logging.error('There is no TSM/VSM with IP: %s', TSM_IPs[x-1])
        logging.debug('mount/umount 100 NFS volumes test case is blocked...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    else:
        tsm = tsm[1]
        tsm_id = tsm[0].get('id')
        datasetid = tsm[0].get('datasetid')
        if tsm_id is None or datasetid is None:
            print 'getting TSM/VSM id or datasetid as None'
            logging.error('Getting tsm id or datasetid as None...')
            logging.debug('tsm id: %s', tsm_id)
            logging.debug('datasetid: %s', datasetid)
            logging.debug('mount/umount 100 NFS volumes test case is blocked.')
            is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
        else:
            TSM_IDs[x-1] = tsm_id
            DATASET_IDs[x-1] = datasetid
#------------------------------------------------------------------------------

###volume creation-------------------------------------------------------------
for x in range(1, 6):
    for y in range(1, 21):
        volDict = {'name': 'T100%sv%s' %(x, y), 'tsmid': TSM_IDs[x-1], \
                'iops': 100, 'datasetid': DATASET_IDs[x-1], \
                'protocoltype': 'NFS'}
        result = create_volume(volDict, STDURL)
        verify_create_volume(result)
#------------------------------------------------------------------------------

###getting volumes id and mountpoint--------------------------------------------
for x in range(1, 6):
    volumes = listVolumeWithTSMId_new(STDURL, TSM_IDs[x-1])
    if volumes[0] == 'PASSED':
        volumes = volumes[1]
    else:
        print 'Not able to list the volumes...'
        logging.error('Not able to list volumes %s', volumes[1])
        logging.debug('mount/umount 100 NFS volumes test case is blocked...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    update_volid_mntpoint(volumes)
#------------------------------------------------------------------------------

###Updating network to access the share----------------------------------------
for x in range(1, 101):
    result = addNFSclient(STDURL, VOLUME_IDs[x-1], 'ALL')
    if result[0] == 'FAILED' and 'already exists' in str(result[1]):
        pass
    elif result[0] == 'FAILED':
        endTime = ctime()
        print 'Not able to update network ALL to access NFS share'
        logging.error('Not able to update network ALL, Error: %s', result[1])
        logging.debug('mount/umount 100 NFS volumes test case is failed...')
        resultCollection('mount/umount 100 NFS volumes test case', \
                ['FAILED', ''], startTime, endTime)
        exit()
#------------------------------------------------------------------------------

def umount_all():
    if len(MOUNTED_SHARE) == 0:
        print 'There is no volume mounted...'
        logging.debug('There is no volume mounted...')
        return
    for x in range(1, (len(MOUNTED_SHARE) + 1)):
        result = umount_with_dir(MOUNTED_SHARE[x-1])
        if result[0] == 'FAILED':
            print 'Not able to umount volume with mountpoint %s' \
                    %(MOUNTED_SHARE[x-1])
            logging.error('Not able to umount volume with mountpoint %s, '\
                    'Error: %s', MOUNTED_SHARE[x-1], result[1])
            UMOUNT_SUCCESS = False
        else:
            print 'volume with mountpoint %s umounted' %(MOUNTED_SHARE[x-1])
            logging.debug('volume with mountpoint %s umounted...', \
                    MOUNTED_SHARE[x-1])


###mounting all the volumes----------------------------------------------------
for x in range(1, 6):
    i = 20 * (x - 1)
    for y in range(1, 21):
        mnt_dir = {'TSMIPAddress': str(TSM_IPs[x-1]), 'mountPoint': \
                str(MNT_POINTS[i]), 'name': 'T100%sv%s' %((x), y)}
        mnt_result = mountNFS_new(mnt_dir)
        if 'already mounted' in str(mnt_result[1]):
            print 'Volume T100%sv%s already mounted' %(x, y)
            logging.debug('Volume T100%sv%s already mounted', x, y)
            print 'Mardan\n'
            print i
            MOUNTED_SHARE.append(str(MNT_POINTS[i]))
        elif mnt_result[0] == 'FAILED':
            endTime = ctime()
            print 'Not able to mout volume T100%sv%s' %((x), y)
            logging.error('Not able to mout volume T100%sv%s', x, y)
            MOUNT_SUCCESS = False
            break
        else:
            MOUNTED_SHARE.append(str(MNT_POINTS[i]))
            print 'Volume T100%sv%s mounted successfully' %(x, y)
            logging.debug('Volume T100%sv%s mounted successfully', x, y)
        i = i + 1
    if not MOUNT_SUCCESS:
        break
#------------------------------------------------------------------------------

###umount all NFS shares-------------------------------------------------------
logging.debug('Going to umount the mounted volumes...')
umount_all()
#------------------------------------------------------------------------------

###verifying mount/umount 100 NFS volumes test case----------------------------
endTime = ctime()
if MOUNT_SUCCESS and UMOUNT_SUCCESS:
    print 'All 100 volumes mounted snd umounted successfully...'
    logging.debug('All 100 volumes mounted and umounted successfully...')
    resultCollection('mount/umount 100 NFS volumes test case is', \
            ['PASSED', ''], startTime, endTime)
elif not MOUNT_SUCCESS and not UMOUNT_SUCCESS:
    print 'Got error during mounting and umounting the volumes...'
    logging.info('Got error during mounting and umount the volumes...')
    logging.debug('mount/umount 100 NFS volumes test case is failed...')
    resultCollection('mount/umount 100 NFS volumes test case is', \
            ['FAILED', ''], startTime, endTime)
elif not MOUNT_SUCCESS:
    print 'Having problem in mounting all the volumes...'
    logging.error('Having problem in mounting all the volumes...')
    logging.debug('mount/umount 100 NFS volumes test case is failed...')
    resultCollection('mount/umount 100 NFS volumes test case is', \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Having problem in umounting all the volumes...'
    logging.error('Having problem in umounting all the volumes...')
    logging.debug('mount/umount 100 NFS volumes test case is failed...')
    resultCollection('mount/umount 100 NFS volumes test case is', \
            ['FAILED', ''], startTime, endTime)
#------------------------------------------------------------------------------

###Deleting volumes------------------------------------------------------------
for x in range(1, 6):
    i = 20 * (x - 1)
    for y in range(1, 21):
        result = delete_volume(VOLUME_IDs[i], STDURL)
        if result[0] == 'FAILED':
            VOL_REMOVE = False
        i = i + 1
#------------------------------------------------------------------------------

###deleting TSM/VSM------------------------------------------------------------
if VOL_REMOVE:
    for x in range(0, 5):
        delete_tsm_resp = delete_tsm(TSM_IDs[x], STDURL)
        if delete_tsm_resp[0] == 'FAILED':
            TSM_REMOVE = False
#------------------------------------------------------------------------------

#verifying and logging remove_configuration details----------------------------
if VOL_REMOVE and TSM_REMOVE:
    print 'configuration removed successfully for mount/umount 100 NFS test'
    logging.debug('confguration removed successfully for mount/umount 100 '\
            'NFS test')
elif VOL_REMOVE:
    print 'Not able to remove VSM/TSM of mount/umount 100 NFS test'
    logging.error('Not able to remove VSM/TSM configuration of mount/umount '\
            '100 NFS test')
else:
    print 'Not able to remove volumes of mount/umount 100 NFS test'
    logging.error('Not able to remove volume configuration of mount/umount '\
            '100 NFS test')
#------------------------------------------------------------------------------

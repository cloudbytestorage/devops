import os
import sys
import time
import json
import logging
from time import ctime
from tsmUtils import create_tsm
from accountUtils import get_account_id
from poolUtils import get_pool_info, listPool, getFreeDisk, getDiskToAllocate, \
        create_pool, listDiskGroup
from haUtils import get_controller_info, list_controller, get_value, \
        get_node_IP
from volumeUtils import create_volume, addNFSclient, delete_volume, \
        listVolumeWithTSMId_new
from tsmUtils import create_tsm, delete_tsm, listTSMWithIP_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer
from cbrequest import configFile, sendrequest, mountNFS_new, umountVolume, \
        get_url, get_apikey, queryAsyncJobResult, resultCollection, \
        umount_with_dir

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------create pool, create vsms for regression test'\
        'started--------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python  create_pool_vsms.py conf.txt'
FOOTER_MSG = 'create pool, create vsms for regression test completed'
BLOCKED_MSG = 'create pool, create vsms for regression test is'

check_mendatory_arguments(sys.argv,2, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

conf = configFile(sys.argv)

POOL_NAME = 'regressionPL1'
POOL_IOPS = '5000'
POOL_DISK_TYPE = 'SAS'
NUM_POOL_DISKS = '3'
POOL_TYPE = 'raidz1'
account_name = None

try:
    DEVMAN_IP = conf['host']
    USER = conf['username']
    PASSWORD = conf['password']
except KeyError:
    print 'Please provide correct information in config file'

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

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

tcName = 'protocol_regression_suite'

def verify_list_controller(list_cntrl, startTime):
    if list_cntrl[0] == 'PASSED':
        return list_cntrl[1]
    logging.error('Testcase %s is blocked due to: %s', tcName, list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    ogging.error('Testcase %s is blocked due to: %s', tcName, get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# pool creation
#-------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

for x in range(0, 3):
        TSM_IPs[x] = conf['ipVSM%s' %(x+1)]
        TSM_interface[x] = conf['interfaceVSM%s' %(x+1)]
        TSM_dnsserver[x] = conf['dnsVSM%s' %(x+1)]
        if TSM_IPs[x] == '' and TSM_interface[x] == '' and TSM_dnsserver[x] \
                == '':
                    print 'Value for ipVSM/interfaceVSM/dnsVSM getting None'
                    logging.debug('Value for key ipVSM/interfaceVSM/dnsVSM '\
                            'is None, specify correct values in config file')
                    logging.debug('create pool, create vsms for regression test '\
                            'is blocked')
                    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
        logging.debug('Value foe key \'ipVSM%s\' is: %s', (x+1), \
                conf['ipVSM%s' %(x+1)])
        logging.debug('Value foe key \'interfaceVSM%s\' is: %s', (x+1), \
                conf['interfaceVSM%s' %(x+1)])
        logging.debug('Value foe key \'dnsVSM%s\' is: %s', (x+1), \
                conf['dnsVSM%s' %(x+1)])

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

###---getting pool id----------------------------------------------------------
pool_result = listPool(STDURL)
if pool_result[0] == 'FAILED':
    print 'Not able to get Pools...'
    logging.error('create pool, create vsms for regression test is blocked...')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
elif pool_result[0] == 'BLOCKED':
    print 'There is no pool...'
    logging.debug('create pool, create vsms for regression test is')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
else:
    pools = pool_result[1]

pool_info = get_pool_info(pools, POOL_NAME)
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
    logging.error('create pool, create vsms for regression test is blocked, '\
            'Error: %s', account_id[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
print account_id
#------------------------------------------------------------------------------

###creating 5 TSM--------------------------------------------------------------
for x in range(1, 4):
    tsm_dict = {'name': 'T100%s' %(x), 'accountid': account_id, 'poolid': \
            pool_id, 'totaliops': '1000', 'quotasize': '1T', 'tntinterface': \
            str(TSM_interface[x-1]), 'dnsserver': str(TSM_dnsserver[x-1]), \
            'ipaddress': str(TSM_IPs[x-1]), 'totalthroughput': '4000'}
    #calling create TSM method...
    result = create_tsm(tsm_dict, STDURL)
    if result[0] == 'FAILED':
        print 'Not able to create VSM/TSM %s' %(tsm_dict.get('name'))
        logging.error('Not able to create VSM/TSM %s', result[1])
        logging.debug('create pool, create vsms for regression test is blocked...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
#------------------------------------------------------------------------------

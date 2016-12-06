
'''
###############################################################################################################
# Testcase Name : Continuous_Archival_Ops_NFS                                                                 #
#                                                                                                             #
# Testcase Description : This test performs the following actions :                                           #
#                        a) Creates multiple large file of specified size on the NFS volume,                  #
#                        b) writes into the above file                                                        #
#                        c) reads from the above file and                                                     # 
#                        d) zips file after a fixed period with timestamp                                     #
#                        e) Moves file into backup location (another NFS volume)                              #
#                                                                                                             #
#                                                                                                             # 
# Testcase Pre-Requisites : Controllers have to be in available state                                         #
#                                                                                                             #
# Testcase Creation Date : 08/05/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 23/05/2016                                                                         #  
#                                                                                                             #  
# Modifications made : a) Added step to flush cache buffers before read                                       #  
#                                                                                                             #
# Testcase Author : Karthik                                                                                   #
###############################################################################################################
'''

# Import necessary packages and methods

import sys
import json
import logging
from time import ctime
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        get_apikey, mountNFS, executeCmd, sshToOtherClient, putFileToController
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, UMain
from haUtils import get_controller_info, list_controller, get_value, get_node_IP
from poolUtils import listPool, get_pool_info, getFreeDisk, getDiskToAllocate, \
        create_pool, listDiskGroup, delete_pool
from accountUtils import get_account_id
from tsmUtils import listTSMWithIP_new, create_tsm, delete_tsm
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new, get_volume_info

# Clear the log file before execution starts

executeCmd('> logs/automation_execution.log')

# Initialization for Logging location 
tcName = sys.argv[0]
tcName = tcName.split('.py')[0]
logFile = tcName + '.log'
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
       filename='logs/'+logFile,filemode='a',level=logging.DEBUG)

# Initialization for few common global variables

startTime = ctime()
HEADER_MSG = 'Testcase "%s" is started' %tcName
FOOTER_MSG = 'Testcase "%s" is completed' %tcName
BLOCKED_MSG = 'Testcase "%s" is blocked' %tcName
EXECUTE_SYNATX = 'python %s.py conf.txt' %tcName

logging.info('%s', HEADER_MSG)

# Check for correct usage of script

check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNATX, FOOTER_MSG, BLOCKED_MSG, startTime)

# Get necessary params and values from config file (conf.txt)

conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

POOL_TYPE = conf['pool_type']
NUM_POOL_DISKS = conf['num_pool_disks']
POOL_DISK_TYPE = conf['pool_disk_type']
POOL_IOPS = conf['pool_iops']
POOL_NAME = 'POOLTEST'

VSM_IP = conf['ipVSM1']
VSM_INTERFACE = conf['interfaceVSM1']
VSM_DNS = conf['dnsVSM1']
VSM_NAME = 'VSMTEST'

VOL1_NAME = 'VolTest1'
VOL2_NAME = 'VolTest2'

VOL1_IOPS = int(POOL_IOPS)/2
VOL2_IOPS = VOL1_IOPS

CLIENT1_IP = conf['Client1_IP']
CLIENT1_USER = conf['Client1_user'] 
CLIENT1_PASSWORD = conf['Client1_pwd']

CLIENT_NFS_MOUNT_PNT_1 = '/mnt/nfs_source'
CLIENT_NFS_MOUNT_PNT_2 = '/mnt/nfs_backup'

logging.debug('DEVMAN_IP: %s', DEVMAN_IP)
logging.debug('USER: %s', USER)
logging.debug('PASSWORD: %s', PASSWORD)
logging.debug('VSM_IP: %s', VSM_IP)
logging.debug('APIKEY: %s', APIKEY)
logging.debug('STDURL: %s', STDURL)

# definitions for some methods used in this script

def verify_list_controller(list_cntrl, startTime):
    if list_cntrl[0] == 'PASSED':
        return list_cntrl[1]
    logging.error('Testcase %s is blocked due to' \
            ': %s',tcName, list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Getting controller info and state before creating pool

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
    logging.error('The single node in HAgroup is in maintenance, testcase cannot proceed')
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

pool_params = {'name': POOL_NAME, 'siteid': site_id, 'clusterid': ctrl_cluster_id, \
        'controllerid': ctrl_id, 'iops': POOL_IOPS, 'diskslist': allocatable_diskidlist, \
        'grouptype': POOL_TYPE}

# Pool creation step

pool_creation = create_pool(pool_params, STDURL)
if pool_creation[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
           ' : %s', tcName, pool_creation[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Obtain the Pool list for before extracting the name

pool_list = listPool(STDURL)
if pool_list[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, pool_list[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
pool_list = pool_list[1]

# Get the pool_info for the desired from the list obtained above

#pool_info = get_pool_info(pool_list, POOL_NAME)
pool_info = get_pool_info(pool_list, None)
if pool_info[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
           ' : %s', tcName, pool_info[1])

# Extract the pool_id from the info obtained for said pool above

pool_id = pool_info[1] # Note that in get_pool_info return value, pool_info[1] itself is ID

# Get account ID for VSM creation

account_id = get_account_id(STDURL, None) # 2nd param is acc_name, if None, taken as 1st acc
if account_id[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
           ': %s', tcName, account_id[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
account_id = account_id[1]

# Provide variables for VSM creation (from conf & hardcode) in dict format 

vsm_dict = {'name': VSM_NAME, 'accountid': account_id, 'poolid': \
        pool_id, 'totaliops': POOL_IOPS, 'quotasize': '1T', 'tntinterface': \
        VSM_INTERFACE, 'dnsserver': VSM_DNS, \
        'ipaddress': VSM_IP, 'totalthroughput': 4*int(POOL_IOPS)}

# Create VSM using the pool_id and the params received from conf file

result = create_tsm(vsm_dict, STDURL) # This method is an aberration, elsewhere STDURL is 1st param
if result[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Get the info for the VSM created above (this list method response contains id, not create, so needed)

vsm = listTSMWithIP_new(STDURL, VSM_IP)
if vsm[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, tsm[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
vsminfo = vsm[1]
print vsminfo

# Extract the vsm_id & vsm_dataset_id from info obtained above

vsm_id = vsminfo[0].get('id')
vsm_dataset_id = vsminfo[0].get('datasetid')

# Provide variables for Volume1 & Volume2 creation (from conf & hardcode) in dict format 

vol1_dict = {'name': VOL1_NAME, 'quotasize': '500G', 'tsmid': vsm_id, 'iops': VOL1_IOPS, \
        'datasetid': vsm_dataset_id, 'protocoltype': 'NFS'}

vol2_dict = {'name': VOL2_NAME, 'quotasize': '500G', 'tsmid': vsm_id, 'iops': VOL2_IOPS, \
        'datasetid': vsm_dataset_id, 'protocoltype': 'NFS'}

# Create Volume1 & Volume2 using the vsm_ids and params specified 

result = create_volume(vol1_dict, STDURL)
verify_create_volume(result)

result = create_volume(vol2_dict, STDURL)
verify_create_volume(result)

# Get the info for the Volume created above (this list method response contains id, etc.., not create, so needed)

volumes = listVolumeWithTSMId_new(STDURL, vsm_id)
if volumes[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, volumes[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
volumes = volumes[1]

# Extract the vol_id & vol_mnt_pt for both volumes from info obtained above

'''
for vol in volumes:
    vol_id = vol.get('id')
    vol_mnt_pt = vol.get('mountpoint')
'''

vol1_info = get_volume_info(volumes, VOL1_NAME)
vol1_id, vol1_mnt_pt = vol1_info[2], vol1_info[3]
print vol1_id, vol1_mnt_pt

vol2_info = get_volume_info(volumes, VOL2_NAME)
vol2_id, vol2_mnt_pt = vol2_info[2], vol2_info[3]
print vol2_id, vol2_mnt_pt

# Updating nfs client access property for both volume

result = addNFSclient(STDURL, vol1_id, 'ALL')
if result[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

result = addNFSclient(STDURL, vol2_id, 'ALL')
if result[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Form the command to mount source & destintion, will be sent to client for execution

source_mkdir_cmd = 'mkdir %s' %(CLIENT_NFS_MOUNT_PNT_1) # Way to assign string where using %s
source_mount_cmd = 'mount -o mountproto=tcp,sync %s:/%s %s' %(VSM_IP, vol1_mnt_pt, CLIENT_NFS_MOUNT_PNT_1)
source_check_mount_cmd = 'df -h | grep %s | awk {\'print $NF\'}' %(vol1_mnt_pt)

dest_mkdir_cmd = 'mkdir %s' %(CLIENT_NFS_MOUNT_PNT_2) # Way to assign string where using %s
dest_mount_cmd = 'mount -o mountproto=tcp,sync %s:/%s %s' %(VSM_IP, vol2_mnt_pt, CLIENT_NFS_MOUNT_PNT_2)
dest_check_mount_cmd = 'df -h | grep %s | awk {\'print $NF\'}' %(vol2_mnt_pt)

# Perform the source nfs mount on the client machine

mkdir_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, source_mkdir_cmd)
mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, source_mount_cmd)
check_mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, source_check_mount_cmd)
check_mount_result = check_mount_result.strip('\n') # printing last column

if CLIENT_NFS_MOUNT_PNT_1 == check_mount_result:
    print "Source Volume is mounted successfully"
else:
    print "Source Volume is not mounted successfully" 
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, mount_result)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Perform the dest nfs mount on the client machine

mkdir_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, dest_mkdir_cmd)
mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, dest_mount_cmd)
check_mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, dest_check_mount_cmd)
check_mount_result = check_mount_result.strip('\n') # printing last column

if CLIENT_NFS_MOUNT_PNT_2 == check_mount_result:
    print "Destination Volume is mounted successfully"
else:
    print "Destination Volume is not mounted successfully"
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, mount_result)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Transfer the shell script that will run the workload 

src_file = 'AMSx-WLAx-NSWx-NFSx-xxxx-AUX1_ARCHIVAL_FILE_OPS.py'
dst_file = src_file
file_transfer_result = putFileToController(CLIENT1_IP, CLIENT1_PASSWORD, src_file, dst_file)

# Form the command that will run the workload on the NFS mount point

run_workload_cmd = 'python %s %s %s' %(src_file, CLIENT_NFS_MOUNT_PNT_1, CLIENT_NFS_MOUNT_PNT_2)

# Note the time when the workload starts

startTime = ctime()

# Run the File Create Read ModifyWrite Delete Ops on the NFS mount point for 5 iterations

sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, run_workload_cmd)

# Note the time when the workload execution has completed

endTime = ctime()

# Grep the workload script's log file to verify successful run

test_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, \
        'grep -w "CREATED\|MODIFIED\|ARCHIVED\|DELETED" Archival.log | wc -l')
if int(test_result) > 4:
    print "Workload has run successfully"
    logging.info('Testcase %s is successfully completed', tcName)
    resultCollection('Testcase %s is :' %tcName, \
            ['PASSED', ''], startTime, endTime)
else:
    logging.error('Testcase %s is failed,' \
            'look at client logs', tcName)
    resultCollection('Testcase %s is :' %tcName, \
            ['FAILED', ''], startTime, endTime)


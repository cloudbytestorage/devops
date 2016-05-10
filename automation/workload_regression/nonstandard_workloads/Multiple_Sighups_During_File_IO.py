'''
###############################################################################################################
# Testcase Name : Multiple_Sighups_During_File_IO                                                             #
#                                                                                                             #
# Testcase Description : This test performs the following actions continuously for fixed set of iterations :  #
#                        a) Initiates multiple sighups by issuing <sh /usr/local/cb/bin/services_bkptenant    #
#                           nfs sighup> command                                                               #
#                        b) Verify IOPS are running on the NFS shares                                         #
#                                                                                                             # 
#                                                                                                             #
# Testcase Creation Date : 27/04/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 27/04/2016                                                                         #  
#                                                                                                             #  
# Modifications made : None                                                                                   #  
#                                                                                                             #
# Testcase Author : Mardan                                                                                    #
###############################################################################################################
'''

# Import necessary packages and methods
import sys
import json
import time
import logging
from time import ctime
from accountUtils import get_account_id
from vdbenchUtils import executeVdbenchFile, kill_vdbench
from tsmUtils import listTSMWithIP_new, create_tsm, delete_tsm
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new
from haUtils import get_controller_info, list_controller, get_value, get_node_IP
from cbrequest import get_url, configFile, sendrequest, mountNFS, get_apikey, \
        executeCmd, sshToOtherClient, resultCollection, getControllerInfo, \
        putFileToController
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_iops_by_api
from poolUtils import listPool, get_pool_info, getFreeDisk, getDiskToAllocate, \
        create_pool, listDiskGroup, delete_pool

# Clear configuration before this test begins

'''
CleanUpResult = CleanUp(STDURL)
if CleanUpResult[0] == 'FAILED':
    logging.error('Cleanup before starting testcase Multiple_Sighups_During_File_IO')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
'''

# Clear the log file before execution starts

#executeCmd('> logs/automation_execution.log')

# Initialization for Logging location 

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/Multiple_Sighups_During_File_IO.log', filemode = 'a', \
        level = logging.DEBUG)
# Initialization for few common global variables

startTime = ctime()
HEADER_MSG = 'Testcase "Multiple_Sighups_During_File_IO" is started'
FOOTER_MSG = 'Testcase "Multiple_Sighups_During_File_IO" is completed'
BLOCKED_MSG = 'Testcase "Multiple_Sighups_During_File_IO" is blocked'
EXECUTE_SYNATX = 'python Multiple_Sighups_During_File_IO.py conf.txt'

logging.info('%s', HEADER_MSG)

# Check for correct usage of script

check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNATX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

# Get necessary params and values from config file (conf.txt)

conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
NODE_PSWD = conf['node_pswd']
APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

POOL_TYPE = conf['pool_type']
NUM_POOL_DISKS = conf['num_pool_disks']
POOL_DISK_TYPE = conf['pool_disk_type']
POOL_IOPS = conf['pool_iops']
POOL_NAME = 'POOLTEST'

VSM_IP = conf['ipVSM2']
VSM_INTERFACE = conf['interfaceVSM2']
VSM_DNS = conf['dnsVSM2']
VSM_NAME = 'VSMTESTM1'

VOL_NAME = 'VolTestM1'

CLIENT1_IP = conf['Client1_IP']
CLIENT1_USER = conf['Client1_user'] 
CLIENT1_PASSWORD = conf['Client1_pwd']

CLIENT_NFS_MOUNT_PNT = '/mnt/nfs_cont_file_ops_multiple_small'

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
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s',list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', result[1])
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
    logging.error('The single node in HAgroup is in maintenance, testcase '\
            'cannot proceed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Steps to get free disk list for pool creation
'''
freedisk = getFreeDisk(ctrl_disks)
if freedisk[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
           ': %s', freedisk[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
freedisk = freedisk[1]

# Steps to get allocatable disks for pool (based on size, type etc..,)

allocatable_diskidlist = getDiskToAllocate(freedisk, NUM_POOL_DISKS, POOL_DISK_TYPE)
if allocatable_diskidlist[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', allocatable_diskidlist[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
allocatable_diskidlist = allocatable_diskidlist[1]

# Get params for pool creation (Needs controller, pool info etc..,)

pool_params = {'name': POOL_NAME, 'siteid': site_id, 'clusterid': ctrl_cluster_id, \
        'controllerid': ctrl_id, 'iops': POOL_IOPS, 'diskslist': allocatable_diskidlist, \
        'grouptype': POOL_TYPE}

# Pool creation step

pool_creation = create_pool(pool_params, STDURL)
if pool_creation[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
           ' : %s', pool_creation[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

'''
# Obtain the Pool list for before extracting the name

pool_list = listPool(STDURL)
if pool_list[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', pool_list[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
pool_list = pool_list[1]

# Get the pool_info for the desired from the list obtained above

#pool_info = get_pool_info(pool_list, POOL_NAME)
pool_info = get_pool_info(pool_list, None)
if pool_info[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
           ' : %s', pool_info[1])

# Extract the pool_id from the info obtained for said pool above

pool_id = pool_info[1] # Note that in get_pool_info return value, pool_info[1] itself is ID

# Get account ID for VSM creation

account_id = get_account_id(STDURL, None) # 2nd param is acc_name, if None, taken as 1st acc
if account_id[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
           ': %s', account_id[1])
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
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Get the info for the VSM created above (this list method response contains id, not create, so needed)
vsm = listTSMWithIP_new(STDURL, VSM_IP)
if vsm[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', tsm[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
vsminfo = vsm[1]
print vsminfo
# Extract the vsm_id & vsm_dataset_id from info obtained above

vsm_id = vsminfo[0].get('id')
vsm_dataset_id = vsminfo[0].get('datasetid')
account_name = vsminfo[0].get('accountname')
# Provide variables for Volume creation (from conf & hardcode) in dict format 

vol_dict = {'name': VOL_NAME, 'tsmid': vsm_id, 'iops': POOL_IOPS, \
        'datasetid': vsm_dataset_id, 'protocoltype': 'NFS'}

# Create Volume using the vsm_ids and params specified 

result = create_volume(vol_dict, STDURL)
verify_create_volume(result)

# Get the info for the Volume created above (this list method response 
#contains id, etc.., not create, so needed)

volumes = listVolumeWithTSMId_new(STDURL, vsm_id)
if volumes[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', volumes[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
volumes = volumes[1]

# Extract the vol_id & vol_mnt_pt from info obtained above

for vol in volumes:
    if vol['name'] == '%s' %(VOL_NAME):
        vol_id = vol.get('id')
        vol_mnt_pt = vol.get('mountpoint')
        break

# Updating nfs client access property for volume

result = addNFSclient(STDURL, vol_id, 'ALL')
if result[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)


# Form the command to mount, will be sent to client for execution

mkdir_cmd = 'mkdir %s' %(CLIENT_NFS_MOUNT_PNT) # Way to assign string where using %s
mount_cmd = 'mount -o mountproto=tcp,sync %s:/%s %s' %(VSM_IP, vol_mnt_pt, CLIENT_NFS_MOUNT_PNT)
check_mount_cmd = 'mount | grep %s' %(vol_mnt_pt)

# Perform the nfs mount on the client machine

mkdir_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, mkdir_cmd)
mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, mount_cmd)
check_mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, check_mount_cmd)
if '%s' %(vol_mnt_pt) in str(check_mount_result):
    print "Volume is mounted successfully"
else:
    print "Volume is not mounted successfully" 
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', mount_result)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# Creating Dictionary for vdbench use
dic_for_vdbench_use = {'name': VOL_NAME, 'mountPoint': CLIENT_NFS_MOUNT_PNT}

# Executing vdbench
logging.info('...executing vdbench....')
executeVdbenchFile(dic_for_vdbench_use, 'filesystem_nfs')
data_size = 1000
# wait till vdbench complete seeding...
time.sleep(60) # sleep according to data size given for seeding

# verofy iops are running or not 
iops = get_iops_by_api(vol_id, STDURL)
if iops[0] == 'FAILED':
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', iops[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

iops = iops[1]
if iops > 0:
    print 'iops are running fine...'
    logging.info('IOPS are running fine after starting of vdbench..., '\
            'iops value is: %s', iops)
else:
    print 'iops are not running...'
    logging.debug('IOPS are not running after starting of vdbench...')
    logging.error('Testcase Multiple_Sighups_During_File_IO is blocked due ' \
            'to IOPS are not running')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

# getting jail id for issuing sighup command directly
cmd = 'jls | grep %s | awk \'{print $1}\'' %(VSM_IP)
jail_id = getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'IOPS.txt')
logging.info('jail id: %s', jail_id)

logging.info('Going to execute multiple sighups...')
cmd = 'sh /usr/local/cb/bin/services_bkptenant nfs sighup %s' %(jail_id)
getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'sighup.txt')

time.sleep(5)
getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'sighup.txt')

time.sleep(5)
getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'sighup.txt')

time.sleep(5)
getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'sighup.txt')

time.sleep(5)
getControllerInfo(ctrl_ip, NODE_PSWD, cmd, 'sighup.txt')

# verying IOPS after multiple sighups
iops = get_iops_by_api(vol_id, STDURL)
if iops[0] == 'FAILED':
    logging.error('estcase Multiple_Sighups_During_File_IO is blocked due to' \
            ': %s', iops[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

iops = iops[1]
endTime = ctime()
if iops > 0:
    print 'IOPS are running fine after multiple sighups also'
    logging.info('IOPS are running fine after multiple sighups, iops '\
            'value is: %s', iops)
    logging.info('Testcase Multiple_Sighups_During_File_IO is PASSED...')
    resultCollection('Multiple_Sighups_During_File_IO test case is:', \
            ['PASSED', ''], startTime, endTime)
else:
    print 'IOPS are not running after multiple sighups'
    logging.info('IOPS are not running after multiple sighups...')
    logging.info('Testcase Multiple_Sighups_During_File_IO is FAILED...')
    resultCollection('Multiple_Sighups_During_File_IO test case is:', \
            ['FAILED', ''], startTime, endTime)

# --------- cleaning all the configuration created for this test case ---------
# 1 killing vdbench
kill_vdbench()

# sleeping for 20 seconds after killing vdbench, 
#it wil take some time to erlease the mount point
#time.sleep(20)

# umount the NFS share
umount_result = executeCmd('umount %s' %(CLIENT_NFS_MOUNT_PNT))
'''
# going to delete the nfs share
delete_vol = delete_volume(vol_id, STDURL)
if delete_vol[0] == 'FAILED':
    print 'Volume deleetion failed after running multiple sighup test case'
    logging.debug('Volume deletion failed after running multiple sighup '\
            'test case, error is : %s', delete_vol[1])
    logging.debug('Since volume is not deleted, not going to delete VSM')
    get_logger_footer('Multiple_Sighups_During_File_IO test case is completed')
    exit()

# Volume deleted successfully, going to deete VSMs 
logging.debug('Volume deleted bsuccessfully, going to deete VSMs ')
delete_vsm = delete_tsm(vsm_id, STDURL)
if delete_vsm[0] == 'FAILED':
    print 'VSM deleetion failed after running multiple sighup test case'
    logging.debug('VSM deletion failed after running multiple sighup '\
            'test case, error is : %s', delete_vsm[1])
    logging.debug('Since VSM is not deleted, not going to delete pool')
    get_logger_footer('Multiple_Sighups_During_File_IO test case is completed')
    exit()

# VSM deleted successfully, oging to delete pool
logging.debug('VSM deleted successfully, going to delete pool')
delete_pool = delete_pool(pool_id, STDURL)
if delete_pool[0] == 'FAILED':
    print 'Not able to delete pool'
    logging.error('Not able to delete pool due to: %s', delete_pool[1])
    get_logger_footer('Multiple_Sighups_During_File_IO test case is completed')
    exit()

# all the configuration created for this test cases is deleted
get_logger_footer('Multiple_Sighups_During_File_IO test case is completed')
'''
# ------------------------------- cleanig done --------------------------------

'''
###############################################################################################################
# Testcase Name : AMSx-WLAx-SWxx-GENx-VDBx-TC_WORKLOAD_SIMULATION_TEST.py                                     #
#                                                                                                             #
# Testcase Description : This test performs the following actions continuously for fixed set of iterations :  #
---------------------------------- filesystem configuration templates ----------------------------------------#
                    1. Fconf1: File-100-FSyncWrite-Random-RandomFileselect-Conf                               #
                    2. Fconf2: File-100-FSyncWrite-Random-SequentialFileselect-Conf                           #
                    3. Fconf3: File-100-Read-Random-RandomFileselect-Conf                                     #
                    4. Fconf4: File-100-Read-Random-SequentialFileselect-Conf                                 #
                    5. Fconf5: File-100-Read-Sequential-RandomFileselect-Conf                                 #
                    6. Fconf6: File-100-Read-Sequential-SequentialFileselect-Conf                             #
                    7. Fconf7: File-100-SyncWrite-Random-RandomFileselect-Conf                                #
                    8. Fconf8: File-100-SyncWrite-Random-SequentialFileselect-Conf                            #
                    9. Fconf9: File-100-SyncWrite-Sequential-RandomFileselect-Conf                            #
                    10. Fconf10: File-100-SyncWrite-Sequential-SequentialFileselect-Conf                      #
                    11. Fconf11: File-80R20W-Random-RandomFileselect-Conf                                     #
                    12. Fconf12: File-Attr-Test-Conf                                                          #
                    13. Fconf13: File-Compression-Workload-Conf                                               #
                    14. Fconf14: File-Create-Write-Read-Delete-Conf                                           #
                    15. Fconf15: File-Dedupe-Workload-Conf                                                    #
                    16. Fconf16: File-Read-Shared-Access-Conf                                                 #
                    17. Fconf17: File-Recursive-Structure-Write-Read-Conf                                     #
                    18. Fconf18: File-Write-Shared-Access-Conf                                                #
                                                                                                              #
------------------------------------ rawconfiguration templates ----------------------------------------------#
                    1. Rconf1: Raw-100-Read-Random-Conf                                                       #
                    2. Rconf2: Raw-100-Read-Sequential-Conf                                                   #
                    3. Rconf3: Raw-100-Write-Random-Conf                                                      #
                    4. Rconf4: Raw-100-Write-Sequential-Conf                                                  #
                    5. Rconf5: Raw-80R20W-Random-Conf                                                         #
                    6. Rconf6: Raw-Access-Beyond-2TB-Conf                                                     #
                    7. Rconf7: Raw-Hot-Banding-Conf                                                           #
                    8. Rconf8: Raw-Random-Range-Workload-Conf                                                 #
                    9. Rconf9: Raw-Streamed-workload-Conf                                                     #
                    10. Rconf10: Raw-Stride-Read-Write-Conf                                                   #
#                                                                                                             # 
#                                                                                                             #
# Testcase Creation Date : 31/05/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 15/11/2016                                                                         #  
#                                                                                                             #  
# Modifications made : vdbench changes, log and result addition, conf changes                                                                                   #  
#                                                                                                             #
# Testcase Author : Mardan, Karthik                                                                                    #
###############################################################################################################
'''

# Import necessary packages and methods
import sys
import json
import time
import logging
import datetime
from time import ctime
from accountUtils import get_account_id
from vdbenchUtils import executeVdbench, createRunTimeConfig, vdParseAndPlotImage
from tsmUtils import listTSMWithIP_new, create_tsm, delete_tsm
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new, getDiskAllocatedToISCSI, mount_iscsi
from haUtils import get_controller_info, list_controller, get_value, get_node_IP
from cbrequest import get_url, configFile, sendrequest, get_apikey, executeCmd,\
        sshToOtherClient, resultCollection, getControllerInfo, mountNFS_new, \
        putFileToController
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_iops_by_api, UMain, assign_iniator_gp_to_LUN, discover_iscsi_lun, \
        iscsi_login_logout, execute_mkfs
from poolUtils import listPool, get_pool_info, getFreeDisk, getDiskToAllocate, \
        create_pool, listDiskGroup, delete_pool

indianTime = datetime.datetime.now()

# getting the test case name
tcName = sys.argv[0]
tcName = tcName.split('.py')[0]

# creating log file with test case name
logFile = tcName + '.log'

# Initialization for Logging location 
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
        filename='logs/'+logFile,filemode='a',level=logging.DEBUG)

# Clear the log file before execution starts
executeCmd('> logs/%s' %(logFile))

# Initialization for few common global variables

startTime = ctime()
HEADER_MSG = 'Testcase "%s" is started' %(tcName)
FOOTER_MSG = 'Testcase "%s" is completed' %(tcName)
BLOCKED_MSG = 'Testcase "%s" is blocked' %(tcName)
EXECUTE_SYNATX = 'python %s.py conf.txt nfs/iscsi' %(tcName)

logging.info('%s', HEADER_MSG)

# Check for correct usage of script

check_mendatory_arguments(sys.argv, 3, EXECUTE_SYNATX, FOOTER_MSG, \
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
PROTOCOL_TYPE = (sys.argv[2]).lower()

WORKLOAD_TYPE = (conf['workload_type']).split()

if len(WORKLOAD_TYPE) == 1:
    # lower() will return as string but we need as list, 
    # split will convert it again in list
    
    WORKLOAD_TYPE = conf['workload_type'].lower().split()

# lower() will return as string but we need as list,
#split will convert it again in list
DEVICE_TYPE = conf['device_type'].lower().split()

ACTIVE_DATA_SIZE = conf['size']
RUN_TIME = conf['elapsed']
NUMBER_OF_FILES = conf['files']
NUMBER_OF_THREADS = conf['threads']

# creating a dictionary with user given values in conf.txt file to... 
# ...create config file to run vdbench
userValues = {'anchor': '', 'size': ACTIVE_DATA_SIZE, 'elapsed': RUN_TIME, \
        'files': NUMBER_OF_FILES, 'threads': NUMBER_OF_THREADS}

if WORKLOAD_TYPE == 'filesystem' and (DEVICE_TYPE == 'raw' or DEVICE_TYPE == \
        'both'):
    print 'If workload_type is "filesystem" than device_type should be '\
            '"filesystem"'
    logging.debug('If workload_type is "filesystem" than device_type should '\
            'be "filesystem"')
    logging.info('%s is blocked', tcName)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
elif WORKLOAD_TYPE == 'raw' and (DEVICE_TYPE == 'filesystem' or DEVICE_TYPE \
        == 'both'):
    print 'If workload_type is "raw" than device_type should be "raw"'
    logging.debug('If workload_type is "raw" than device_type should be "raw"')
    logging.info('%s is blocked', tcName)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
elif (WORKLOAD_TYPE == 'raw' or DEVICE_TYPE == 'raw') and PROTOCOL_TYPE == 'nfs':
    print 'workload_type should be "filesystem/ALL/or perticular Fconf name" '\
            'and device_type should be "filesystem" if PROTOCOL_TYPE is NFS'
    logging.debug('workload_type should be "filesystem/ALL/or perticular Fconf'\
            ' name" and device_type should be "filesystem" if PROTOCOL_TYPE is NFS')
    logging.info('%s is blocked', tcName)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

POOL_TYPE = conf['pool_type']
NUM_POOL_DISKS = conf['num_pool_disks']
POOL_DISK_TYPE = conf['pool_disk_type']
POOL_IOPS = conf['pool_iops']
POOL_NAME = 'PLTestVdb'

VSM_IP = conf['ipVSM1']
VSM_INTERFACE = conf['interfaceVSM1']
VSM_DNS = conf['dnsVSM1']
VSM_NAME = 'VSMTestVdb1'

logging.debug('DEVMAN_IP: %s', DEVMAN_IP)
logging.debug('USER: %s', USER)
logging.debug('PASSWORD: %s', PASSWORD)
logging.debug('VSM_IP: %s', VSM_IP)
logging.debug('APIKEY: %s', APIKEY)
logging.debug('STDURL: %s', STDURL)

# definitions for some methods used in this script
def getAllFileConfig():
    filesystemConfig = {'Fconf1': 'File-100-FSyncWrite-Random-RandomFileselect-Conf', 
            'Fconf2': 'File-100-FSyncWrite-Random-SequentialFileselect-Conf',
            'Fconf3': 'File-100-Read-Random-RandomFileselect-Conf',
            'Fconf4': 'File-100-Read-Random-SequentialFileselect-Conf',
            'Fconf5': 'File-100-Read-Sequential-RandomFileselect-Conf',
            'Fconf6': 'File-100-Read-Sequential-SequentialFileselect-Conf',
            'Fconf7': 'File-100-SyncWrite-Random-RandomFileselect-Conf',
            'Fconf8': 'File-100-SyncWrite-Random-SequentialFileselect-Conf',
            'Fconf9': 'File-100-SyncWrite-Sequential-RandomFileselect-Conf',
            'Fconf10': 'File-100-SyncWrite-Sequential-SequentialFileselect-Conf',
            'Fconf11': 'File-80R20W-Random-RandomFileselect-Conf',
            'Fconf12': 'File-Attr-Test-Conf',
            'Fconf13': 'File-Compression-Workload-Conf',
            'Fconf14': 'File-Create-Write-Read-Delete-Conf',
            'Fconf15': 'File-Dedupe-Workload-Conf',
            'Fconf16': 'File-Read-Shared-Access-Conf',
            'Fconf17': 'File-Recursive-Structure-Write-Read-Conf',
            'Fconf18': 'File-Write-Shared-Access-Conf'
            }
    return filesystemConfig

def getAllRawConfig():
    rawConfig = {'Rconf1': 'Raw-100-Read-Random-Conf',
            'Rconf2': 'Raw-100-Read-Sequential-Conf',
            'Rconf3': 'Raw-100-Write-Random-Conf',
            'Rconf4': 'Raw-100-Write-Sequential-Conf',
            'Rconf5': 'Raw-80R20W-Random-Conf',
            'Rconf6': 'Raw-Access-Beyond-2TB-Conf',
            'Rconf7': 'Raw-Hot-Banding-Conf',
            'Rconf8': 'Raw-Random-Range-Workload-Conf',
            'Rconf9': 'Raw-Streamed-workload-Conf',
            'Rconf10': 'Raw-Stride-Read-Write-Conf'
            }
    return rawConfig

def getSelectedConfig(WORKLOAD_TYPE, allConfigFiles):
    newConfigFiles = {}
    for values in WORKLOAD_TYPE:
        if values in allConfigFiles:
            newConfigFiles[values] = allConfigFiles[values]
            print values
    return newConfigFiles

def verify_list_controller(list_cntrl, startTime):
    if list_cntrl[0] == 'PASSED':
        return list_cntrl[1]
    logging.error('Testcase %s is blocked due to: %s', tcName, list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    logging.error('Testcase %s is blocked due to: %s', tcName, get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('Testcase %s is blocked due to: %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_mount(mountResult):
    if mountResult[0] == 'PASSED':
        return
    logging.error('Testcase %s is blocked due to: %s', tcName, mountResult[1])
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
        logging.error('Testcase %s is blocked getting volid:%s, '\
                'accountid:%s, voliqn: %sand mntpoint: %s', tcName, volid, \
                accountid, voliqn, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, voliqn, accountid, mntpoint

def  verify_add_auth_gp(add_auth_group, auth_gp):
    if add_auth_group[0] == 'FAILED':
        logging.debug('Testcase %s is blocked Not able to assign auth' \
                'group %s to LUN', tcName, auth_gp)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('Testcase %s is blocked getting iqn is None', tcName)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_iscsi_operation(result, vol_name, action):
    if result[0] == 'PASSED':
        logging.debug('%s successfully for iSCSI LUN %s', action, vol_name)
        return
    logging.error('Testcase %s is blocked Not able to %s %s, Error: '\
            '%s', tcName, action, vol_name, str(result[1]))
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

def getiSCSIDevice(volName, vsm_id, POOL_IOPS, vsm_dataset_id, STDURL):
    volumeDict = {'name': volName, 'tsmid': vsm_id, 'datasetid': \
            vsm_dataset_id, 'protocoltype': 'ISCSI', 'iops': POOL_IOPS, \
            'quotasize': '20G'}
    result = create_volume(volumeDict, STDURL)
    verify_create_volume(result)
    logging.info('listing volume...')
    volumes = listVolumeWithTSMId_new(STDURL, vsm_id)
    if volumes[0] == 'FAILED':
        logging.error('Testcase %s is blocked due to' \
                ': %s', tcName, volumes[1])
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    volumes = volumes[1]
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
    iscsiDevice = verify_getDiskAllocatedToISCSI(result, mnt_point)
    return iscsiDevice, vol_id, account_id, mnt_point, iqn

# Getting controller info and state before creating pool
#'''
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

pool_params = {'name': POOL_NAME, 'siteid': site_id, 'clusterid': ctrl_cluster_id, \
        'controllerid': ctrl_id, 'iops': POOL_IOPS, 'diskslist': allocatable_diskidlist, \
        'grouptype': POOL_TYPE}
# creating pool
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

pool_info = get_pool_info(pool_list, POOL_NAME)
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
#'''
result = create_tsm(vsm_dict, STDURL) # This  method is an aberration, ... 
                                      # ...elsewhere STDURL is 1st param
if result[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
#'''
# Get the info for the VSM created above (this list method response...
# ...contains id, not create, so needed)
vsm = listTSMWithIP_new(STDURL, VSM_IP)
if vsm[0] == 'FAILED':
    logging.error('Testcase %s is blocked due to' \
            ': %s', tcName, tsm[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
vsminfo = vsm[1]
# Extract the vsm_id & vsm_dataset_id from info obtained above

vsm_id = vsminfo[0].get('id')
vsm_dataset_id = vsminfo[0].get('datasetid')
account_name = vsminfo[0].get('accountname')
# VSM creation done, it will be common for all the vdbench run
# '''
### starting of vdbench configurations------------------------------------------

if PROTOCOL_TYPE == 'nfs':
    pass
elif PROTOCOL_TYPE == 'iscsi':
    pass
else:
    print 'Please give protocol type (nfs or iscsi) as parameter of script'
    exit()

# fileConfigFiles = filesystem configuration files
if PROTOCOL_TYPE == 'nfs':
    if WORKLOAD_TYPE[0] == 'all' or WORKLOAD_TYPE[0] == 'filesystem':
        print 'All the filesystem vdbench config file to execute'
        logging.debug('All the filesystem vdbench config file to execute')
        fileConfigFiles = getAllFileConfig()
    else:
        print 'creating list of filesystem vdbench config file to be execute'
        logging.debug('creating list of filesystem vdbench config file to be '\
                'execute')
        fileConfigFiles = getSelectedConfig(WORKLOAD_TYPE, getAllFileConfig())
 
    for key in fileConfigFiles:
        vdConfigFileName = fileConfigFiles[key]

        VOL_NAME = key

        confFile = VOL_NAME # creating a configuration file as VOL_NAME
        
        # output directory for vdbench
        outputDir = '%s_%s' %(VOL_NAME, indianTime.isoformat())

        # Provide variables for Volume creation (from conf & hardcode) in dict format
        volumeDict = {'name': VOL_NAME, 'tsmid': vsm_id, 'iops': POOL_IOPS, \
                'datasetid': vsm_dataset_id, 'protocoltype': 'NFS', 'quotasize': '20G'}

        # Create Volume using the vsm_ids and params specified 
        result = create_volume(volumeDict, STDURL)
        verify_create_volume(result)

        # Get the info for the Volume created above (this list method response 
        #contains id, etc.., not create, so needed)
        volumes = listVolumeWithTSMId_new(STDURL, vsm_id)
        if volumes[0] == 'FAILED':
            logging.error('Testcase %s is blocked due to' \
                    ': %s', tcName, volumes[1])
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
            logging.error('Testcase %s is blocked due to' \
                    ': %s', result[1])
            is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

        # mounting the NFS share to client
        volDir = {'mountPoint': vol_mnt_pt, 'TSMIPAddress': VSM_IP, 'name': \
                VOL_NAME}

        mountResult = mountNFS_new(volDir)
        verify_mount(mountResult)
        volMntPoint = 'mount/%s' %(vol_mnt_pt)
	userValues['anchor'] = volMntPoint
        
        #copying perticular vdconf template to new file to execute vdbench
        vdBenchConfig = '%s' %(vol_mnt_pt)
        executeCmd('cp vdbench/templates/%s vdbench/%s' %(vdConfigFileName, vdBenchConfig))

        #updating configuration file before executing vdbench
        createRunTimeConfig('vdbench/%s' %(vdBenchConfig), userValues)
        
        # Executing vdbench
        executeVdbench(vdBenchConfig, outputDir)
	
	flatfile = '%s/flatfile.html' %(outputDir)
	#vdParseAndPlotImage(flatfile, 'rate')
	#vdParseAndPlotImage(flatfile, 'resp')
	#vdParseAndPlotImage(flatfile, 'MB/sec')

        time.sleep(2)
        umountResult = executeCmd('umount %s' %(volMntPoint))
        #UMain(volMntPoint)
        delete_volume(vol_id, STDURL)
        time.sleep(2)
    exit()

# iscsi implementation
fileConfigFiles = {}
rawConfigFiles = {}
if WORKLOAD_TYPE[0] == 'all':
    if DEVICE_TYPE[0] == 'filesystem':
        print 'All the filesystem vdbench config file to execute'
        fileConfigFiles = getAllFileConfig()
    elif DEVICE_TYPE[0] == 'raw':
        print 'All the raw vdbench config file to execute'
        rawConfigFiles = getAllRawConfig()
    elif DEVICE_TYPE[0] == 'both':
        print 'All the raw and filesystem vdbench config file to execute'
        fileConfigFiles = getAllFileConfig()
        rawConfigFiles = getAllRawConfig()
    else:
        print '"DEVICE_TYPE can be filesystem, raw, or both"'
        exit()

elif WORKLOAD_TYPE[0] == 'filesystem':
    print 'All the filesystem vdbench config file to execute'
    fileConfigFiles = getAllFileConfig()

elif WORKLOAD_TYPE[0] == 'raw':
    print 'All the raw vdbench config file to execute'
    rawConfigFiles = getAllRawConfig()
else:
     print 'creating list of vdbench config file to be execute'
     fileConfigFiles = getSelectedConfig(WORKLOAD_TYPE, getAllFileConfig())
     rawConfigFiles = getSelectedConfig(WORKLOAD_TYPE, getAllRawConfig())

fileExecutions = len(fileConfigFiles)
rawExecutions = len(rawConfigFiles)
if fileExecutions == rawExecutions == 0:
    print 'Please provide atleast one config file to execute vdbench'
    exit()

for key in fileConfigFiles:
    vdConfigFileName = fileConfigFiles[key]
    VOL_NAME = key
    
    confFile = VOL_NAME # creating a configuration file as VOL_NAME
    
    # output directory for vdbench
    outputDir = '%s_%s' %(VOL_NAME, indianTime.isoformat())
    
    #copying perticular vdconf template to new file to execute vdbench
    executeCmd('cp vdbench/templates/%s vdbench/%s' %(vdConfigFileName, VOL_NAME))
    iscsiDevice, vol_id, account_id, vol_mnt_point, iqn = \
            getiSCSIDevice(VOL_NAME, vsm_id, POOL_IOPS, vsm_dataset_id, STDURL)
    result = execute_mkfs(iscsiDevice, 'ext3')
    verify_execute_mkfs(result)
    mountResult = mount_iscsi(iscsiDevice, VOL_NAME)
    verify_mount(mountResult)
    volMntPoint = 'mount/%s' %(VOL_NAME)
    userValues['anchor'] = volMntPoint

    #updating configuration file before executing vdbench
    createRunTimeConfig('vdbench/%s' %(VOL_NAME), userValues)
    
    executeVdbench(confFile, outputDir)
    flatfile = '%s/flatfile.html' %(outputDir)
    #vdParseAndPlotImage(flatfile, 'rate')
    #vdParseAndPlotImage(flatfile, 'resp')
    #vdParseAndPlotImage(flatfile, 'MB/sec')
    
    time.sleep(2)
    umountResult = executeCmd('umount %s' %(volMntPoint))
    login_result = iscsi_login_logout(iqn, VSM_IP, 'logout')
    verify_iscsi_operation(login_result, VOL_NAME, 'logout')
    add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')
    verify_add_auth_gp(add_auth_group, 'None')
    time.sleep(2)
    delete_volume(vol_id, STDURL)
    time.sleep(2)
    executeCmd('rm -rf vdbench/%s' %(VOL_NAME))

for key in rawConfigFiles:
    vdConfigFileName = rawConfigFiles[key]
    VOL_NAME = key
    
    confFile = VOL_NAME # creating a configuration file as VOL_NAME
    
    # output directory for vdbench
    outputDir = '%s_%s' %(VOL_NAME, indianTime.isoformat())
    
    #copying perticular vdconf template to new file to execute vdbench
    executeCmd('cp vdbench/templates/%s vdbench/%s' %(vdConfigFileName, VOL_NAME))
    iscsiDevice, vol_id, account_id, vol_mnt_point, iqn = \
            getiSCSIDevice(VOL_NAME, vsm_id, POOL_IOPS, vsm_dataset_id, STDURL)
    
    userValues['anchor'] = '/dev/%s' %(iscsiDevice)
    
    #updating configuration file before executing vdbench
    createRunTimeConfig('vdbench/%s' %(VOL_NAME), userValues)

    executeVdbench(confFile, outputDir)
    
    flatfile = '%s/flatfile.html' %(outputDir)
    #vdParseAndPlotImage(flatfile, 'rate')
    #vdParseAndPlotImage(flatfile, 'resp')
    #vdParseAndPlotImage(flatfile, 'MB/sec')
    
    time.sleep(2)
    login_result = iscsi_login_logout(iqn, VSM_IP, 'logout')
    verify_iscsi_operation(login_result, VOL_NAME, 'logout')
    add_auth_group = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')
    verify_add_auth_gp(add_auth_group, 'None')
    time.sleep(2)
    delete_volume(vol_id, STDURL)
    time.sleep(2)
    executeCmd('rm -rf vdbench/%s' %(VOL_NAME))

import os
import sys
import time
import json
import logging
import subprocess
from math import floor
from time import ctime
from cbrequest import get_apikey, get_url, umountVolume, mountNFS, \
        resultCollection, resultCollectionNew, configFile, getoutput, \
        executeCmd, getControllerInfoAppend, passCmdToController
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
        delete_volume, listVolumeWithTSMId_new
from tsmUtils import get_tsm_info, listTSMWithIP_new, create_tsm, \
        editNFSthreads, delete_tsm
from haUtils import change_node_state, get_controller_info, list_controller, \
        get_value
from utils import is_blocked, check_alerts, updateGlobalSettings, \
        get_IOPS_values_from_node
from accountUtils import listAccount_new, get_account_info, create_account, \
        delete_account
from vdbenchUtils import kill_vdbench, is_vdbench_alive
from poolUtils import listPool, get_pool_info, listPoolWithControllerId, \
        getFreeDisk, getDiskToAllocate, create_pool, listDiskGroup, \
        get_value_from_diskGroup, disklistID, addDiskGroup, delete_diskGroup, \
        delete_pool, replaceDisk, listSharedDisk

###steps followed in pool lifecycle
#1. provisioning and deprovisioning of all types of pool
#2.  provisioning and deprovisioning of pool in ha degraded state
#3.  provisioning and deprovisioning of spare/zil/cache/metavdev
#4. creating pool - tsm - nfs vol - mounting the share
#5. while IOS are running provisioning and deprovisioning cache and zil
#6. filling pool and volume above 80% and checking alerts
#7. replace of disk which is in use while IOs are running
#8. adding cache collecting read/writes
#9. adding vdev collecting read/writes
#10. deleting cache
#11. killing vdbench
#12. deprovisioning volume - tsm - pool

# note disk req is 4 if single type of disk is used to run this testcase
# 2 ssd needed(based on pool type) to verify metavdev, else that case is failed 
# SSD disks for log, log_mirror and cache is must else blocking that case
#SSD requried is 2

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)
logging.info('---Start of testcase "Testing pool life cycle"-----')

if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows...'
    print 'python pool_lifecycle.py conf.txt'
    logging.error('Arguments are not correct...')
    exit()

startTime = ctime()
FOOTER_MSG = 'pool life cycle test case completed'
BLOCKED_MSG = 'pool life cycle test case is'
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
node_passwd = config['node1_passwd']
node_ip = config["node1"]

#--------------------------------UPDATE HERE-----------------------------------
#disk type to verify all type of pool creation
#minimum disk requried is 4

#pool_disk_type = 'SAS'
pool_disk_type = 'SSD'

#disk type for cache, log, log_mirror creation(SSD must)
##by default SSD for metavdev creation
grp_disk = 'SSD'

#for main  pool creation(2), vdev(2) specify one type of disk
#minimum disk requried is 4

#final_disk_type = 'SAS'
final_disk_type = 'SSD'
final_pool_type = 'raidz1'
final_no_of_disk = 2  #for pool creation and vdev


###to enable iscsi Reservation (comment it if already enabled)
cmd = 'touch /etc/disablescsi'
#enable_iscsiReservation =  passCmdToController(node_ip, 'test', cmd)

###----------------------------------METHODS-----------------------------------

def mountPointDetails(mountPoint):
    df = subprocess.Popen(["df", "-m", "%s" %(mountPoint)], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    output = ' '.join(output.splitlines()[1:])
    filesystem, size, used, available, percent, mountpoint = output.split()
    return [filesystem, size, used, available, percent, mountpoint]

def writingVDBfile(volume, vol_size, vdbNewFile):
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    old_size = 'volumeSize'
    vdb_path = 'vdbench/%s' %vdbNewFile
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " \
        %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), vdb_path))
    res = executeCmd("sed -i 's/%s/%s/' %s " \
        %(old_size.replace('/', '\/'), vol_size.replace('/', '\/'), vdb_path))

def get_disklist_id(num_of_disks, disk_type, NODE1_IP):
    ###getting disk list ID
    list_cntrl = list_controller(stdurl)
    controllers = verify_list_controller(list_cntrl, startTime)
    get_info = get_controller_info(NODE1_IP, controllers)
    verify_get_controller_info(get_info, startTime)
    status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
            site_id  = get_value(get_info)
    free_disks =  getFreeDisk(ctrl_disks)
    if free_disks[0] == 'FAILED':
        return ['FAILED', free_disks[1]]
    disklist_id = getDiskToAllocate(free_disks[1], num_of_disks, disk_type)
    if disklist_id[0] == 'FAILED':
        print disklist_id[1]
        logging.error('Pool creation is blocked, due to : %s', disklist_id[1])
        return ['FAILED', disklist_id[1]]
    return ['PASSED', disklist_id[1]]

def get_pool_params(pool_name, pool_type, site_id, ctrl_id, ctrl_cluster_id, \
        disklist_id):
    pool_params = {'name': pool_name, 'siteid': site_id, \
            'clusterid': ctrl_cluster_id, 'controllerid': ctrl_id, \
            'iops': 5000, 'diskslist': disklist_id, 'grouptype': pool_type}
    return pool_params

def get_node_ip(controllers):
    node_ip_list = []
    num_of_Nodes = 0
    for controller in controllers:
        num_of_Nodes = num_of_Nodes + 1
        nodeIP  = controller.get('ipAddress')
        nodeName = controller.get('name')
        node_ip_list.append(nodeIP)
    return node_ip_list, num_of_Nodes

def verify_list_controller(list_cntrl, startTime):
    if list_cntrl[0] == 'PASSED':
        return list_cntrl[1]
    logging.error('Pool life cycle test case is blocked due to: %s', \
            list_cntrl[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_controller_info(get_info, startTime):
    if get_info[0] == 'PASSED':
        return
    logging.error('Pool life cycle test case is blocked due to: %s', \
            get_info[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def __create_pool(pool_name, pool_type, num_of_disks, disk_type, ctrl_disks,\
        site_id, ctrl_id, ctrl_cluster_id):
    disklist_id = get_disklist_id(num_of_disks, disk_type, NODE1_IP)
    if disklist_id[0] == 'FAILED':
        logging.error('%s', disklist_id[1])
        endTime = ctime()
        resultCollection('%s Pool creation' %(pool_type), ['BLOCKED', ''], \
                startTime, endTime)
        return ['FAILED', '']
    else:
        pool_params = get_pool_params(pool_name, pool_type, site_id, ctrl_id, \
                ctrl_cluster_id, disklist_id[1])
        pool_creation = create_pool(pool_params, stdurl)
        logging.debug('%s', pool_creation)
        endTime = ctime()
        if pool_creation[0] == 'PASSED':
            resultCollection('%s Pool creation' %(pool_type), ['PASSED', ''], \
                    startTime, endTime)
            return ['PASSED', '']
        resultCollection('%s Pool creation' %(pool_type), ['FAILED', ''], \
                startTime, endTime)
        return ['FAILED', '']

def get_pool_id(pools, pool_name):
    pool_id = None
    for pool in pools:
        if pool['name'] == pool_name:
            pool_id = pool['id']
    return pool_id

def verify_list_pool(list_pool, startTime):
    if list_pool[0] == 'PASSED':
        return list_pool[1]
    logging.error('Pool life cycle test case is blocked due to: %s', \
            list_pool[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_pool_info(get_poolInfo, startTime):
    if get_poolInfo[0] == 'PASSED':
        return
    logging.error('Pool life cycle test case is blocked due to: %s', \
            get_poolInfo[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_list_account(list_acct, startTime):
    if list_acct[0] == 'PASSED':
        return list_acct[1]
    logging.error('Pool life cycle test case is blocked due to: %s', \
            list_acct[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_get_acct_info(get_accInfo, startTime):
    if get_accInfo[0] == 'PASSED':
        return
    logging.error('Pool life cycle test case is blocked due to: %s', \
            get_accInfo[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def addDisk(pool_type, pool_id,  no_of_disk, group_type, disk_type, NODE1_IP):
    list_cntrl = list_controller(stdurl)
    if list_cntrl[0] == 'FAILED':
        return ['FAILED', list_cntrl[1]]
    cntrl_values =  get_controller_info(NODE1_IP, list_cntrl[1])
    if cntrl_values[0] == 'FAILED':
        return ['FAILED' ,cntrl_values[1]]
    disks_avail = getFreeDisk(cntrl_values[6])
    if disks_avail[0] == 'FAILED':
        return ['FAILED',disks_avail[1]]
    if group_type  in  ('cache', 'log', 'log mirror', 'log_mirror'):
        if disk_type == 'SSD':
            disk_list_id = getDiskToAllocate(disks_avail[1], \
                    no_of_disk, disk_type)
            if disk_list_id[0] == 'FAILED':
                return ['FAILED', disk_list_id[1]]
        else:
            return ['FAILED', 'To add disk group "%s", require SSD disk' %group_type]
    else:
        diskGroupList =  listDiskGroup(pool_id, stdurl)
        if diskGroupList[0] == 'FAILED':
            return ['FAILED', diskGroupList[1]]
        disk_details = get_value_from_diskGroup(diskGroupList[1], pool_type)
        if disk_details[0] ==  'FAILED':
            return ['FAILED', disk_details[1]]
        disk_list_id = disklistID(disk_details[1], disk_type, no_of_disk, \
                        disks_avail[1])
        if disk_list_id[0] ==  'FAILED':
            return ['FAILED', disk_list_id[1]]
    diskGroup = addDiskGroup(pool_id, cntrl_values[5], group_type, \
            disk_list_id[1], 4096, stdurl)
    if diskGroup[0] ==  'FAILED':
        return ['FAILED', diskGroup[1]]
    else:
        return ['PASSED', 'Successfully added the disk group']

###delete disk group
def delDisk(group_type, pool_id, stdurl):
    diskGroupList =  listDiskGroup(pool_id, stdurl)
    if diskGroupList[0] == 'FAILED':
        return ['FAILED', diskGroupList[1]]
    disk_details = get_value_from_diskGroup(diskGroupList[1], group_type)
    if disk_details[0] == 'FAILED':
        return ['FAILED', disk_details[1]]
    del_disk = delete_diskGroup(disk_details[3], stdurl)
    if del_disk[0] == 'FAILED':
        return ['FAILED', del_disk[1]]
    else:
        return ['PASSED', 'Successfully deleted the disk group']

def meta_creation(num_of_disks, disk_type, NODE1_IP, pool_id, \
        ctrl_cluster_id, group_type):
    disklist_id = get_disklist_id(num_of_disks, disk_type, NODE1_IP)
    if disklist_id[0] == 'FAILED':
        return ['FAILED', disklist_id[1]]
    diskGroup = addDiskGroup(pool_id, ctrl_cluster_id, group_type, \
            disklist_id[1], 4096, stdurl)
    if diskGroup[0] == 'FAILED':
        return ['FAILED', diskGroup[1]]
    else:
        return ['PASSED', 'Successfully added the disk group']

def multiple_of_num(num, multiple):
    rem = num % multiple
    if rem == 0:
        return num
    else:
        num = num + multiple - rem
        return num

def verify_alert_result(alert_result, category, startTime):
    endTime = ctime()
    if alert_result[0] == 'PASSED':
        logging.debug('Getting alert for %s test case passed', category)
        resultCollection('Getting alert for \'%s\' test case:' %(category), \
                ['PASSED', ''], startTime, endTime)
    else:
        logging.debug('Getting alert for \'%s\' test case failed', category)
        resultCollection('Getting alert for %s test case:' %(category), \
                ['FAILED', ''], startTime, endTime)

##can replace 1 disk at a time
### no_of_disk = 1
def to_replace_disk(pool_type, pool_id,  no_of_disk, disk_type, NODE1_IP):
    list_cntrl = list_controller(stdurl)
    if list_cntrl[0] == 'FAILED':
        return ['FAILED', list_cntrl[1]]
    cntrl_values =  get_controller_info(NODE1_IP, list_cntrl[1])
    if cntrl_values[0] == 'FAILED':
        return ['FAILED' ,cntrl_values[1]]
    disks_avail = getFreeDisk(cntrl_values[6])
    if disks_avail[0] == 'FAILED':
        return ['FAILED',disks_avail[1]]
    diskGroupList =  listDiskGroup(pool_id, stdurl)
    if diskGroupList[0] == 'FAILED':
        return ['FAILED', diskGroupList[1]]
    disk_details = get_value_from_diskGroup(diskGroupList[1], pool_type)
    if disk_details[0] == 'FAILED':
        return ['FAILED', disk_details[1]]
    shared_disk = listSharedDisk(pool_id, disk_details[3], stdurl)
    if shared_disk[0] == 'FAILED':
        return ['FAILED', shared_disk[1]]
    else:
        #ramdomly taking one disk id for diskgroup list
        for shared_disks in shared_disk[1]:
            pool_disk_id = shared_disks.get('id') #current disk to be replaced
            pool_disk_label = shared_disks.get('disklabel')
            logging.debug('Disk which is going to be replaced is %s: %s', \
                    pool_disk_label, pool_disk_id)
            break
    disk_list_id = disklistID(disk_details[1], disk_type, no_of_disk, \
                        disks_avail[1])
    if disk_list_id[0] == 'FAILED':
        return ['FAILED', disk_list_id[1]]
    disk_replace = replaceDisk(pool_disk_id, disk_list_id[1], \
            disk_details[3], stdurl)
    if disk_replace[0] == 'FAILED':
        return ['FAILED', disk_replace[1]]
    else:
        return ['PASSED', 'Successfully replaced disk with id "%s" '\
                'by disk with id "%s"' %(pool_disk_id, disk_list_id[1])]
###---------------------------------END OF METHODS-----------------------------------------------

logging.info('Pool life cycle testcases started....')
resultCollectionNew('-------------------POOL LIFECYCLE TESTCASES STARTS'\
        '--------------------',['',''])
startTime = ctime()
list_cntrl = list_controller(stdurl)
controllers = verify_list_controller(list_cntrl, startTime)

#getting controllers IP address for futther use
controllers_ip, num_of_Nodes = get_node_ip(controllers)
if num_of_Nodes == 1:
    NODE1_IP = controllers_ip[0]
elif num_of_Nodes == 2:
    NODE1_IP = controllers_ip[0]
    NODE2_IP = controllers_ip[1]
else:
    logging.debug('Number of Nodes are more than 2, please revisit the code')
    exit()

get_info = get_controller_info(NODE1_IP, controllers)
verify_get_controller_info(get_info, startTime)
status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
        site_id  = get_value(get_info)

logging.info('Provisioning and deprovisioning of different types of pool....')
resultCollectionNew('\nPROVISIONING AND DEPROVISIONING OF DIFFERRENT TYPES OF '\
                    'POOLS....', ['', ''])
#creating stripe pool
startTime = ctime()
create_result = __create_pool('strp_pool1', 'stripe', 1, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)

if create_result[0] == 'PASSED':
    pools = listPoolWithControllerId(stdurl, ctrl_id)
    pool_id = get_pool_id(pools[1], 'strp_pool1')
    if pool_id is not None:
        delete_result = delete_pool(pool_id, stdurl)
        endTime = ctime()
        if delete_result[0] == 'FAILED':
            resultCollection('stripe Pool deletion' , ['FAILED', ''], \
                        startTime, endTime)
        resultCollection('stripe Pool deletion' , ['PASSED', ''], \
                startTime, endTime)

#creating mirror pool
startTime = ctime()
create_result = __create_pool('mirr_pool1', 'mirror', 2, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)
if create_result[0] == 'PASSED':
    pools = listPoolWithControllerId(stdurl, ctrl_id)
    pool_id = get_pool_id(pools[1], 'mirr_pool1')
    if pool_id is not None:
        delete_result = delete_pool(pool_id, stdurl)
        endTime = ctime()
        if delete_result[0] == 'FAILED':
            resultCollection('mirror Pool deletion' , ['FAILED', ''], \
                            startTime, endTime)
        resultCollection('mirror Pool deletion' , ['PASSED', ''], \
                        startTime, endTime)

#creating single parity pool
startTime = ctime()
create_result = __create_pool('z1_pool1', 'raidz1', 2, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)

if create_result[0] == 'PASSED':
    pools = listPoolWithControllerId(stdurl, ctrl_id)
    pool_id = get_pool_id(pools[1], 'z1_pool1')
    if pool_id is not None:
        delete_result = delete_pool(pool_id, stdurl)
        endTime = ctime()
        if delete_result[0] == 'FAILED':
            resultCollection('raidz1 Pool deletion' , ['FAILED', ''], \
                            startTime, endTime)
        resultCollection('raidz1 Pool deletion' , ['PASSED', ''], \
                startTime, endTime)

#creating double parity pool
startTime = ctime()
create_result = __create_pool('z2_pool1', 'raidz2', 3, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)

if create_result[0] == 'PASSED':
    pools = listPoolWithControllerId(stdurl, ctrl_id)
    pool_id = get_pool_id(pools[1], 'z2_pool1')
    if pool_id is not None:
        delete_result = delete_pool(pool_id, stdurl)
        endTime = ctime()
        if delete_result[0] == 'FAILED':
            resultCollection('raidz2 Pool deletion' , ['FAILED', ''], \
                            startTime, endTime)
        resultCollection('raidz2 Pool deletion' , ['PASSED', ''], \
                    startTime, endTime)

#creating triple parity pool
startTime = ctime()
create_result = __create_pool('z3_pool1', 'raidz3', 4, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)

if create_result[0] == 'PASSED':
    pools = listPoolWithControllerId(stdurl, ctrl_id)
    pool_id = get_pool_id(pools[1], 'z3_pool1')
    if pool_id is not None:
        delete_result =  delete_pool(pool_id, stdurl)
        endTime = ctime()
        if delete_result[0] == 'FAILED':
            resultCollection('raidz3 Pool deletion' , ['FAILED', ''], \
                    startTime, endTime)
        resultCollection('raidz3 Pool deletion' , ['PASSED', ''], \
                    startTime, endTime)

logging.info('Provisioning and deprovisioning of different types of '\
        'pool finished....') 
resultCollectionNew('END OF PROVISIONING AND DEPROVISIONING OF DIFFERRENT '\
        'TYPES OF POOLS....', ['', ''])

###-----------------------------------------------------------------------
### Pool creation check in HA degraded state
logging.info('Verifying Pool provisioning and deprovising when HAGroup '\
        'in degraded state....')
resultCollectionNew('\nVERIFYING POOL PROVISIONING AND DEPROVISIONING WHEN '\
        'HAGROUP IN DEGRADED STATE....', ['', ''])
startTime = ctime()
pool_creation_check = False
#changing node Node2 to maintenance state, to degrade the HA Group
node_maint = change_node_state(stdurl, NODE2_IP, 'maintenance')
if node_maint[0] == 'PASSED':
    print 'Node state is changed to maintenance'
    logging.debug('Node with IP: %s successfully moved to maintenance', \
            NODE2_IP)
    pool_creation_check = True
    resultCollectionNew('HAGroup is in degraded state....', ['', ''])
else:
    logging.debug('Provisioning of pool when HA Group is in degraded state is '\
            'blocked due to failed to move node with IP "%s" '\
            'to maintenance', NODE2_IP) 
    endTime = ctime()
    resultCollection('Provisioning of pool when HA Group is in degraded state is: ',\
            ['BLOCKED',''], startTime, endTime)

if pool_creation_check:
    #creating mirror parity pool
    startTime = ctime()
    create_result = __create_pool('Pool_HAdegrade1', 'mirror', 2, pool_disk_type, \
            ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)
    if create_result[0] == 'PASSED':
        endTime = ctime()
        logging.debug('Provisioning of pool when HA Group is in degraded state '\
                'is successfull')
        logging.debug('Going to delete recently created pool...')
        pools = listPoolWithControllerId(stdurl, ctrl_id)
        pool_id = get_pool_id(pools[1], 'Pool_HAdegrade1')
        if pool_id is not None:
            delete_result = delete_pool(pool_id, stdurl)
            endTime = ctime()
            if delete_result[0] == 'FAILED':
                resultCollection('mirror Pool deletion ' , ['FAILED', ''], \
                        startTime, endTime)
            resultCollection('mirror Pool deletion ' , ['PASSED', ''], \
                    startTime, endTime)
    
    startTime = ctime()
    create_result = __create_pool('Pool_HAdegrade2', 'raidz1', 2, pool_disk_type, \
            ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)
    if 'PASSED' in create_result:
        endTime = ctime()
        logging.debug('Provisioning of pool when HA Group is in degraded state '\
                'is successfull')

    ##changing node state to available    
    startTime = ctime()
    node_avail = change_node_state(stdurl, NODE2_IP, 'available')
    if node_avail[0] == 'PASSED':
        print 'Node state is changed to available'
        logging.debug('Node with IP: %s successfully moved to available', \
                            NODE2_IP)
    else:
        endTime = ctime()

        logging.debug('Failed to move node with ip "%s" to available state '\
                'after provisioning pool in degraded HA group', NODE2_IP)
        resultCollection('Moving node state to available is failed',\
                ['BLOCKED',''], startTime, endTime)
    
    startTime = ctime()
    if create_result[0] == 'PASSED':
        pools = listPoolWithControllerId(stdurl, ctrl_id)
        pool_id = get_pool_id(pools[1], 'Pool_HAdegrade2')
        if pool_id is not None:
            delete_result = delete_pool(pool_id, stdurl)
            endTime = ctime()
            if delete_result[0] == 'FAILED':
                resultCollection('raidz1 Pool deletion' , ['FAILED', ''], \
                            startTime, endTime)
            resultCollection('raidz1 Pool deletion' , ['PASSED', ''], \
                        startTime, endTime)

logging.info('End of verifying pool provisioning and deprovisioning when '\
        'HAGroup in degraded state....')
resultCollectionNew('END OF VERIFYING POOL PROVISIONING AND DEPROVISIONING '\
        'WHEN HAGROUP IN DEGRADED STATE....', ['', ''])

###----------------------------------------------------------------------------------------
## add spare/metadev/zil/cache
logging.info('Verifying provisioning and deprovision of '\
        'spare/zil/cache/metavdevs....')
resultCollectionNew('\nVERIFYING PROVISIONING AND DEPROVISIONING OF '\
        'SPARE/ZIL/CACHE/METAVDEVS....', ['', ''])

#creating single parity pool
startTime = ctime()
create_result = __create_pool('z1_pool', 'raidz1', 2, pool_disk_type, \
        ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)

pools = listPoolWithControllerId(stdurl, ctrl_id)
pool_id = get_pool_id(pools[1], 'z1_pool')
pool_type = 'raidz1'

##Spare
startTime = ctime()
group_type1 = 'spare'
add_disks1 = addDisk(pool_type, pool_id, 2, group_type1, \
        pool_disk_type, NODE1_IP)
endTime = ctime()
if 'FAILED' in str(add_disks1):
    print add_disks1[1]
    logging.error('%s', add_disks1[1])
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Successfully added disk group "%s"' %group_type1
    logging.debug('Successfully added disk group "%s"', group_type1)
    resultCollection('"%s" disk Group addition' %group_type1,\
            ['PASSED', ''], startTime, endTime)

    time.sleep(2)
    startTime = ctime()
    del_disks1 = delDisk(group_type1, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks1:
        print del_disks1[1]
        logging.error('%s', del_disks1[1])
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type1
        logging.debug('Successfully deleted the disk group "%s"', group_type1)
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['PASSED', ''], startTime, endTime)

##log       
startTime = ctime()
group_type1 = 'log'
add_disks1 = addDisk(pool_type, pool_id, 1, group_type1, \
        grp_disk, NODE1_IP)
endTime = ctime()
if 'FAILED' in str(add_disks1):
    print add_disks1[1]
    logging.error('%s', add_disks1[1])
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Successfully added disk group "%s"' %group_type1
    logging.debug('Successfully added disk group "%s"', group_type1)
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['PASSED', ''], startTime, endTime)

    time.sleep(2)
    startTime = ctime()
    del_disks1 = delDisk(group_type1, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks1:
        print del_disks1[1]
        logging.error('%s', del_disks1[1])
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type1
        logging.debug('Successfully deleted the disk group "%s" ', group_type1)
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['PASSED', ''], startTime, endTime)

###log_mirror      
startTime = ctime()
group_type1 = 'log_mirror'
add_disks1 = addDisk(pool_type, pool_id, 2, group_type1, \
        grp_disk, NODE1_IP)
endTime = ctime()
if 'FAILED' in str(add_disks1):
    print add_disks1[1]
    logging.error('%s', add_disks1[1])
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Successfully added disk group "%s"' %group_type1
    logging.debug('Successfully added disk group "%s"', group_type1)
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['PASSED', ''], startTime, endTime)

    time.sleep(2)
    startTime = ctime()
    del_disks1 = delDisk(group_type1, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks1:
        print del_disks1[1]
        logging.error('%s', del_disks1[1])
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type1
        logging.debug('Successfully deleted the disk group "%s" ', group_type1)
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['PASSED', ''], startTime, endTime)

##cache
startTime = ctime()
group_type1 = 'cache'
add_disks1 = addDisk(pool_type, pool_id, 1, group_type1, \
        grp_disk, NODE1_IP)
endTime = ctime()
if 'FAILED' in str(add_disks1):
    print add_disks1[1]
    logging.error('%s', add_disks1[1])
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Successfully added disk group "%s"' %group_type1
    logging.debug('Successfully added disk group "%s"', group_type1)
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['PASSED', ''], startTime, endTime)

    time.sleep(2)
    startTime = ctime()
    del_disks1 = delDisk(group_type1, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks1:
        print del_disks1[1]
        logging.error('%s', del_disks1[1])
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type1
        logging.debug('Successfully deleted the disk group "%s" ', group_type1)
        resultCollection('"%s" disk Group deletion' %group_type1, \
                ['PASSED', ''], startTime, endTime)


###metavdev
startTime = ctime()
meta = updateGlobalSettings('ui.pool.metavdev.option.enable', 'true', stdurl)
endTime = ctime()
if 'FAILED' in meta:
    logging.info('Failed to enable metavdev in global setting')
    resultCollection('Enabling metavdev in global setting', \
                        ['FAILED', ''], startTime, endTime)
else:
    logging.info('Successfully  enabled metavdev in global setting')
    resultCollection('Enabling metavdev in global setting', \
                    ['PASSED', ''], startTime, endTime)

##for metavdev SSD disk is must, else this case will be failed
startTime = ctime()
group_type1 = 'meta_raidz1'
add_disks1 = meta_creation(2, 'SSD', NODE1_IP, pool_id, ctrl_cluster_id, group_type1)
endTime = ctime()
if 'FAILED' in str(add_disks1):
    print add_disks1[1]
    logging.error('%s', add_disks1[1])
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Successfully added disk group "%s"' %group_type1
    logging.debug('Successfully added disk group "%s"', group_type1)
    resultCollection('"%s" disk Group addition' %group_type1, \
            ['PASSED', ''], startTime, endTime)

startTime = ctime()
delete_result = delete_pool(pool_id, stdurl)
endTime = ctime()
if delete_result[0] == 'FAILED':
    resultCollection('raidz1 Pool deletion' , ['FAILED', ''], \
                        startTime, endTime)
else:
    resultCollection('raidz1 Pool deletion' , ['PASSED', ''], \
            startTime, endTime)

startTime = ctime()
meta = updateGlobalSettings('ui.pool.metavdev.option.enable', 'false', stdurl)
endTime = ctime()
if 'FAILED' in meta:
    logging.info('Failed to disable metavdev in global setting')
    resultCollection('Disabling metavdev in global setting', \
                        ['FAILED', ''], startTime, endTime)
else:
    logging.info('Successfully  disabled metavdev in global setting')
    resultCollection('Disabling metavdev in global setting', \
                    ['PASSED', ''], startTime, endTime)

logging.info('End of verifying provisioning and deprovisioning of '\
        'spare/zil/cache/metavdevs....')
resultCollectionNew('END OF VERIFYING PROVISIONING AND DEPROVISIONING OF '\
        'SPARE/ZIL/CACHE/METAVDEVS....', ['', ''])

###---------------------------------------------------------------------------------------
# creating raidz1 pool for executing other pool life cycle test cases
logging.info('Creation of Raidz1 pool, tsm and volume....')
resultCollectionNew('\nCREATION OF RAIDZ1_POOL, TSM, VOLUME....', ['', ''])

list_cntrl = list_controller(stdurl)
controllers = verify_list_controller(list_cntrl, startTime)
get_info = get_controller_info(NODE1_IP, controllers)
verify_get_controller_info(get_info, startTime)
status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
        site_id  = get_value(get_info)

pool_name = 'Poolz1'
#pool_type = 'raidz1'

#pool type, disk type and no. of disks are dependent for adding vdev
#if you are changing these parameters please make sure change..
#in adding vdev to the same pool
startTime = ctime()
create_result = __create_pool(pool_name, final_pool_type, final_no_of_disk, \
        final_disk_type, ctrl_disks, site_id, ctrl_id, ctrl_cluster_id)
if create_result[0] == 'FAILED':
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
###---------------------------------------------------------------------------

###create TSM and volume and exposing to client
list_pool = listPool(stdurl)
pools = verify_list_pool(list_pool, startTime)
get_poolInfo =  get_pool_info(pools, pool_name)
verify_get_pool_info(get_poolInfo, startTime)
pool_id = get_poolInfo[1]
pool_size = get_poolInfo[2]

startTime = ctime()
acct_name = 'Account'
account_creation = create_account(acct_name, stdurl)
if account_creation[0] == 'FAILED' and 'already exists' in str(account_creation[1]):
    logging.debug('%s, getting the same account...', account_creation[1])
elif account_creation[0] == 'FAILED':
    logging.error('Not able to create account, Error: %s', account_creation[1])
    logging.error('Pool life cycle test case is blocked due to account '\
            'creation failed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
else:
    logging.debug('Account %s is created successfully...', acct_name)

list_acct = listAccount_new(stdurl)
accounts = verify_list_account(list_acct, startTime)
get_accInfo =  get_account_info(accounts, acct_name) 
verify_get_acct_info(get_accInfo, startTime)
acct_id = get_accInfo[1]

pool_size = '%sM' %(pool_size)
tsm_params = {'name' : 'VSMz1', 'ipaddress': config["ipVSM1"] , \
        'accountid': acct_id, 'poolid': pool_id, \
        'tntinterface': config["interfaceVSM1"], 'quotasize':pool_size, \
        'totaliops': 5000} #, 'totalthroughput': 0}
#tsm_params['totalthroughput'] = tsm_params['totaliops']*4
#tsm_params['totalthroughput'] = tsm_params['totaliops']*128 #for 1.p6 build

startTime = ctime()
tsm_creation =  create_tsm(tsm_params, stdurl)
if 'FAILED' in tsm_creation:
    print tsm_creation[1]
    logging.error('Pool life cycle test case is blocked due to: %s', \
                tsm_creation[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
else:
    endTime = ctime()
    resultCollection('%s TSM/VSM creation' %tsm_params['name'], \
            ['PASSED', ''], startTime, endTime)
    logging.debug('%s TSM/VSM created successfully', tsm_params['name'])

tsm_ip = tsm_params['ipaddress']
list_tsm = listTSMWithIP_new(stdurl, tsm_ip)
if 'FAILED' in list_tsm:
    msg = 'Failed to list tsm for given IP : "%s"' %tsm_ip
    logging.error('Pool life cycle test case is blocked due to: %s', msg)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

get_tsmInfo = get_tsm_info(list_tsm[1])
tsm_id = get_tsmInfo[0]
tsm_name = get_tsmInfo[1]
dataset_id = get_tsmInfo[2]
tsm_quota = get_tsmInfo[4]
#print tsm_quota
Nfs_threads =  editNFSthreads(tsm_id, 256, stdurl)
if Nfs_threads[0] == 'FAILED':
    logging.debug('%s', Nfs_threads[1])
else:
    logging.debug('Nfs threads is successfully updated to 256')

#volume dictionary for creating volume
vol = {'name': 'NFSvolz1', 'tsmid': tsm_id, 'datasetid': dataset_id, \
        'protocoltype': 'NFS', 'iops': 5000, 'quotasize': tsm_quota}

startTime = ctime()
vol_creation = create_volume(vol, stdurl)
if vol_creation[0] == 'FAILED':
    #print vol_creation[1]
    logging.error('Pool life cycle test case is blocked due to: %s', \
                            vol_creation[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
else:
    endTime = ctime()
    resultCollection('%s volume creation' %vol['name'], \
            ['PASSED', ''], startTime, endTime)
    logging.debug('%s volume created successfully', vol['name'])

logging.info('Listing volumes...')
vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
if vol_list[0] == 'FAILED':
    msg = 'Failed to list volume in the tsm: "%s"' %tsm_name
    logging.error('Pool life cycle test case is blocked due to: %s', msg)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

volume_name = vol['name']
get_volInfo = get_volume_info(vol_list[1], volume_name)
if get_volInfo[0] == 'PASSED':
    volid = get_volInfo[2]
    volname = get_volInfo[1]
    vol_mntPoint = get_volInfo[3]
else:
    msg = 'Failed to get volume details'
    logging.error('Pool life cycle test case is blocked due to: %s', msg)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

#adding networ(client's network)k to nfs server 
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'FAILED':
    logging.error('Pool life cycle test case is blocked due to: %s', addClient[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

logging.info('End of creation of pool,tsm  and volume....')
resultCollectionNew('END OF CREATION OF POOL, TSM AND VOLUME....', ['', ''])

#creating directory for map NFS share to client
mnt_info = {'TSMIPAddress' : tsm_ip, 'mountPoint': vol_mntPoint,\
        'name' : volname}

logging.info('Exposing volume to client....')
startTime = ctime()
nfsMount = mountNFS(mnt_info)
if nfsMount == 'PASSED':
    logging.info('volume is mounted succesfully')
else:
    msg = 'Failed to mount the volume: "%s"' %volname
    logging.error('Pool life cycle test case is blocked due to: %s', msg)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
                    %(mnt_info['mountPoint']))
mount_point = mount_point[0].strip('\n')
#passing this to get used space
logging.info('volume is exposed to client....')
###-----------------------------------------------------------------------------------
path = pool_name+'/'+acct_name+tsm_name+'/'+volname
#this path is used in reng cmd in method get_IOPS_values_from_node

logging.info('Writing vdbench file')
VdbFile = 'filesystem_nfs'
vdbNewFile = 'filesystem_nfs'
executeCmd('yes | cp -rf vdbench/templates/%s vdbench/%s' %(VdbFile, vdbNewFile))
vol_size = '256M' #Give size in multiple of xfersize...\
        #creating 20 files and 20 threads through vdbench, 
writeFile = writingVDBfile(mnt_info, vol_size, vdbNewFile)
logging.info('executing vdbench for filling 5GB data...')
out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' %vdbNewFile)
time.sleep(2)
pidCheck = is_vdbench_alive(vdbNewFile)
print pidCheck

while True:
    mountDetails = mountPointDetails(mount_point)
    Used = mountDetails[2]
    #Used = os.popen("df -m | grep %s | awk '{print $3}' " \
     #                %(mnt_info['mountPoint'])).read()
    #Used = Used.strip()
    if int(Used) >= 5120:
        logging.debug('vdbench has created file of 5GB successfully...')
        logging.debug('size filled : %s', Used)
        logging.info('sleeping for 60 seconds for running vdbench after '\
                'creating file...')
        time.sleep(60) # let run vdbench after creating file 
        break
    else:
        pidCheck = is_vdbench_alive(vdbNewFile)
        if pidCheck:
            continue
        else:
            logging.error('Vdbench has terminated unexpectedly without '\
                    'creating initial file')
            logging.debug('The file written by vdbench is of %sM', Used)
            print 'Vdbench has terminated unexpectedly'
            break

if not pidCheck:
    endTime = ctime()
    logging.debug('Vdbench has stopped running')
    resultCollection('Vdbench has stopped running, testcase to be verified '\
        'while IOs are running are', ['BLOCKED', ''], startTime, endTime)
else:
    logging.info('Vdbench is running fine, executing further test cases...')
    ##add and remove spare/zil/log while IOs are running
    logging.info('Verifying continous provisioning and deprovisioning of '\
            'zil/cache devices while IOs are running....')
    resultCollectionNew('\nVERIFYING CONTINOUS PROVISIONING AND DEPROVISIONING'\
                ' of ZIL/CACHE DEVICES WHILE IOS ARE RUNNING....', ['', ''])
    logging.info("Read/writes before adding log device is shown below....")
    resultCollectionNew("Read/writes before adding log device is shown "\
            "below....", ['',''])
    rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
    logging.debug("%s", rw)
    
    startTime = ctime()
    group_type1 = 'log'
    add_disks1 = addDisk(final_pool_type, pool_id, 1, group_type1, \
            grp_disk, NODE1_IP)
    endTime = ctime()
    if 'FAILED' in str(add_disks1):
        print add_disks1[1]
        logging.error('%s', add_disks1[1])
        resultCollection('while IOs are running, "%s" disk Group addition' \
                %group_type1, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully added disk group "%s"' %group_type1
        logging.debug('Successfully added disk group "%s" while IOs '\
                'are running', group_type1)
        resultCollection('while IOs are running, "%s" disk Group addition' \
            %group_type1, ['PASSED', ''], startTime, endTime)

    logging.info("Read/writes after adding log device is shown below....")
    resultCollectionNew("Read/writes after adding log device is shown "\
            "below....", ['',''])
    rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
    logging.debug("%s", rw)

    time.sleep(2)
    startTime = ctime()
    del_disks1 = delDisk(group_type1, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks1:
        print del_disks1[1]
        logging.error('%s', del_disks1[1])
        resultCollection('while IOs are running, "%s" disk Group deletion' \
                %group_type1, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type1
        logging.debug('Successfully deleted the disk group "%s" while IOs are '\
                'running', group_type1)
        resultCollection('while IOs are running, "%s" disk Group deletion' \
                %group_type1, ['PASSED', ''], startTime, endTime)

    time.sleep(2)
    #pidCheck = is_vdbench_alive(vdbNewFile)
    #if pidCheck:
    #    logging.debug('Vdbench is running...')
    logging.info("Read/writes before adding cache device is shown below....")
    resultCollectionNew("Read/writes before adding cache device is shown "\
            "below....", ['',''])
    rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
    logging.debug("%s", rw)
    
    startTime = ctime()
    group_type2 = 'cache'
    add_disks2 = addDisk(final_pool_type, pool_id, 1, group_type2, \
            grp_disk, NODE1_IP)
    endTime = ctime()
    if 'FAILED' in add_disks2:
        print add_disks2[1]
        logging.error('%s', add_disks2[1])
        resultCollection('while IOs are running, "%s" disk Group addition' \
            %group_type2, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully added disk group "%s"' %group_type2
        logging.debug('Successfully added disk group "%s" while IOs '\
                'are running', group_type2)
        resultCollection('while IOs are running, "%s" disk Group addition' \
                %group_type2, ['PASSED', ''], startTime, endTime)

    logging.info("Read/writes after adding cache device is shown below....")
    resultCollectionNew("Read/writes after adding cache device is shown "\
            "below....", ['',''])
    rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
    logging.debug("%s", rw)

    time.sleep(2)
    startTime = ctime()
    del_disks2 = delDisk(group_type2, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks2:
        print del_disks2[1]
        logging.error('%s', del_disks2[1])
        resultCollection('while IOs are running, "%s" disk Group deletion' \
                %group_type2, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type2
        logging.debug('Successfully deleted the disk group "%s" while IOs are '\
                'running', group_type2)
        resultCollection('while IOs are running, "%s" disk Group deletion' \
            %group_type2, ['PASSED', ''], startTime, endTime)


    logging.info('End of verifying continous provisioning and deprovisioning '\
            'of zil/cache devices while IOs are running....')
    resultCollectionNew('END OF VERIFYING CONTINOUS PROVISIONING AND DEPROVISING'\
                ' OF ZIL/CACHE DEVICES WHILE IOS ARE RUNNING....', ['', ''])

##before killing vdbench waiting for 10s
time.sleep(10)
pidCheck = is_vdbench_alive(vdbNewFile)
if pidCheck:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_vdbench()
    time.sleep(5)
    pidCheck = is_vdbench_alive(vdbNewFile)
    if pidCheck:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_vdbench()
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

#removing previously written vdbench file...
output = getoutput('mount | grep %s | awk \'{print $3}\'' %(mnt_info['mountPoint']))
new_str = output[0].rstrip('\n')
remove_vdb_file = os.system('rm -rf %s/*' %new_str)
###--------------------------------------------------------------------------------------

##running vdbench
logging.info('Writing vdbench file')
VdbFile = 'filesystem_config'
vdbNewFile = 'filesystem_config'
executeCmd('yes | cp -rf vdbench/templates/%s vdbench/%s' %(VdbFile, vdbNewFile))
vol_size = int(floor((float(vol['quotasize'].strip('M')))*(0.85)))
vol_size = int(vol_size/20) #Give size in multiple of xfersize, \
        #creating 20 threads and 20 files in vdbench
vol_size = multiple_of_num(vol_size, 4)
vol_size = '%sM' %(vol_size)
writeFile = writingVDBfile(mnt_info, (vol_size), vdbNewFile)
logging.info('executing vdbench command')
#time.sleep(10)
logging.info('starting vdbench to fill 80% & above of pool capacity....')
out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' %vdbNewFile)
time.sleep(5)

vol_size1 = int(floor((float(vol['quotasize'].strip('M')))*(0.85)))
vol_size1 = multiple_of_num(vol_size1, 4)
logging.debug('vdbench has to create file with %sM of size', vol_size1)

while True:
    mountDetails = mountPointDetails(mount_point)
    Used = mountDetails[2]
    #Used = os.popen("df -m | grep %s | awk '{print $3}' " \
     #                    %(mnt_info['mountPoint'])).read()
    #Used = Used.strip()
    if int(Used) >= int(vol_size1) :
        logging.debug('vdbench has successfully created file above 80% of the '\
                'pool capacity...')
        logging.debug('size filled : %s', Used)
        logging.info('sleeping for 100 seconds to run vdbench for actual '\
                'IOPS after creating file of above 80% of pool capacity')
        time.sleep(100)
        break
    else:
        pidCheck = is_vdbench_alive(vdbNewFile)
        if pidCheck:
            continue
        else:
            logging.error('Vdbench has terminated unexpectedly without '\
                    'creating initial file')
            logging.debug('The file written by vdbench is of %sM', Used)
            print 'Vdbench has terminated unexpectedly'
            break

### space uses alerts------------------------------------------------------------------ 
#logging.info('checking for space uses alerts for pool and volume....')
startTime = ctime()
alert_result = check_alerts(stdurl, 2, 'space', 'Pool Capacity')
verify_alert_result(alert_result, 'Pool Capacity', startTime)
alert_result = check_alerts(stdurl, 2, 'space', 'Volume Capacity')
verify_alert_result(alert_result, 'Volume Capacity', startTime)
###-------------------------------------------------------------------------------------

###adding cache after pool is filled  above 85%...
pidCheck = is_vdbench_alive(vdbNewFile)
if not pidCheck:
    endTime = ctime()
    logging.debug('Vdbench has stopped running')
    logging.debug('Performace impact by adding vdev testacase is blocked') 
    resultCollection('Vdbench has stopped running, testcase to verify '\
    'performace impact by adding vdev is', ['BLOCKED', ''], startTime, endTime)
else:
    logging.info('Collecting read/writes 4times with interval of 1min '\
            'before adding cache....')
    resultCollectionNew('Collecting read/writes 4times with interval of 1min '\
            'before adding cache....',['',''])

    for x in range(1, 5):
        logging.info("%s. Read/writes before adding cache is shown below....", x)
        resultCollectionNew("%s. Read/writes before adding cache is shown "\
                "below...." %x, ['',''])
        rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
        logging.debug("%s", rw)
        time.sleep(60)

    startTime = ctime()
    group_type2 = 'cache'
    add_disks2 = addDisk(final_pool_type, pool_id, 1, group_type2, \
            grp_disk, NODE1_IP)
    endTime = ctime()
    if 'FAILED' in add_disks2:
        print add_disks2[1]
        logging.error('"%s" addition failed due to : %s', group_type2, add_disks2[1])
        resultCollection('while IOs are running, "%s" disk Group addition' \
            %group_type2, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully added disk group "%s"' %group_type2
        logging.debug('Successfully added disk group "%s" while IOs are '\
                'running', group_type2)
        resultCollection('while IOs are running, "%s" disk Group addition' \
                %group_type2, ['PASSED', ''], startTime, endTime)

        time.sleep(180) #sleeping for 3min after adding cache 
        logging.info('sleeping for 3 minutes so that cache is used and '\
                'then collecting read/writes....')

        logging.info('Collecting read/writes 4times with interval of 1min '\
                'after adding cache....')
        resultCollectionNew('Collecting read/writes 4times with interval of '\
                '1min after adding cache....',['',''])

        for x in range(1, 5):
            logging.info("%s. Read/writes after adding cache is shown "\
                    "below....", x)
            resultCollectionNew("%s. Read/writes after adding cache is shown "\
                    "below...." %x, ['',''])
            rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
            logging.debug("%s", rw)
            time.sleep(60)

    logging.info('Expanding pool by adding vdevs and verifying performance '\
            'impact....')
    resultCollectionNew('\nVERIFYING POOL PERFORMANCE IMPACT AFTER EXPANDING '\
            'POOL BY ADDING VDEVS....', ['', ''])

    logging.info('Collecting read/writes 4times with interval of 1min '\
            'before adding vdev....')
    resultCollectionNew('Collecting read/writes 4times with interval of 1min '\
            'before adding vdev....',['',''])

    for x in range(1, 5):
        logging.info("%s. Read/writes before adding vdev is shown below....", x)
        resultCollectionNew("%s. Read/writes before adding vdev is shown "\
                "below...." %x, ['',''])
        rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
        logging.debug("%s", rw)
        time.sleep(60)

    startTime = ctime()
    add_vdev = addDisk(final_pool_type, pool_id, final_no_of_disk, \
            final_pool_type, final_disk_type ,NODE1_IP)
    endTime = ctime()
    if 'FAILED' in add_vdev:
        print add_vdev[1]
        logging.error('%s', add_vdev[1])
        resultCollection('To expand pool capacity addition of "%s" vdev' \
            %group_type2, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully added vdev "%s" and expanded pool capacity' \
                %(final_pool_type)
        logging.debug('Successfully added vdev "%s" and expanded pool '\
                'capacity', final_pool_type)
        resultCollection('To expand pool capacity addition of "%s" vdev ' \
                %final_pool_type, ['PASSED', ''], startTime, endTime)

        logging.info('Collecting read/writes 4times with interval of 1min '\
                'after adding vdev....')
        resultCollectionNew('Collecting read/writes 4times with interval of '\
                '1min after adding vdev....',['',''])

        for x in range(1, 5):
            logging.info("%s. Read/writes after adding vdev is shown "\
                    "below....", x)
            resultCollectionNew("%s. Read/writes after adding vdev is shown "\
                    "below.... " %x, ['',''])
            rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
            logging.debug("%s", rw)
            time.sleep(60) #total 4mins

        time.sleep(60)##refresh time inteval for size to get updated is 5mins
        list_pool = listPool(stdurl)
        pools = verify_list_pool(list_pool, startTime)
        get_poolInfo =  get_pool_info(pools, pool_name)
        verify_get_pool_info(get_poolInfo, startTime)
        new_pool_size = get_poolInfo[2]
        logging.debug('Pool size before adding vdev: %s, after adding vdev: '\
                '%s', pool_size, new_pool_size)

    logging.info('End of verifying pool performance impact after expanding '\
            'pool by adding vdev....')
    resultCollectionNew('END OF VERIFYING POOL PERFORMANCE IMPACT AFTER '\
                    'EXPANDING POOL BY ADDING VDEVS....', ['',''])

    time.sleep(2)
    startTime = ctime()
    del_disks2 = delDisk(group_type2, pool_id, stdurl)
    endTime = ctime()
    if 'FAILED' in del_disks2:
        print del_disks2[1]
        logging.error('"%s" deletion failed due to : %s', group_type2, del_disks2[1])
        resultCollection('while IOs are running, "%s" disk Group deletion' \
                %group_type2, ['FAILED', ''], startTime, endTime)
    else:
        print 'Successfully deleted the disk group "%s"' %group_type2
        logging.debug('Successfully deleted the disk group "%s" while IOs are '\
                'running', group_type2)
        resultCollection('while IOs are running, "%s" disk Group deletion' \
            %group_type2, ['PASSED', ''], startTime, endTime)

        logging.info('Collecting read/writes 4times with interval of 1min '\
                'after deleting cache....')
        resultCollectionNew('Collecting read/writes 4times with interval of '\
                '1min after deleting cache....',['',''])

        for x in range(1, 5):
            logging.info("%s. Read/writes after deleting cache is shown "\
                    "below....", x)
            resultCollectionNew("%s. Read/writes after deleting cache is shown"\
                    " below...." %x, ['',''])
            rw = get_IOPS_values_from_node(path, NODE1_IP, node_passwd)
            logging.debug("%s", rw)
            time.sleep(60) #total 4mins

###replace online disk... while IOs are running
startTime = ctime()
pidCheck = is_vdbench_alive(vdbNewFile)
if not pidCheck:
    endTime = ctime()
    logging.debug('Vdbench has stopped running')
    logging.debug('Online disk replacement and resilvering testacase is blocked')
    resultCollection('Vdbench has stopped running, testcase to verify '\
        'Online disk replacement and resilvering is', ['BLOCKED', ''], \
        startTime, endTime)
else:
    logging.info('Replacing Online Disk....')
    resultCollectionNew('\nREPLACING ONLINE DISK ....',['',''])
    startTime = ctime()
    disk_replace = to_replace_disk(final_pool_type, pool_id, 1, \
            final_disk_type, NODE1_IP)
    endTime = ctime()
    if disk_replace[0] == "PASSED":
        print disk_replace[1]
        logging.debug('%s', disk_replace[1])
        resultCollection('Online Disk replacement', ['PASSED', ''], \
                startTime, endTime)
        startTime = ctime()
        while True:
            cmd = 'zpool status Poolz1 | grep "scan\|resilvering"'
            scan = getControllerInfoAppend(NODE1_IP, 'test', cmd, \
                    'logs/automation_execution.log')
            print scan
            if 'resilver in progress' in scan:
                print 'resilvering of disk is happening'
                logging.debug('resilvering of disk is happening')
                logging.info('waiting for 2mins and checking again....')
                time.sleep(120)
                continue
            else:
                endTime = ctime()
                print 'resilvering completed'
                logging.debug('resilvering completed....')
                resultCollection('Resilvering process for disk replaced', \
                        ['PASSED', ''], startTime, endTime)
                break
    else:
        print disk_replace[1]
        logging.error('Online disk replacement failed due to : %s', \
                disk_replace[1])
        resultCollection('Online Disk replacement', ['FAILED', ''], \
                startTime, endTime)

time.sleep(10) #before killing vdbench process sleeping for 10s
pidCheck = is_vdbench_alive(vdbNewFile)
if pidCheck:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    #print 'vdbench is running'
    kill_vdbench()
    time.sleep(5)
    pidCheck = is_vdbench_alive(vdbNewFile)
    if pidCheck:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_vdbench()
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped or it may be completed...')
    print 'Vdbench process has stopped or it may be completed'

time.sleep(10) #sleeping for 10s before deletion process starts

###-----------------------------------------------------------------------------------
###umount vol and del vol, tsm, acc, pool
logging.info('Deprovisiong of volume, tsm, account and  pool....')
resultCollectionNew('\nDEPROVISIONING OF VOLUME, TSM, ACCOUNT AND POOL....', \
        ['', ''])
startTime = ctime()
umount = umountVolume(mnt_info)
endTime = ctime()
if 'FAILED' in umount:
    logging.debug('Failed to umount the volume "%s"', volname)
    resultCollection('Failed to umount the volume "%s"' %volname, \
            ['FAILED', ''], startTime, endTime)
else:
    logging.debug('Successfully unmounted the volume "%s"', volname)
    resultCollection('umount of the volume "%s"' %volname, \
                        ['PASSED', ''], startTime, endTime)

startTime = ctime()
del_vol = delete_volume(volid, stdurl)
endTime = ctime()
if 'FAILED' in del_vol:
    print 'Failed to delete the volume "%s"' %(volname)
    logging.debug('Failed to delete the volume "%s"', volname)
    resultCollection('Failed to delete the volume "%s"' %(volname), \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Deleted the volume "%s"' %volname
    logging.debug('Successfully deleted the volume "%s"', volname)
    resultCollection('Deletion of volume "%s"' %volname, \
                        ['PASSED', ''], startTime, endTime)

startTime = ctime()
del_tsm = delete_tsm(tsm_id, stdurl)
endTime = ctime()
if 'FAILED' in del_tsm:
    print 'Failed to delete the tsm "%s"' %(tsm_name)
    logging.debug('Failed to delete the tsm "%s"', tsm_name)
    resultCollection('Failed to delete the tsm "%s"' %(tsm_name), \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Deleted the TSM "%s"' %tsm_name
    logging.debug('Successfully deleted the tsm "%s"', tsm_name)
    resultCollection('Deletion of Tsm "%s"' %tsm_name, \
            ['PASSED', ''], startTime, endTime)

startTime = ctime()
del_account = delete_account(acct_id, stdurl)
endTime = ctime()
if 'FAILED' in del_account:
    print 'Failed to delete the account "%s"' %(acct_name)
    logging.debug('Failed to delete the account "%s"', acct_name)
    resultCollection('Failed to delete the account "%s"' %(acct_name), \
            ['FAILED', ''], startTime, endTime)
else:
    print 'Deleted the account "%s"' %acct_name
    logging.debug('Successfully deleted the account "%s"', acct_name)
    resultCollection('Deletion of account "%s"' %acct_name, \
            ['PASSED', ''], startTime, endTime)

startTime = ctime()
del_pool = delete_pool(pool_id, stdurl)
endTime = ctime()
if 'FAILED' in del_pool:
    print 'Failed to delete the pool "%s"' %(pool_name)
    logging.debug('Failed to delete the pool "%s"', pool_name)
    resultCollection('Failed to delete the pool "%s"' %(pool_name), \
            ['FAILED', ''], startTime, endTime)
else:
     print 'Deleted the pool "%s"' %pool_name
     logging.debug('Successfully deleted the pool "%s"', pool_name)
     resultCollection('Deletion of pool "%s"' %pool_name, \
        ['PASSED', ''], startTime, endTime)

logging.info('End of deprovisiong of volume, tsm, account and  pool....')
resultCollectionNew('END OF DEPROVISIONING OF VOLUME, TSM, ACCOUNT AND POOL....', \
        ['',''])

resultCollectionNew('-------------------POOL LIFECYCLE TESTCASES ENDS'\
                '--------------------',['','\n'])
logging.info('---------------------%s---------------------', FOOTER_MSG)

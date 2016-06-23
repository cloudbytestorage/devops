import sys
import os
import time
import json
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile
from haUtils import change_node_state, ping_machine
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_node_ip 
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        getControllerInfo, executeCmd, get_apikey, executeCmdNegative, \
        getoutput, mountNFS

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------------ungracefull HA test case(NFS)'\
        'started------------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python ungraceFullHANFS.py conf.txt'
FOOTER_MSG = 'ungracefull HA test case(NFS) completed'
BLOCKED_MSG = 'Ungracefull HA test case(NFS) is blocked'

check_mendatory_arguments(sys.argv, 2, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
VSM_IP = conf['ipVSM1']
APIKEY = get_apikey(conf)
NODE1_IP = None
PASSWD = 'test' # node password
#is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
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
    logging.error('ungracefull HA test case(NFS) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def controllerIP(tsms):
    if tsms[0] == 'PASSED':
        tsm = tsms[1]
        return tsm[0].get('controlleripaddress'), tsm[0].get('controllerName')
    logging.error('ungracefull HA test case(NFS) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def get_node2_ip(NODE1_IP, stdurl):
    querycommand = 'command=listController'
    logging.debug('executing listController...')
    listController_resp = sendrequest(stdurl, querycommand)
    data = json.loads(listController_resp.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listControllerResponse'].get('errortext'))
        logging.error('ungracefull HA test case(NFS) blocked '\
                'due to %s', errormsg)
        is_blocked(startTime, FOOTER_MSG, errormsg)
    controllers = data['listControllerResponse']['controller']
    has_second_node = False
    has_first_node = False
    NODE2_IP = None
    for controller in controllers:
        if controller['ipAddress'] == NODE1_IP:
            node1_clustername = controller['clustername']
            has_first_node = True
            if has_second_node:
                if node2_clustername == node1_clustername:
                    return NODE2_IP
            continue
        node2_clustername = controller['clustername']
        NODE2_IP = controller['ipAddress']
        has_second_node = True
        if has_first_node:
            if node1_clustername == node2_clustername:
                return NODE2_IP
        if NODE2_IP is None:
            logging.error('ungracefull HA test case(NFS) blocked '\
                    'due to %s', 'There is no second Node')
            is_blocked(startTime, FOOTER_MSG, 'There is no second Node')
        return NODE2_IP


def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('ungracefull HA test case(NFS) is blocked Volume '\
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
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or accountid is None or mntpoint is None:
        logging.error('ungracefull HA test case(NFS) is blocked getting volid:'\
                '%s, accountid: %s, and mntpoint: %s', \
                volid, accountid, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, accountid, mntpoint

def verify_get_node_ip(result):
    if result[0] == 'PASSED':
        return result[1]
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_ddNFSclient(add_client_result, network, vol_name):
    if add_client_result[0] == 'PASSED':
        logging.debug('added clent <%s> to volume  %s successfully', \
                network, vol_name)
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_mountNFS(mount_result, volume_dir):
    if mount_result == 'PASSED':
        logging.debug('Volume %s mounted at mount/%s successfully', \
                volume_dir['name'], volume_dir['mountPoint'])
        return
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_umount_result(umount_result, mount_dir):
    if umount_result[0] == 'PASSED':
        logging.debug('umounted %s successfully', mount_dir)
        return
    logging.error('Not able to umount %s Error:%s', mount_dir, umount_result)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_pool_import(poolName, NODE2_IP, PASSWD):
    logging.debug('pool import at peer Node would take some time, '\
            'sleeping for 25 seconds')
    time.sleep(25)
    logging.debug('executing zpool list at Node:%s', NODE2_IP)
    getControllerInfo(NODE2_IP, PASSWD, 'zpool list', 'listpool.txt')
    import_result = executeCmd('cat listpool.txt | grep %s' %(poolName))
    if import_result[0] == 'PASSED':
        logging.debug('pool %s imported successfully at peer Node:%s', \
                poolName, NODE2_IP)
        return
    
    logging.debug('pool is not imported till 25 seconds after reboot the Node')
    logging.debug('sleeping for another 10 seconds')
    time.sleep(10)

    logging.debug('executing zpool list at Node:%s', NODE2_IP)
    getControllerInfo(NODE2_IP, PASSWD, 'zpool list', 'listpool.txt')
    import_result = executeCmd('cat listpool.txt | grep %s' %(poolName))
    if import_result[0] == 'PASSED':
        logging.debug('pool %s imported successfully at peer Node:%s', \
                poolName, NODE2_IP)
        return

    logging.debug('pool is not imported till 35 seconds after reboot the Node')
    logging.debug('sleeping for another 10 seconds')
    time.sleep(10)

    logging.debug('executing zpool list at Node:%s', NODE2_IP)
    getControllerInfo(NODE2_IP, PASSWD, 'zpool list', 'listpool.txt')
    import_result = executeCmd('cat listpool.txt | grep %s' %(poolName))
    if import_result[0] == 'PASSED':
        logging.debug('pool %s imported successfully at peer Node:%s', \
                poolName, NODE2_IP)
        return

    logging.error('pool %s import failed at peer Node:%s', poolName, NODE2_IP)
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_IOPS(NODE1_IP, PASSWD, iops_datapath):
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 2 ;\
            echo "-----------------"; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(NODE1_IP, PASSWD, cmd, 'beforeHAIO1.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    logging.debug('sleeping for 3 seconds before fatching new IOPS value...')
    time.sleep(3)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(NODE1_IP, PASSWD, cmd, 'beforeHAIO2.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    io_output = executeCmdNegative('diff beforeHAIO1.txt beforeHAIO2.txt')
    if io_output[0] == 'FAILED':
        msg = 'IOPS are not running, please make sure to run IOPS properly'
        logging.debug('Compared result: %s, Error: %s', io_output[0], msg)
        logging.debug('IOPS Error: Not going to reset the Node...')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    elif io_output[0] == 'PASSED':
        msg =  "Iops are  running fine"
        logging.debug('Compared result: %s', msg)
        print msg
        return
    else:
        print "problem in comparing files"
        logging.error('problem in comparing files')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_IOPS_afterHA(NODE2_IP, PASSWD, iops_datapath):
    endTime = ctime()
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 2 ;\
            echo "-----------------"; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(NODE2_IP, PASSWD, cmd, 'afterHAIO1.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    logging.debug('sleeping for 3 seconds before fatching new IOPS value...')
    time.sleep(3)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(NODE2_IP, PASSWD, cmd, 'afterHAIO2.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    io_output = executeCmdNegative('diff afterHAIO1.txt afterHAIO2.txt')
    if io_output[0] == 'FAILED':
        msg = 'IOPS are not running after HA failover...'
        logging.debug('Compared result: %s, Error: %s', io_output[0], msg)
        logging.debug('IOPS Error: ungracefull HA test case(NFS) failed...')
        resultCollection('Ungracefull HA test case(NFS) failed', \
                ['FAILED', ''], startTime, endTime)
    elif io_output[0] == 'PASSED':
        msg =  "IOPS are  running fine after ungracefull HA"
        logging.debug('Compared result: %s', msg)
        resultCollection('Ungracefull HA test case(NFS) passed', \
                ['PASSED', ''], startTime, endTime)
        print msg
    else:
        print "problem in comparing files"
        logging.error('problem in comparing files')
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
#logging.debug('tsms... %s', str(tsms))
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id, controllerid, accName, poolName = getTsmInfo(tsms)
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, controllerid:%s, '\
        'accName:%s, poolName:%s', tsm_name, tsm_id, dataset_id, \
        controllerid, accName, poolName)

result = get_node_ip(STDURL, controllerid)
NODE1_IP = verify_get_node_ip(result)
NODE2_IP = get_node2_ip(NODE1_IP, STDURL)
volumeDict = {'name': 'ungrceHANFS1', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'NFS', 'iops': 500}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s, and mountpoint: %s', vol_id, \
        account_id, mnt_point)
volume_dir = {'mountPoint': mnt_point, 'TSMIPAddress': VSM_IP, 'name': \
        volumeDict['name']}
add_client_result = addNFSclient(STDURL, vol_id, 'ALL')
verify_ddNFSclient(add_client_result, 'ALL', volumeDict['name'])
mount_result = mountNFS(volume_dir)
verify_mountNFS(mount_result, volume_dir)
mount_dir = 'mount/%s' %(mnt_point)
mount_dir2 = {'name': volumeDict['name'], 'mountPoint': volumeDict['name']}
logging.info('...executing vdbench....')
executeVdbenchFile(mount_dir2, filesystem_nfs)
time.sleep(20)
logging.info('verifying the IOPS before Node goes to reset...')
iops_datapath = poolName+'/'+accName+tsm_name+'/'+volumeDict['name']
verify_IOPS(NODE1_IP, PASSWD, iops_datapath)
logging.debug('going to move node to reset...')
getControllerInfo(NODE1_IP, PASSWD, 'reboot', 'reboot.txt')

logging.debug('verifying pool import at peer Node: %s', NODE2_IP)
verify_pool_import(poolName, NODE2_IP, PASSWD)
logging.debug('before verifying IOPS after reset the Node, sleeping for 10secs')
time.sleep(10)
logging.debug('verifying IOPS at peer Node IP: %s', NODE2_IP)
verify_IOPS_afterHA(NODE2_IP, PASSWD, iops_datapath)

#Wait till Node come up and move it to available state
logging.debug('Waiting for 3 minutes to come up the Node:%s, It may take 5 to '\
        '15 minutes', NODE1_IP)
time.sleep(180)
node_online = True
ping_result = ping_machine(NODE1_IP)
count = 1
while ping_result[0] == 'FAILED':
    if count == 4:
        logging.error('Node %s did not come up after 15 minutes, So can not '\
                'make it available ', NODE1_IP)
        node_online = False
        break
    logging.debug('Still Node %s did not come UP, sleeping for 3 more minutes',\
            NODE1_IP)
    time.sleep(180)
    count = count + 1
    ping_result = ping_machine(NODE1_IP)

logging.debug('ungracefull HA test case(NFS) completed, executing umount')
umount_result = executeCmd('umount %s' %(mount_dir))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete '\
            'the NFS share, since test case is complete', mount_dir)
else:
    logging.debug('NFS share %s umounted successfully', mount_dir)

remove_configuration = True
if node_online:
    #There might be few chances to Node come up, and suddenly we move it...
    #to available state, so sleep for 5 seconds
    time.sleep(5)
    available_state = change_node_state(STDURL, NODE1_IP, 'available')
    if available_state == 'FAILED':
        logging.debug('Not able to move Node to available state, Will not be '\
                'able to remove configuration')
    else:
        logging.debug('Node with IP: %s is in available state, removing '\
                'configuration', NODE1_IP)
        remove_configuration = True
else:
    logging.debug('Node did not come up can not remove configuration, please '\
            'check it manually...')

if remove_configuration:
    logging.debug('ungracefull HA test case(NFS) completed, removing '\
            'configuration')
    logging.debug('Going to delete the volume')
    delete_volume(vol_id, STDURL)
    get_logger_footer('ungracefull HA test case(NFS) completed')

import sys
import os
import time
import json
import logging
from time import ctime
from haUtils import change_node_state
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile
from volumeUtils import create_volume, delete_volume, addNFSclient, \
        listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        get_node_ip 
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        getControllerInfo, executeCmd, get_apikey, executeCmdNegative, \
        getoutput, mountNFS

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('------------------------------partial fail over test case(NFS)'\
        'started------------------------------')
startTime = ctime()
EXECUTE_SYNTAX = 'python partial_fail_over_nfs.py conf.txt'
FOOTER_MSG = 'partial fail over test case(NFS) completed'
BLOCKED_MSG = 'Partial fail over test case(NFS) is blocked'

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
    logging.error('partial fail over test case(NFS) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def controllerIP(tsms):
    if tsms[0] == 'PASSED':
        tsm = tsms[1]
        return tsm[0].get('controlleripaddress'), tsm[0].get('controllerName')
    logging.error('partial fail over test case(NFS) blocked '\
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def get_node2_ip(NODE1_IP, stdurl):
    querycommand = 'command=listController'
    logging.debug('executing listController...')
    listController_resp = sendrequest(stdurl, querycommand)
    data = json.loads(listController_resp.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listControllerResponse'].get('errortext'))
        logging.error('partial fail over test case(NFS) blocked '\
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
            logging.error('partial fail over test case(NFS) blocked '\
                    'due to %s', 'There is no second Node')
            is_blocked(startTime, FOOTER_MSG, 'There is no second Node')
        return NODE2_IP


def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('partial fail over test case(NFS) is blocked Volume '\
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
        logging.error('partial fail over test case(NFS) is blocked getting '\
                'volid: %s, accountid: %s and mntpoint: %s', volid, \
                accountid, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, accountid, mntpoint

def verify_get_node_ip(result):
    if result[0] == 'PASSED':
        return result[1]
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_IOPS(NODE1_IP, PASSWD):
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

def verify_IOPS_afterHA(NODE2_IP, PASSWD):
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
        logging.debug('IOPS Error: partial fail over test case(NFS) failed...')
        resultCollection('partial fail over test case(NFS) failed', \
                ['FAILED', ''], startTime, endTime)
    elif io_output[0] == 'PASSED':
        msg =  "IOPS are  running fine after partial fail over"
        logging.debug('Compared result: %s', msg)
        resultCollection('partial fail over test case(NFS) passed', \
                ['PASSED', ''], startTime, endTime)
        print msg
    else:
        print "problem in comparing files"
        logging.error('problem in comparing files')
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
volumeDict = {'name': 'partialNFS1', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'NFS', 'iops': 500}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s and mountpoint: %s', vol_id, \
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
logging.info('verifying the IOPS before Partial fail over...')
iops_datapath = poolName+'/'+accName+tsm_name+'/'+volumeDict['name']
verify_IOPS(NODE1_IP, PASSWD)
logging.debug('Making down the VSMs interface for partial fail over...')
interface1 = conf['interfaceVSM1']
cmd = 'ifconfig %s down' %(interface1)
logging.debug('executing <ifconfig %s down> at controller', interface1)
interface_down = getControllerInfo(NODE1_IP, PASSWD, cmd, 'interfacedown.txt')
logging.debug('sleeping for 5 seconds for pool export...')
time.sleep(5)
# have to write code for verofication of pool export
logging.debug('verifying IOPS after partial fail over...')
logging.debug('before verifying IOPS sleeping for 2 seconds...')
time.sleep(2)
logging.debug('verifying IOPS at peer Node IP: %s', NODE2_IP)
verify_IOPS_afterHA(NODE2_IP, PASSWD)
logging.debug('Making interface up for partial give back')
cmd = 'ifconfig %s up' %(interface1)
logging.debug('executing <ifconfig %s up> at controller', interface1)
interface_up = getControllerInfo(NODE1_IP, PASSWD, cmd, 'interfaceup.txt')
logging.debug('sleeping for 5 seconds for pool import...')
time.sleep(5)
# have to write code for verofication of pool export
logging.debug('sleeping for 2 seconds, after partial fail over...')
time.sleep(2)
logging.debug('verifying IOPS at peer Node IP: %s', NODE2_IP)
verify_IOPS_afterHA(NODE2_IP, PASSWD)
time.sleep(170)
logging.debug('partial fail over test case(NFS) completed, removing configuration')
umount_result = executeCmd('umount %s' %(mount_dir))
if umount_result[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete '\
            'the NFS share, since test case is complete', mount_dir)
else:
    logging.debug('NFS share %s umounted successfully', mount_dir)

logging.debug('Go and delete the volume')
delete_volume(vol_id, STDURL)
get_logger_footer('partial fail over test case(NFS) completed')

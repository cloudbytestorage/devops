import json
import requests
import md5
import subprocess
import os
import time
import logging
from time import ctime
import sys
from tsmUtils import listTSMWithIP_new, get_tsm_info
from cbrequest import executeCmd, sendrequest, queryAsyncJobResult, get_url,\
    mountNFS, umountVolume, getControllerInfo, getoutput, get_apikey,\
    executeCmdNegative, configFile, resultCollection, resultCollectionNew
from volumeUtils import create_volume, delete_volume, mount_iscsi, \
    getDiskAllocatedToISCSI, edit_qos_iops, edit_qos_compression, \
    edit_qos_readonly, listVolumeWithTSMId_new, get_volume_info, \
    edit_vol_quota
from utils import assign_iniator_gp_to_LUN, discover_iscsi_lun,\
    iscsi_login_logout, get_logger_footer, execute_mkfs, logAndresult
from haUtils import change_node_state
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench

logging.basicConfig(format = '%(asctime)s %(message)s',\
        filename = 'logs/automation_execution.log',\
        filemode = 'a', level = logging.DEBUG)

testcase = 'Edit lun attributes and save changes after HA failover and giveback'

logging.info('----Start of testcase "%s"----', testcase)

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python changeHAAvailabilityInIscsi.py conf.txt" 
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
tsm_ip = '%s' %(config['ipVSM2'])
passwd = '%s' %(config['password'])

def is_blocked():
    endTime = ctime()
    get_logger_footer('Working of LUN attributes on HA failover/HA availability'\
            'test completed')
    resultCollection('Working of LUN attributes on HA failover/HA availability'\
            'test case is', ['BLOCKED', ''], startTime, endTime)
    exit()

def verify_add_auth_gp(add_auth_group):
    if add_auth_group[0] == 'FAILED':
        logging.debug('Working of LUN attributes on HA failover/Ha availability'\
                'test case is blocked '\
                'Not able to assign auth group to iSCSI LUN')
        is_blocked()

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('Working of LUN attributes on HA failover/Ha availability'\
            'case is blocked '\
            'getting iqn is None')
    is_blocked()

def verify_iscsi_login(result, vol_name):
    if result[0] == 'PASSED':
        logging.debug('login successfully for iSCSI LUN %s', vol_name)
        return
    if 'already exists' in str(result[1]):
        logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
                'get the iscsi device name', vol_name)
        return
    logging.error('Working of LUN attributes on HA failover/Ha availability'\
            'is blocked Not able to login %s, Error: %s', vol_name, str(result[1]))
    is_blocked()
   
def verify_getDiskAllocatedToISCSI(result, mountpoint):
    if result[0] == 'PASSED' and mountpoint in str(result[1]):
        logging.debug('iscsi logged device... %s', result[1][mountpoint])
        return result[1][mountpoint]
    logging.error('Not able to get iscsi legged device')
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

##-----------------------------------------------------------------------
startTime = ctime()
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsm_ip)
tsm_list = listTSMWithIP_new(stdurl, tsm_ip)
if 'PASSED' in tsm_list:
    logging.info('TSM present with the given IP "%s"', tsm_ip)
else:
    endTime = ctime()
    print tsm_list[1]
    logAndresult(testcase, 'BLOCKED', tsm_list[1], startTime, endTime)

get_tsmInfo = get_tsm_info(tsm_list[1])
tsm_id = get_tsmInfo[0]
tsm_name = get_tsmInfo[1]
dataset_id = get_tsmInfo[2]
accName = tsm_list[1][0].get('accountname')
accId = tsm_list[1][0].get('accountid')
poolName = tsm_list[1][0].get('hapoolname')
poolId = tsm_list[1][0].get('poolid')
node_ip = tsm_list[1][0].get('controlleripaddress')
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
            tsm_name, tsm_id, dataset_id)
logging.debug('pool_name: %s, pool_id: %s, account_name: %s, account_id: %s, '\
        'node_ip: %s', poolName, poolId, accName, accId, node_ip)

volume = {'name': 'iscsiHA', 'tsmid': tsm_id, 'datasetid': dataset_id,\
        'protocoltype': 'ISCSI','iops':50}
create_vol = create_volume(volume, stdurl)
if 'FAILED' in create_vol:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', create_vol[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(volume['name'])

logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
if 'PASSED' in vol_list:
    logging.info('Volumes present in the TSM "%s"', tsm_name)
else:
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
            %(tsm_name) + vol_list[1]
    logAndresult(testcase, 'BLOCKED', vol_list[1], startTime, endTime)

volume_name = volume['name']
get_volInfo = get_volume_info(vol_list[1], volume_name)
volname, volid, vol_iqn, group_id = get_volInfo[1], get_volInfo[2], \
                get_volInfo[4], get_volInfo[5]
logging.debug('volname: %s, volid: %s, vol_iqn: %s, vol_grpID: %s',\
    volname, volid, vol_iqn, group_id)

result = assign_iniator_gp_to_LUN(stdurl, volid, accId, 'ALL')
verify_add_auth_gp(result)
logging.debug('getting iqn for volume %s', volname)
iqn = discover_iscsi_lun(tsm_ip, vol_iqn)
iqn = verify_iqn(iqn)
logging.debug('iqn for discovered iSCSI LUN... %s', iqn)
login_result = iscsi_login_logout(iqn, tsm_ip, 'login')
verify_iscsi_login(login_result, volname)
time.sleep(5)
mountpoint = accName + volname 
result = getDiskAllocatedToISCSI(tsm_ip, mountpoint)
device = verify_getDiskAllocatedToISCSI(result, mountpoint)
mkfs_result = execute_mkfs(device, 'ext3')
verify_execute_mkfs(mkfs_result)
mount_result = mount_iscsi(device, volname)
verify_mount(mount_result)
mount_dir = {'name':volname, 'mountPoint':volname}

#run vdbench
logging.info('Running vdbench  by using file')
exe = executeVdbenchFile(mount_dir, 'filesystem_iscsi')
check_vdbench = is_vdbench_alive(volname)
logging.info('Waiting for 30s before changing node state')
time.sleep(30)

check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    #changing state of node to maintance....
    logging.info('Performing HA Failover....')
    node_maint = change_node_state(stdurl, node_ip, 'maintenance')
    if node_maint[0] == 'PASSED':
        print 'Node with IP: "%s" moved to maintenance successfully' %node_ip
    else:
        msg = 'Node with IP:"%s" failed to move it to maintenance mode' %node_ip
        endTime = ctime()
        logAndresult(testcase, 'BLOCKED', node_maint[1], startTime, endTime)
    
    time.sleep(5)
    logging.info('Checking whether vdbench is still running or not after '\
            'node is moved to maintanence mode....') 
    if not check_vdbench:
        msg = 'Vdbench has stopped running after node is changed to '\
                'maintanence mode'
        print msg
        logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
    logging.debug('Vdbench is still running after node state change....')

    resultCollectionNew('Verifying lun attributes modification after '\
            'HA failover....', ['', ''])
    logging.info('Verifying lun attributes modification after HA failover....')
    
    logging.info('Editing IOPS....')
    startTime = ctime()
    edit_iops = edit_qos_iops(group_id, 300, stdurl)
    if edit_iops[0] == 'FAILED':
         endTime = ctime()
         logging.debug('Expected Result: Failed to update iops due to HA failover')
         resultCollection('IOPS update unsuccessful during HA failover', \
                ['PASSED', ''], startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Unexpected Result: Successfully updated iops during HA failover'
        print msg
        logging.debug('%s', msg)
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                startTime, endTime)

    logging.info('Editing Quota....')    
    startTime = ctime()
    edit_quota = edit_vol_quota(volid, '12G', stdurl)
    if edit_quota[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Expected Result: Failed to update quota due to HA failover')
        resultCollection('Quota update unsuccessful during HA failover', \
                    ['PASSED', ''], startTime, endTime)

    else:
        endTime = ctime()
        msg = 'Unexpected Result: Successfully updated iops during HA failover'
        print msg
        logging.debug('%s', msg)
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
            startTime, endTime)

    logging.info('Modifying Compression state....')
    startTime = ctime()
    modify_comp = edit_qos_compression(stdurl, volid, 'on')
    if modify_comp[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Expected Result: Failed to update compression due to '\
                'HA failover')
        resultCollection('Compression update unsuccessful during HA failover', \
                ['PASSED', ''], startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Unexpected Result: Successfully updated compression during '\
                'HA failover'
        print msg
        logging.debug('%s', msg)
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                startTime, endTime)

else:
    endTime = ctime()
    msg = 'Vdbench has stopped running'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)


check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    ##Moving node to available
    logging.info('Performing HA Giveback....')
    node_avail = change_node_state(stdurl, node_ip, 'available')
    if node_avail[0] == 'PASSED':
        print 'Node with IP:"%s"  moved to available mode' %node_ip
    else:
        msg = 'Node with IP:"%s" failed to move it to available mode' %node_ip
        endTime = ctime()
        logAndresult(testcase, 'BLOCKED', node_maint[1], startTime, endTime)
    time.sleep(5)
    logging.info('Checking whether vdbench is still running or not after '\
                'node is moved to available mode....')
    if not check_vdbench:
        msg = 'Vdbench has stopped running after node is changed to '\
                    'available mode'
        print msg
        logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
    
    logging.debug('Vdbench is still running after node state change....')

    resultCollectionNew('Verifying lun attributes modification after '\
            'HA Giveback....', ['', ''])
    logging.info('Verifying lun attributes modification after HA giveback....')

    logging.info('Editing IOPS....')
    startTime = ctime()
    edit_iops = edit_qos_iops(group_id, 500, stdurl)
    if edit_iops[0] == 'FAILED':
         endTime = ctime()
         logging.debug('Failed to update iops after HA giveback')
         resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                    startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated iops after HA giveback'
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated IOPS after HA giveback', \
                ['PASSED',''], startTime, endTime)
    
    logging.info('Modifying Compression state....')
    startTime = ctime()
    modify_comp = edit_qos_compression(stdurl, volid, 'on')
    if modify_comp[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to modify compression state after HA giveback')
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                        startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated compression state after HA giveback'
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated compression state after HA '\
                'giveback', ['PASSED', ''], startTime, endTime)
else:
    endTime = ctime()
    msg = 'Vdbench has stopped running'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
                startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_vdbench()
    time.sleep(2)
    check_vdbench = is_vdbench_alive(volname)
    if check_vdbench:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_vdbench()
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

logging.debug('unmounting the volume %s', (volname))
Umount = executeCmd('umount /dev/%s1' %device)
if Umount[0] == 'PASSED':
    logging.info('Successfully Unmounted ISCSI lun "dev/%s1"', device)
else:
    msg = 'Unmount failed for lun "/dev/%s1"' %device
    print msg
    logging.error('%s', msg)

logging.info('logging out from iscsi session')
logout_result = iscsi_login_logout(iqn, tsm_ip, 'logout')
if logout_result[0] == 'PASSED':
    logging.debug('logout successfully for iSCSI LUN %s', volname)
else:
    logging.debug('%s', logout_result[1])
    print logout_result[1]

set_auth_group = assign_iniator_gp_to_LUN(stdurl, volid, accId, 'None')
if set_auth_group[0] == 'FAILED':
    logging.error('Not able to set auth group to None, not deleting volume')
    exit()
else:
    logging.debug('Initiator group is set to "none"')

logging.info('Deleting volume "%s"', volname)
deleteVolume = delete_volume(volid, stdurl)
if deleteVolume[0] == 'PASSED':
    print 'Volume \"%s\" Deleted successfully' %(volname)
    logging.debug('Volume \"%s\" Deleted successfully', volname)
else:
    print 'Failed to deleted the volume \"%s\"' %(volname)
    logging.debug('Failed to deleted the volume \"%s\"', volname)

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)


        

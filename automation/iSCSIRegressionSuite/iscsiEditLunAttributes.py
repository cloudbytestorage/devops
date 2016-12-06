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
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench
from cbrequest import executeCmd, sendrequest, queryAsyncJobResult, get_url,\
    mountNFS, umountVolume, getControllerInfo, getoutput, get_apikey,\
    executeCmdNegative, configFile, resultCollection, resultCollectionNew
from volumeUtils import create_volume, delete_volume, edit_qos_readonly, \
    edit_qos_compression, edit_qos_syncronization, mount_iscsi, \
    getDiskAllocatedToISCSI, listVolumeWithTSMId_new, get_volume_info, \
    edit_vol_quota, edit_qos_grace, edit_qos_iops
from utils import assign_iniator_gp_to_LUN, discover_iscsi_lun,\
    iscsi_login_logout, get_logger_footer, execute_mkfs, logAndresult

logging.basicConfig(format = '%(asctime)s %(message)s',\
        filename = 'logs/automation_execution.log',\
        filemode = 'a', level = logging.DEBUG)

testcase = "Modify the lun Attributes and verify if I/o interrupts"

logging.info('----Start of testcase "%s"----', testcase)

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

lun_attri = {'iops': 200, 'quota': '20G', 'compression': 'on', \
        'sync': 'standard', 'readonly': 'true', 'grace': 'true'}

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
tsm_ip = '%s' %(config['ipVSM2'])
passwd = '%s' %(config['password'])

def is_blocked():
    endTime = ctime()
    get_logger_footer('Modifying QOS attributes on iSCSI volume, test completed')
    resultCollection('Modifying QOS functionality on iSCSI LUN, test case is',\
            ['BLOCKED', ''], startTime, endTime)
    exit()

def verify_add_auth_gp(add_auth_group):
    if add_auth_group[0] == 'FAILED':
        logging.debug('Modifying QOS functionality on iSCSI LUN \
                test case is blocked '\
                'Not able to assign auth group to iSCSI LUN')
        is_blocked()

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('Modifying QOS functionality on iSCSI LUN test' \
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
    logging.error('Modifying QOS functionality on iSCSI LUN test case \
            is blocked Not able to login %s, Error: %s', vol_name, str(result[1]))
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

def verify_vdbench_during_prop_edit(volname):
    logging.info('Sleeping for 10s....')
    time.sleep(10) #waiting 10s before editing other properties
    logging.info('Checking whether vdbench is still running or not....')
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing lun attributes'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)

def getting_qos_data_from_node(node_ip, passwd, datapath, outFile):
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 2 ;\
        echo "-----------------"; reng stats access dataset %s qos |\
        head -n 4' %(datapath, datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(node_ip, passwd, cmd, outFile)
    logging.debug('iops result is %s', (iops_res))
    return iops_res

def file_compare(firstFile, secondFile, prptName):
    logging.info('Comparing QOS result files...')
    qos_output = executeCmdNegative('diff %s %s' %(firstFile, secondFile))
    logging.debug('compared result is %s', (qos_output))
    if qos_output[0] == 'FAILED':
        msg = 'Qos values are same after updating "%s"' %prptName
        endTime = ctime()
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    elif qos_output[0] == 'PASSED':
        msg = 'Qos values are different after updating "%s"' %prptName
        logging.debug('%s', msg)
    else:
        logging.error('Failed to compare files having qos values')
        print "problem in comparing files"

#------------------------------------------------------------------------------
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


##creating volume
volume = {'name': 'iscsiPropEdit', 'tsmid': tsm_id, 'datasetid': dataset_id,\
        'protocoltype': 'ISCSI','iops':100}
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
            %(tsm_name) + volList[1]
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = volume['name']
get_volInfo = get_volume_info(vol_list[1], volume_name)
volname, volid, vol_iqn, group_id = get_volInfo[1], get_volInfo[2], \
                get_volInfo[4], get_volInfo[5]
logging.debug('volname: %s, volid: %s, vol_iqn: %s, vol_grpID: %s',\
    volname, volid, vol_iqn, group_id)

vl = vol_list[1][0]
old_attri = {'iops': vl.get('iops'), 'quota':vl.get('quota'), \
        'compression': vl.get('compression'), 'sync': vl.get('sync'), \
        'readonly': vl.get('readonly'), 'grace': vl.get('graceallowed')}

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

qos_datapath = poolName+'/'+accName+tsm_name+'/'+volname

logging.info('Running vdbench  by using file')
exe = executeVdbenchFile(mount_dir, 'filesystem_iscsi')
time.sleep(5)
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('vdbench is running')
    logging.info('Editing LUN attributes while IOs are running....')
    #-------------------------IOPS------------------------------------
    logging.info('Editing IOPS....')
    startTime = ctime()
    edit_iops = edit_qos_iops(group_id, lun_attri['iops'], stdurl)
    if edit_iops[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to update iops while IOs are running due to: %s',\
            edit_iops[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                    startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated iops of volume "%s" from %s to %s' \
            'while IOs are running' %(volname, old_attri['iops'], \
            lun_attri['iops'])
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated IOPS while IOs are running', \
            ['PASSED', ''], startTime, endTime)
    
    logging.info('Getting qos details from controller after '\
                        'updating IOPS....')
    after_iops_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterIOPSupdate1.txt' )
    logging.debug('Qos details after Updating IOPS is shown below:')
    logging.debug('%s', after_iops_upd)
    logging.info('waiting for 5s and again taking Qos details....')
    time.sleep(5)
    after_iops_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterIOPSupdate2.txt' )
    logging.debug('Qos details after Updating IOPS is shown below:')
    logging.debug('%s', after_iops_upd)

    file_compare('logs/afterIOPSupdate1.txt','logs/afterIOPSupdate2.txt','iops')

    verify_vdbench_during_prop_edit(volname)
    
    os.system('rm -rf logs/afterIOPSupdate1.txt logs/afterIOPSupdate2.txt')

    #-----------------COMPRESSION---------------------------------- 
    logging.info('Modifying Compression state....')
    startTime = ctime()
    modify_comp = edit_qos_compression(stdurl, volid, lun_attri['compression'])
    if modify_comp[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to modify compression state while IOs are '\
                'running due to: %s', modify_comp[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                        startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated compression state for volume "%s" from '\
                '%s to %s while IOs are running' %(volname, \
                old_attri['compression'], lun_attri['compression'])
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated compression state while IOs '\
                'are running', ['PASSED', ''], startTime, endTime)
    
    logging.info('Getting qos details from controller after '\
                        'updating Compression....')
    after_cmp_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterCOMPupdate1.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_cmp_upd)
    logging.info('waiting for 5s and again taking Qos details....')
    time.sleep(5)
    after_cmp_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterCOMPupdate2.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_cmp_upd)

    file_compare('logs/afterCOMPupdate1.txt',\
            'logs/afterCOMPupdate2.txt','compression')

    verify_vdbench_during_prop_edit(volname)

    os.system('rm -rf logs/afterCOMPupdate1.txt logs/afterCOMPupdate2.txt')
    #-----------------------SYNC----------------------------------
    logging.info('Modifying Syncronization state....')
    startTime = ctime()
    modify_sync = edit_qos_syncronization(stdurl, volid, lun_attri['sync'])
    if modify_sync[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to modify syncronization state while IOs are '\
                'running due to: %s', modify_sync[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                        startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated syncronization state of volume "%s" from '\
                '%s to %s while IOs are running' %(volname, \
                old_attri['sync'], lun_attri['sync'])
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated Syncronization state while IOs '\
                'are running', ['PASSED', ''], startTime, endTime)
    
    logging.info('Getting qos details from controller after '\
                        'updating Grace....')
    after_sync_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterGRACEupdate1.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_sync_upd)
    logging.info('waiting for 5s and again taking Qos details....')
    time.sleep(5)
    after_sync_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterGRACEupdate2.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_sync_upd)

    file_compare('logs/afterSYNCupdate1.txt',\
            'logs/afterSYNCupdate2.txt','syncronization')

    verify_vdbench_during_prop_edit(volname)

    os.system('rm -rf logs/afterSYNCupdate1.txt logs/afterSYNCupdate2.txt')
    
    #--------------------------GRACE-------------------------------
    logging.info('Modifying Grace state....')
    startTime = ctime()
    modify_grace = edit_qos_grace(group_id, lun_attri['grace'], stdurl)
    if modify_grace[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to modify Grace state while IOs are '\
                'running due to: %s', modify_grace[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                        startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated Grace state of volume "%s" from '\
                '%s to %s while IOs are running' %(volname, \
                old_attri['readonly'], lun_attri['readonly'])
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated Grace state while IOs '\
                'are running', ['PASSED', ''], startTime, endTime)
    
    logging.info('Getting qos details from controller after '\
                        'updating Grace....')
    after_grace_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterGRACEupdate1.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_grace_upd)
    logging.info('waiting for 5s and again taking Qos details....')
    time.sleep(5)
    after_grace_upd = getting_qos_data_from_node(node_ip, passwd, \
                qos_datapath, 'logs/afterGRACEupdate2.txt' )
    logging.debug('Qos details after Updating Grace is shown below:')
    logging.debug('%s', after_grace_upd)

    file_compare('logs/afterGRACEupdate1.txt',\
            'logs/afterGRACEupdate2.txt','grace')

    verify_vdbench_during_prop_edit(volname)

    os.system('rm -rf logs/afterGRACEupdate1.txt logs/afterGRACEupdate2.txt')
 
else:
    endTime = ctime()
    msg = 'Vdbench has stopped running'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

logging.info('Case2: When readonly is enabled vdbench should stop running...')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('Modifying Readonly state....')
    startTime = ctime()
    modify_ro = edit_qos_readonly(stdurl, volid, lun_attri['readonly'])
    if modify_ro[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to modify readonly state while IOs are '\
                'running due to: %s', modify_ro[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                        startTime, endTime)
    else:
        endTime = ctime()
        msg = 'Successfully updated Readonly state of volume "%s" from '\
                '%s to %s while IOs are running' %(volname, \
                old_attri['readonly'], lun_attri['readonly'])
        print msg
        logging.debug('%s', msg)
        resultCollection('Successfully updated Readonly state while IOs '\
                'are running', ['PASSED', ''], startTime, endTime)
    
    time.sleep(8)
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        msg = 'Expected result: Vdbench has stopped running '\
                'after enabling readonly'
        logging.debug('%s', msg)
    else:
        endTime = ctime()
        msg = 'Unexpected result: Vdbench has not stopped running '\
        'after enabling readonly'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
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
Umount = executeCmd('umount  /dev/%s1' %device)
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


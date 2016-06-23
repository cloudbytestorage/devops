import json
import requests
import md5
import subprocess
import os
import time
import logging
from time import ctime
import sys
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile
from cbrequest import executeCmd, sendrequest, queryAsyncJobResult, get_url,\
        mountNFS, umountVolume, getControllerInfo, getoutput, get_apikey, \
        executeCmdNegative, configFile, resultCollection
from volumeUtils import create_volume, delete_volume, mount_iscsi, edit_qos_tp,\
        getDiskAllocatedToISCSI, listVolumeWithTSMId_new, edit_qos_iops
from utils import assign_iniator_gp_to_LUN, discover_iscsi_lun, iscsi_login_logout,\
                get_logger_footer, execute_mkfs

logging.basicConfig(format = '%(asctime)s %(message)s',\
        filename = 'logs/automation_execution.log',\
        filemode = 'a', level = logging.DEBUG)
logging.info('---Start of script "Edit QoS properties while running'\
        'IOPS and verify QoS values using ISCSI"---')
IopsEnable_Flag =  TpEnable_flag = 0
if len(sys.argv) == 4:
    if  sys.argv[2].lower() == "%s" %("iopsenable"):
        IopsEnable_Flag = 1
        iops_value = sys.argv[3]
    elif sys.argv[2].lower() == "%s" %("iopsdisable"):
        TpEnable_flag = 1
        throughput_value = sys.argv[3]
    else:
        print 'Arguments are not correct,please provide the corrrect'\
                'arguments as below\n'
        print 'python updIscsiQos.py conf.txt IopsEnable/IopsDisable'\
                'Iopsvalue/Throughputvalue'
        print 'If you give IopsEnabled give the Iops value or else'\
                'throughput value'
        exit()
else:
    print 'Arguments are not correct,please provide the corrrect'\
            'arguments as below\n'
    print 'python updIscsiQos.py conf.txt IopsEnable/IopsDisable'\
            'Iopsvalue/Throughputvalue'
    print "If you give IopsEnabled give the Iops value or else throughput value"
    exit()

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
tsm_ip = '%s' %(config['ipVSM1'])
passwd = '%s' %(config['password'])

def is_blocked():
    endTime = ctime()
    get_logger_footer('Modifying QOS on iSCSI test completed')
    resultCollection('Modifying QOS functionality on iSCSI LUN test case is',\
            ['BLOCKED', ''], startTime, endTime)
    exit()

def verify_add_auth_gp(add_auth_group):
    if add_auth_group[0] == 'FAILED':
        logging.debug('Modifying QOS functionality on iSCSI LUN' \
                'test case is blocked Not able to assign auth group to iSCSI LUN')
        is_blocked()

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('Modifying QOS functionality on iSCSI LUN test' \
            'case is blocked getting iqn is None')
    is_blocked()

def verify_iscsi_login(result, vol_name):
    if result[0] == 'PASSED':
        logging.debug('login successfully for iSCSI LUN %s', vol_name)
        return
    if 'already exists' in str(result[1]):
        logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
                'get the iscsi device name', vol_name)
        return
    logging.error('Modifying QOS functionality on iSCSI LUN test case' \
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

startTime = ctime()
##listing Accounts to get Accname
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
data = json.loads(resp_listAccount.text)
AccountList = data['listAccountResponse']
if 'errorcode' in str(AccountList):
    errormsg = str(data['listAccountResponse']['errortext'])
    print errormsg
    endTime = ctime()
    resultCollection('Listing of Account failed',['BLOCKED',''], startTime, endTime)
    exit()
try:
    accounts = data["listAccountResponse"]["account"]
    if data["listAccountResponse"]["count"] > 0:
        accId =  data["listAccountResponse"]["account"][0]["id"]
        accName =  data["listAccountResponse"]["account"][0]["name"]
        
except:
    print 'Accounts not present...Create Account'
    exit()
##listing pool to get poolname
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl, querycommand)
data = json.loads(resp_listHAPool.text)
PoolList = data['listHAPoolResponse']
if 'errorcode' in str(PoolList):
    errormsg = str(data['listHAPoolResponse']['errortext'])
    print errormsg
    endTime = ctime()
    resultCollection('Listing of Pool failed',['BLOCKED',''], startTime, endTime)
    exit()
elif data["listHAPoolResponse"]["count"] > 0:
    poolId = data["listHAPoolResponse"]["hapool"][0]["id"]
    poolName = data["listHAPoolResponse"]["hapool"][0]["name"]
else:
    print 'Pool Not present..create Pool'
    exit()
### Listing Tsm to get id and dataset id
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsm_ip)
tsm_list = listTSMWithIP_new(stdurl, tsm_ip)
if 'PASSED' in tsm_list:
    logging.info('TSM present with the given IP "%s"', tsm_ip)
    pass
elif 'BLOCKED' in tsm_list:
    errormsg = 'There is no TSM with IP "%s"' %(tsm_ip)
    print errormsg
    logging.warning('TSM with IP "%s" not present, Create TSM', tsm_ip)
    logging.debug('-------Ending script because no TSM present-------')
    endTime = ctime()
    resultCollection('Listing of Tsm failed',['BLOCKED', ''], startTime, endTime)
    exit()
else:
    errormsg =  'Not able to list TSMs due to: ' + tsm_list[1]
    logging.debug('%s', tsm_list[1])
    logging.debug('-------Ending script because Failed to list TSM-------')
    endTime =ctime()
    resultCollection('Listing of Tsm failed',['BOLCKED',''], startTime, endTime)
    exit()
tsm_id = tsm_list[1][0].get('id')
tsm_name = tsm_list[1][0].get('name')
dataset_id = tsm_list[1][0].get('datasetid')
vsmAccName = tsm_list[1][0].get('accountname')
node_ip = tsm_list[1][0].get('controlleripaddress')
logging.info('Got TSM ID and Dataset ID "%s"  "%s" of "%s"', tsm_id, dataset_id, tsm_name)

if IopsEnable_Flag == 1:
    logging.info('Creating dictionary for creating volume')
    volume1 = {'name': 'IscsiIopsVol1', 'tsmid': tsm_id, 'datasetid': dataset_id,\
            'protocoltype': 'ISCSI', 'iopscontrol':'true', 'tpcontrol':'false','iops':1000}
    logging.info('Dictionary created')
    logging.debug('%s', volume1)
    logging.info('creating volume "%s"', volume1['name'])
    create_vol = create_volume(volume1, stdurl)
    print create_vol[0]
    logging.debug('%s', create_vol)
    if 'FAILED' in create_vol:
        errormsg = 'Not able to create vol due to:' + create_vol[1]
        print errormsg
        logging.debug('%s', create_vol[1])
        logging.debug('-------Ending script because Failed to create volume------')
        endTime = ctime()
        resultCollection('creation of volume failed',['BLOCKED',''], startTime, endTime)
        exit()
    logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
    vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
    if 'PASSED' in vol_list:
        logging.info('Volumes present in the TSM "%s"', tsm_name)
        pass
    else:
        errormsg = 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + vol_list[1]
        print errormsg
        logging.debug('%s', vol_list[1])
        logging.debug('-------Ending script because Failed to list volume-----')
        endTime = ctime()
        resultCollection('Listing of volume Blocked the testcase', \
                ['BLOCKED',''], startTime, endTime)
        exit()
    for vol in vol_list[1]:
        if vol['name'] == volume1['name']:
            iops_volid = vol.get('id')
            iops_volname = vol.get('name')
            iopsgroup_id = vol.get('groupid')
            iops_vol_iqn = vol.get('iqnname')
    logging.info('Got IopsVolume ID = "%s" and Group ID = "%s" of "%s"', \
            iops_volid, iopsgroup_id, iops_volname)
    result = assign_iniator_gp_to_LUN(stdurl, iops_volid, accId, 'ALL')
    verify_add_auth_gp(result)
    logging.debug('getting iqn for volume %s', iops_volname)
    iqn = discover_iscsi_lun(tsm_ip, iops_vol_iqn)
    iqn = verify_iqn(iqn)
    logging.debug('iqn for discovered iSCSI LUN... %s', iqn)
    login_result = iscsi_login_logout(iqn, tsm_ip, 'login')
    verify_iscsi_login(login_result, iops_volname)
    time.sleep(5)
    mountpoint = accName + iops_volname
    result = getDiskAllocatedToISCSI(tsm_ip, mountpoint)
    device = verify_getDiskAllocatedToISCSI(result, mountpoint)
    mkfs_result = execute_mkfs(device, 'ext3')
    verify_execute_mkfs(mkfs_result)
    mount_result = mount_iscsi(device, iops_volname)
    verify_mount(mount_result)
    ##executing vd bench
    mount_dir = {'name':iops_volname, 'mountPoint':iops_volname}
    logging.info('...executing vdbench....')
    executeVdbenchFile(mount_dir, 'filesystem_iscsi')
    time.sleep(14)
    logging.info('verifying the Iops in volume')
    iops_datapath = poolName+'/'+accName+tsm_name+'/'+iops_volname
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------"; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(node_ip, passwd, cmd, 'iopsoutput.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    res = edit_qos_iops(iopsgroup_id, iops_value, stdurl)
    if res[0] == 'PASSED':
        logging.debug('IOPs value is updated')
        endTime = ctime()
        resultCollection('updating QOS property is Passed in ISCSI',\
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('IOPs value is not updated')
        endTime = ctime()
        resultCollection('updating QOS property is failed in ISCSI',\
                ['FAILED',''], startTime, endTime)
    logging.info('verifying the Iops in volume again ')
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res2 = getControllerInfo(node_ip, passwd, cmd, 'updiopsoutput.txt')
    print iops_res2
    logging.debug('iops result is %s', (iops_res))
    logging.info('comparing the both iops result')
    io_output = executeCmdNegative('diff iopsoutput.txt updiopsoutput.txt')
    logging.debug('compared result is %s', (io_output))
    if io_output[0] == 'FAILED':
        msg =  "Iops are not running correct"
        logging.debug('Compared result: %s', msg)
        endTime = ctime()
        resultCollection('Iops value are same after updating the value in ISCSI', \
                ['FAILED',''], startTime, endTime)
        print msg
    elif io_output[0] == 'PASSED':
        msg =  "Iops are  running correct"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Iops value are different after updating the value in ISCSI', \
                ['PASSED',''], startTime, endTime)
    else:
        print "problem in comparing files"
    
    time.sleep(130)
    logging.info('Executing Vdbench stopped')
    logging.info('logging out from iscsi session')
    login_result = iscsi_login_logout(iqn, tsm_ip, 'logout')
    logging.debug('unmounting the volume %s', (iops_volname))
    nfsUmount1 = umountVolume(mount_dir)
    logging.debug('unmounting volume result is %s', (nfsUmount1))
    if nfsUmount1 == 'PASSED':
        logging.info('Deleting the created volume')
        del_vol = delete_volume(iops_volid, stdurl)
        print del_vol
        logging.debug('deleteing volume result is %s', (del_vol))
    else:
        errormsg = "Problem in unmounting volume"
        endTime = ctime()
        resultCollection('umounting volume failed',['BLOCKED',''], startTime, endTime)

    logging.info('---End of script "Edit QoS properties while '\
            'running IOPS and verify QoS values"---')

if TpEnable_flag ==1:
    logging.info('Creating dictionary for creating volume with throughput enabled')
    volume2 = {'name': 'IscsiTpVol', 'tsmid': tsm_id, 'datasetid': dataset_id,\
            'protocoltype': 'ISCSI', 'iopscontrol':'false', 'tpcontrol':'true',\
            'iops': 0, 'throughput':1000}
    logging.info('Dictionary created')
    logging.debug('%s', volume2)
    logging.info('creating volume "%s"', volume2['name'])
    create_vol2 = create_volume(volume2, stdurl)
    print create_vol2
    logging.debug('%s', create_vol2)
    if 'FAILED' in create_vol2:
        print 'Not able to create vol due to:' + create_vol2[1]
        logging.debug('%s', create_vol2[1])
        logging.debug('-------Ending script because Failed to create volume------')
        endTime =ctime()
        resultCollection('creation of volume failed',['BLOCKED',''],\
                startTime, endTime)
        exit()
    logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
    vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
    if 'PASSED' in vol_list:
        logging.info('Volumes present in the TSM "%s"', tsm_name)
        pass
    else:
        print 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + vol_list[1]
        logging.debug('%s', vol_list[1])
        logging.debug('-------Ending script because Failed to list volume-----')
        endTime = ctime()
        resultCollection('Listing of volume failed',['BLOCKED',''],\
                startTime, endTime)
        exit()
    for vol in vol_list[1]:
        if vol['name'] == volume1['name']:
            tp_volid = vol.get('id')
            tp_volname = vol.get('name')
            tpgroup_id = vol.get('groupid')
            tp_vol_iqn = vol.get('iqnname')
    logging.info('Got TpVolume ID = "%s" and Group ID = "%s" of "%s"',\
            tp_volid, tpgroup_id, tp_volname)
    ###########
    result = assign_iniator_gp_to_LUN(stdurl, tp_volid, accId, 'ALL')
    verify_add_auth_gp(result)
    logging.debug('getting iqn for volume %s', tp_volname)
    iqn = discover_iscsi_lun(tsm_ip, tp_vol_iqn)
    iqn = verify_iqn(iqn)
    logging.debug('iqn for discovered iSCSI LUN... %s', iqn)
    login_result = iscsi_login_logout(iqn, tsm_ip, 'login')
    verify_iscsi_login(login_result, tp_volname)
    time.sleep(9)
    mountpoint = accName + tp_volname
    result = getDiskAllocatedToISCSI(tsm_ip, mountpoint)
    device = verify_getDiskAllocatedToISCSI(result, mountpoint)
    mkfs_result = execute_mkfs(device, 'ext3')
    verify_execute_mkfs(mkfs_result)
    mount_result = mount_iscsi(device, tp_volname)
    verify_mount(mount_result)
    ##executing vd bench
    mount_dir = {'name':tp_volname, 'mountPoint':tp_volname}
    logging.info('...executing vdbench....')
    executeVdbenchFile(mount_dir, 'filesystem_iscsi')
    time.sleep(15)
    logging.info('verifying the Throughput in volume')
    tp_datapath =  poolName+'/'+accName+tsm_name+'/'+tp_volname
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(tp_datapath, tp_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    tp_res = getControllerInfo(node_ip, passwd, cmd, 'tpoutput.txt')
    print tp_res
    logging.debug('Throughput result is %s', (tp_res))
    res = edit_qos_tp(tpgroup_id, throughput_value, stdurl)
    if res[0] == 'PASSED':
        logging.debug('Throuhput value is updated while iops is running')
        endTime = ctime()
        resultCollection('updating QOS property is Passed',\
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('Throughput  value is not updated')
        endTime = ctime()
        resultCollection('updating QOS property is failed',\
                ['FAILED',''], startTime, endTime)
    logging.info('verifying the Throuput in volume again ')
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(tp_datapath, tp_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    tp_res2 = getControllerInfo(node_ip, passwd, cmd, 'updtpoutput.txt')
    print tp_res2
    logging.debug('Throughput result is %s', (tp_res2))

    logging.info('comparing the both Throuput  result')
    tp_output = executeCmdNegative('diff tpoutput.txt updtpoutput.txt')
    logging.debug('compared result is %s', (tp_output))
    if tp_output[0] == 'FAILED':
        msg =  "Throughput are not running succesfully"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Throughput value are same after updating the value in ISCSI', \
                ['FAILED',''], startTime, endTime)
    elif tp_output[0] == 'PASSED':
        msg =  "Throughput are running succesfully"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Throughput value are different after updating the value in ISCSI' \
                'and iops are running',['PASSED',''], startTime, endTime)
    else:
        print "Problem in comparing the files"
        
    time.sleep(130)
    logging.info('Executing Vdbench stopped')
    logging.info('logging out from iscsi session')
    login_result = iscsi_login_logout(iqn, tsm_ip, 'logout')
    logging.debug('unmounting the volume %s', (tp_volname))
    nfsUmount2 = umountVolume(mount_dir)
    logging.debug('unmounting volume result is %s', (nfsUmount2))
    if nfsUmount2 == 'PASSED':
        logging.info('Deleting the created volume')
        del_vol = delete_volume(tp_volid, stdurl)
        if del_vol[0] == 'PASSED':
            print del_vol[1]
            logging.debug('deleteing volume  is Passed')
        else:
            endTime = ctime()
            resultCollection('Deleting volume failed',['BLOCKED',''],\
                    startTime, endTime)
    else:
        errormsg = "Problem in unmounting volume"
        endTime = ctime()
        resultCollection('umounting volume failed',['BLOCKED',''],\
                startTime, endTime)
    logging.info('---End of script "Edit QoS properties while'\
            'running IOPS and verify QoS values"---')
    

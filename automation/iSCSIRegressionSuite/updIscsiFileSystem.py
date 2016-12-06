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
        mountNFS, umountVolume, getControllerInfo, getoutput, get_apikey,\
        executeCmdNegative, configFile, resultCollection
from volumeUtils import create_volume, delete_volume, edit_qos_readonly, \
        edit_qos_compression, edit_qos_syncronization, mount_iscsi, \
        getDiskAllocatedToISCSI, listVolumeWithTSMId_new
from utils import assign_iniator_gp_to_LUN, discover_iscsi_lun,\
        iscsi_login_logout, get_logger_footer, execute_mkfs

logging.basicConfig(format = '%(asctime)s %(message)s',\
        filename = 'logs/automation_execution.log',\
        filemode = 'a', level = logging.DEBUG)
logging.info('---Start of script "Modify the lun Attributes and'\
        'verify if I/o interrupts values"---')
readonly_Flag =  comprresion_Flag = Synch_Flag = 0
if len(sys.argv) == 4:
    if  sys.argv[2].lower() == "%s" %("readonly"):
        readonly_Flag = 1
        readonly_value = sys.argv[3].lower()
    elif sys.argv[2].lower() == "%s" %("compression"):
        comprresion_Flag = 1
        compression_value = sys.argv[3].lower()
    elif sys.argv[2].lower() == "%s" %("sync"):
        Synch_Flag = 1
        synch_value = sys.argv[3].lower()
    else:
        print "Arguments are not correct,please provide the corrrect" \
                "arguments as below\n"
        print "python updIscsiFileSystem.py conf.txt readonly/commpression/sync"\
                "true or false/on or off /always or standard"
        exit()
else:
    print "Arguments are not correct,please provide the corrrect" \
            "arguments as below\n"
    print "python updIscsiFileSystem.py conf.txt readonly/commpression/sync"\
            "true or false/on  or off/always or standard"
    exit()

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
tsm_ip = '%s' %(config['ipVSM1'])
passwd = '%s' %(config['password'])

def is_blocked():
    endTime = ctime()
    get_logger_footer('Modifying QOSon iSCSI test completed')
    resultCollection('Modifying QOS functionality on iSCSI LUN test case is',\
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
    resultCollection('Listing of Account failed',['BLOCKED',''],\
            startTime, endTime)
    exit()
try:
    accounts = data["listAccountResponse"]["account"]
    if data["listAccountResponse"]["count"] > 0:
        accId =  data["listAccountResponse"]["account"][0]["id"]
        accName =  data["listAccountResponse"]["account"][0]["name"]
        
except:
    print 'Accounts not present...Create Account'
    endTime = ctime()
    resultCollection('Listing of Account failed',['BLOCKED',''],\
            startTime, endTime)
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
    endTime = ctime()
    resultCollection('Listing of Pool failed',['BLOCKED',''], startTime, endTime)
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
logging.info('Got TSM ID and Dataset ID "%s"  "%s" of "%s"',\
        tsm_id, dataset_id, tsm_name)
##creating volume
logging.info('Creating dictionary for creating volume')
volume1 = {'name': 'iscsiVolume', 'tsmid': tsm_id, 'datasetid': dataset_id,\
        'protocoltype': 'ISCSI','iops':1000}
logging.info('Dictionary created')
logging.debug('%s', volume1)
logging.info('creating volume "%s"', volume1['name'])
create_vol = create_volume(volume1, stdurl)
print create_vol
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
    resultCollection('Listing of volume Blocked the testcase', ['BLOCKED',''],\
            startTime, endTime)
    exit()
volid = vol_list[1][0].get('id')
volname = vol_list[1][0].get('name')
group_id = vol_list[1][0].get('groupid')
vol_iqn = vol_list[1][0].get('iqnname')
logging.info('Got IopsVolume ID = "%s" and Group ID = "%s" of "%s"',\
        volid, group_id, volname)
###########
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

if readonly_Flag == 1:
    res = edit_qos_readonly(stdurl, volid, readonly_value)
    print res[1]
    if res[0] == 'FAILED':
        logging.debug('Read only condition is not updated')
        endTime = ctime()
        resultCollection('updating Read only QOS property is failed', \
                ['BLOCKED',''], startTime, endTime)
    else:
        logging.debug('Read only condition  is updated')
        mkdir_res = executeCmd('mkdir mount/%s/%s' %(volname, volname))
        if mkdir_res[0] == 'FAILED' and readonly_value == 'true':
            logging.debug('Testcase for readonly condition is Passed')
            endTime = ctime()
            resultCollection('Testcase for readonly condition is Passed in ISCSI', \
                    ['PASSED',''], startTime, endTime)
        elif mkdir_res[0] == 'PASSED' and readonly_value == 'false':
            logging.debug('Testcase for readonly condition is Passed')
            endTime = ctime()
            resultCollection('Testcase for readonly condition is Passed in ISCSI ', \
                    ['PASSED',''], startTime, endTime)
        else:
            logging.debug('Testcase for readonly condition is FAILED')
            endTime = ctime()
            resultCollection('Testcase for readonly condition is failed in ISCSI', \
                    ['FAILED',''], startTime, endTime)
    logging.info('logging out from iscsi session')
    login_result = iscsi_login_logout(iqn, tsm_ip, 'logout')
    logging.debug('unmounting the volume %s', (volname))
    Umount1 = umountVolume(mount_dir)
    logging.debug('unmounting volume result is %s', (Umount1))
    if Umount1 == 'PASSED':
        logging.info('Deleting the created volume')
        del_vol = delete_volume(volid, stdurl)
        print del_vol
        logging.debug('deleteing volume result is %s', (del_vol))
        exit()
    else:
        errormsg = "Problem in unmounting volume hence volume is not deleted"
        endTime = ctime()
        resultCollection('umounting volume failed',['BLOCKED',''], startTime, endTime)
    logging.info('---End of script  "Modify the lun Attributes and \
            verify if I/o interrupts values"...')
    exit()
logging.info('...executing vdbench....')
executeVdbenchFile(mount_dir, 'filesystem_iscsi')
##verifying I/Os in volume
logging.info('verifying the I/Os in volume')
io_datapath = poolName+'/'+accName+tsm_name+'/'+volname

time.sleep(15)
cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
        echo "-----------------"; reng stats access dataset %s qos |\
        head -n 4' %(io_datapath, io_datapath)
logging.debug('executing the command %s in controller', str(cmd))
io_res = getControllerInfo(node_ip, passwd, cmd, 'iooutput.txt')
print io_res
logging.debug('I/O result is %s', (io_res))

if comprresion_Flag == 1:
    res = edit_qos_compression(stdurl, volid, compression_value)
    print res[1]
    if res[0] == 'PASSED':
        logging.debug('compression condition  is updated')
        endTime = ctime()
        resultCollection('updating compression QOS property is Passed in ISCSI', \
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('Compression condition  is not updated')
        endTime = ctime()
        resultCollection('updating Compression QOS property is failed in ISCSI', \
                ['FAILED',''], startTime, endTime)
if Synch_Flag ==1:
    res = edit_qos_syncronization(stdurl, volid, synch_value)
    print res[1]
    if res[0] == 'PASSED':
        logging.debug('Synchronization condition is updated')
        endTime = ctime()
        resultCollection('updating Synchronization property is Passed in ISCSI',\
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('Synchronization condition  is not updated')
        endTime = ctime()
        resultCollection('updating Synchronization QOS property is failed in ISCSI', \
                ['FAILED',''], startTime, endTime)

logging.info('verifying the I/Os in volume again ')
time.sleep(10)
cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 20 ;\
        echo "-----------------" ; reng stats access dataset %s qos |\
        head -n 4' %(io_datapath, io_datapath)
logging.debug('executing the command %s in controller', str(cmd))
io_res2 = getControllerInfo(node_ip, passwd, cmd, 'updiooutput.txt')
print io_res2
logging.debug('iops result is %s', (io_res2))
logging.info('comparing the both I/Os result')
io_output = executeCmdNegative('diff iooutput.txt updiooutput.txt')
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
    resultCollection('Iops value are different after updating the value in ISCSI',\
            ['PASSED',''], startTime, endTime)
else: 
    print "problem in comparing files"


time.sleep(130)
logging.info('Executing Vdbench stopped')
logging.info('logging out from iscsi session')
login_result = iscsi_login_logout(iqn, tsm_ip, 'logout')
logging.debug('unmounting the volume %s', (volname))
Umount1 = umountVolume(mount_dir)
logging.debug('unmounting volume result is %s', (Umount1))
if Umount1 == 'PASSED':
    logging.info('Deleting the created volume')
    del_vol = delete_volume(volid, stdurl)
    print del_vol
    logging.debug('deleteing volume result is %s', (del_vol))
else:
    errormsg = "Problem in unmounting volume"
    endTime = ctime()
    resultCollection('umounting volume failed',['BLOCKED',''], startTime, endTime)
logging.info('---End of script  "Modify the lun Attributes and \
        verify if I/o interrupts values"...')


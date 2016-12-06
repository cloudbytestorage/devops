import os
import sys
import time
import json
from time import ctime
import subprocess
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    get_ntwInterfaceAndIP, sendrequest, sshToOtherClient
from volumeUtils import get_volume_info, listVolumeWithTSMId_new, \
    create_volume, delete_volume, getDiskAllocatedToISCSI
from utils import logAndresult, assign_iniator_gp_to_LUN, discover_iscsi_lun, \
        iscsi_login_logout, execute_mkfs, mount_iscsi, deleteiscsiInitiatorGrp
from tsmUtils import get_tsm_info, listTSMWithIP_new

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

##steps followed for this testcase
#1. take iqn of the client
#2. ssh to another client and take its iqn
#3. create a initiator group by giving client's iqn and their IP
#4. create iscsi volume and set the initaor grp
#5. login to the clients and verify

testcase='Adding more initiator in host allow'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Argument are not correct, Please provide as follows"
    print "python moreISCSIInitiatorGroup.py conf.txt "
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
otherClientIP = config["Client1_IP"]
tsmIP = config["ipVSM2"]
initGroup = 'moreInit'

###Add Initiator to the account
def addInitiator(account_id, initGroup, bothInitiatorIqn, network, stdurl):
    querycommand = 'command=addiSCSIInitiator&accountid=%s&name=%s&'\
                    'initiatorgroup=%s&netmask=%s' \
                    %(account_id, initGroup, bothInitiatorIqn, network)
    logging.info('Executing command to add ISCSI InitiatorGroup in Account')
    resp_addInitiator = sendrequest(stdurl, querycommand)
    data = json.loads(resp_addInitiator.text)
    AddInitiators = data["tsmiSCSIInitiatorResponse"]
    if 'errorcode' in str(AddInitiators):
        errormsg = str(data['tsmiSCSIInitiatorResponse']['errortext'])
        print errormsg
        result = ["FAILED", errormsg]
        return result
    else:
        result = ['PASSED', 'Added initiator group']
        return result

def verify_getDiskAllocatedToISCSI(result, mountpoint):
     startTime = ctime()
     if result[0] == 'PASSED' and mountpoint in str(result[1]):
         logging.debug('iscsi logged device... %s', result[1][mountpoint])
         return result[1][mountpoint]
     endTime = ctime()
     msg = 'Not able to get iscsi logged device'
     logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
     
def verify_iscsi_operation(result, vol_name, action):
    if result[0] == 'PASSED':
        logging.debug('%s successfully for iSCSI LUN %s', action, vol_name)
        return
    if 'already exists' in str(result[1]):
        logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
                'get the iscsi device name', vol_name)
        return
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)


logging.info('Getting local client IP')
localClientIP = get_ntwInterfaceAndIP(tsmIP)
if 'FAILED' in localClientIP:
    endTime = ctime()
    print localClientIP[1]
    logAndresult(testcase, 'BLOCKED', localClientIP[1], startTime, endTime)
else:
    localClientIP = localClientIP[1]
    logging.debug('local client IP : "%s"', localClientIP)

ntw1 = "%s/8" %localClientIP
ntw2 = "%s/8" %otherClientIP
network = '%s,%s' %(ntw1, ntw2)

###Getting Intiator IQN from /etc/iscsi Directory
logging.info('Getting Intiator IQN of local machine from /etc/iscsi Directory')
InitiatorIqn = getoutput('cat /etc/iscsi/initiatorname.iscsi '\
                    '| grep iqn | cut -d  "=" -f 2')
InitiatorIqn = InitiatorIqn[0].rstrip('\n')
logging.debug('Got IQN "%s"', InitiatorIqn)
print 'IQN of Local client is : %s' %InitiatorIqn

###SSH of another client
username = config['Client1_user']
pwd = config['Client1_pwd']
cmd = 'cat /etc/iscsi/initiatorname.iscsi | grep iqn | cut -d  "=" -f 2'

logging.info('Establishing SSH for the Client "%s" to get its IQN', \
                    otherClientIP)
otherClientIqn = sshToOtherClient(otherClientIP, username, pwd, cmd)
otherClientIqn = otherClientIqn.rstrip('\n')
logging.debug('Got IQN "%s" of the client "%s"', otherClientIqn, otherClientIP)
print 'IQN of client "%s" is : %s' %(otherClientIP, otherClientIqn)

bothInitiatorIqn = '%s,%s' %(InitiatorIqn, otherClientIqn) 

startTime = ctime()
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsmIP)
tsmList = listTSMWithIP_new(stdurl, tsmIP)
if tsmList[0] == 'PASSED':
    logging.info('TSM present with the given IP "%s"', tsmIP)
    logging.info('Getting tsm_name, tsm_id, and dataset_id...')
    get_tsmInfo = get_tsm_info(tsmList[1])
    tsmID = get_tsmInfo[0]
    tsmName = get_tsmInfo[1]
    datasetID = get_tsmInfo[2]
    logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
            tsmName, tsmID, datasetID)
else:
    endTime = ctime()
    print 'Not able to list Tsm  "%s" due to: ' \
        %(tsmIP) + tsmList[1]
    logAndresult(testcase, 'BLOCKED', tsmList[1], startTime, endTime)

logging.info('Getting account Name and ID')
accountName = tsmList[1][0].get('accountname')
account_id = tsmList[1][0].get('accountid')
logging.debug('account_Name: %s, account_id: %s', accountName, account_id)

vol = {'name': 'moreInitISCSIVol', 'tsmid': tsmID, 'datasetid': datasetID, \
                'protocoltype': 'ISCSI', 'iops': 400}

result = create_volume(vol, stdurl)
if result[0] == 'FAILED':
    endTime = ctime()
    print result
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(vol['name'])
	
startTime = ctime()
logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsmName)
volList = listVolumeWithTSMId_new(stdurl, tsmID)
if volList[0] == 'PASSED':
    logging.info('Volumes present in the TSM "%s"', tsmName)
else: 
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
            %(tsmName) + volList[1] 
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = vol['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_mntPoint, iqnName = get_volInfo[1], get_volInfo[2], \
	get_volInfo[3], get_volInfo[4]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_IqnName: %s',\
                volname, volid, vol_mntPoint, iqnName)

logging.info('Adding initiator group')
init_grp = addInitiator(account_id, initGroup, bothInitiatorIqn, network, stdurl)
if init_grp[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', init_grp[1], startTime, endTime)
else:
    logging.debug('Successfully created initiator group "%s" '\
                'in account "%s"', initGroup, accountName)
    print "Sucessfully created iscsi initiator group \'%s\' "\
                "in %s" %(initGroup, accountName)

volume =  {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}

###Setting the Initiator Group to the volume 
setInitGroup = assign_iniator_gp_to_LUN(stdurl, volid, account_id, initGroup)
if setInitGroup[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', setInitGroup[1], startTime, endTime)
else:
    logging.debug('Successfully updated initiator group "%s" for '\
                    'volume "%s"', initGroup, volname)
    print "sucessfully updated iscsi initiator group '%s' for '%s' "\
            "volume" %(initGroup, volname)
            
discover = discover_iscsi_lun(tsmIP, iqnName)
if discover[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', discover[1], startTime, endTime)
else:
    print discover[1]
    logging.debug('lun discovered : %s', discover[1])

ilogin = iscsi_login_logout(iqnName, tsmIP, 'login')
verify_iscsi_operation(ilogin, volname, 'login')
time.sleep(2)
result = getDiskAllocatedToISCSI(tsmIP, volume['mountPoint'])
device = verify_getDiskAllocatedToISCSI(result, volume['mountPoint'])
print device
fs =  execute_mkfs(device, 'ext3')
if fs[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', fs[1], startTime, endTime)
else:
    print 'filesystem has been written successfully'
    #logging.debug('filesystem has been written successfully')

mountOutput = mount_iscsi(device, volume['name'])               
if mountOutput[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', mountOutput [1], startTime, endTime)
else:
    logging.info('Successfully mounted ISCSI volume "%s"', volume['name'])
    print 'Successfully mounted ISCSI volume "%s"' %volume['name']

time.sleep(1)

unmountISCSI = executeCmd('umount  /dev/%s1' %device)
if unmountISCSI[0] == 'PASSED':
    logging.info('Successfully Unmounted ISCSI lun "/dev/%s1"', device)  
else:
    endTime = ctime()
    msg = 'Unmount failed for lun "/dev/%s1"' %device
    print msg
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

ilogout = iscsi_login_logout(iqnName, tsmIP, 'logout')
verify_iscsi_operation(ilogout, volname, 'logout')

endTime = ctime()
resultCollection('Adding more initiator in host allow, testcase is',\
                    ['PASSED', ' '], startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

logging.info('Setting initiator group to "None"')
setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
if setNone[0] == 'FAILED':
    logging.error('Not able to set auth group to None, do not delete volume')
    exit()
else:
    logging.debug('Initiator group is set to "none"')

logging.info('Deleting initator group "%s"', initGroup)
del_init_grp = deleteiscsiInitiatorGrp(stdurl, account_id, initGroup)
if del_init_grp[0] == 'FAILED':
    logging.error('%s', del_init_grp[1])
else:
    logging.debug('Successfully deleted initiator group "%s"', initGroup)

logging.info('Deleting volume "%s"', volume['name'])
deleteVolume = delete_volume(volid, stdurl)
if deleteVolume[0] == 'PASSED':
    print 'Volume \"%s\" Deleted successfully' %(volume['name'])
    logging.debug('Volume \"%s\" Deleted successfully', \
        volume['name'])
else:
    print 'Failed to deleted the volume \"%s\"' %(volume['name'])
    logging.debug('Failed to deleted the volume \"%s\"', \
            volume['name'])

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)


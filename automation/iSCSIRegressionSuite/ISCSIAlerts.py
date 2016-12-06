import sys
import os
import json
import subprocess
import logging
from time import ctime
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    getControllerInfoAppend
from utils import logAndresult, assign_iniator_gp_to_LUN, discover_iscsi_lun, \
    iscsi_login_logout
from tsmUtils import listTSMWithIP_new, get_tsm_info
from volumeUtils import get_volume_info, listVolumeWithTSMId_new, \
    create_volume, addNFSclient, delete_volume

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
    'logs/automation_execution.log', filemode = 'a', level = logging.DEBUG)

testcase = 'Verify iSCSI login/logout alerts(devd logs)'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows..'
    print 'python ISCSIALerts.py conf.txt'
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

conf = configFile(sys.argv)
apikey = get_apikey(conf)
stdurl = get_url(conf, apikey[1])
tsmIP = conf['ipVSM2']

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

vol = {'name': 'iscsiMountUmount', 'tsmid': tsmID, 'datasetid': datasetID, \
        'protocoltype': 'ISCSI', 'iops': 500}

startTime = ctime()
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
        
setGroup = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'ALL')
if setGroup[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', setGroup[1], startTime, endTime)
else:
    logging.debug('Successfully updated initiator group "ALL" for '\
            'volume "%s"', volname)
    print "sucessfully updated iscsi initiator group 'ALL' for '%s' "\
                "volume" %(volname)

#iscsi login
discover = discover_iscsi_lun(tsmIP, iqnName)
if discover[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', discover[1], startTime, endTime)
else:
    print discover[1]
    logging.debug('lun discovered : %s', discover[1])

login = iscsi_login_logout(iqnName, tsmIP, 'login')
if login[0] == 'PASSED':
    logging.debug('Login successfully for iSCSI LUN %s', volname)
elif 'already exists' in str(result[1]):
    logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
        'get the iscsi device name', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', login[1], startTime, endTime)

nodeIP = tsmList[1][0].get('controlleripaddress')
passwd = "test"
command = 'cat /var/log/devd.log | grep %s | grep logout' \
        %(vol_mntPoint.lower())
logs = getControllerInfoAppend(nodeIP, passwd, command, "results/result.csv")
logging.debug('Login alerts from devd.log is: %s', logs)
print logs

#logout to ISCSI
logout = iscsi_login_logout(iqnName, tsmIP, 'logout')
if logout[0] == 'PASSED':
    logging.debug('Logout successfully for iSCSI LUN %s', volname)
elif 'already exists' in str(result[1]):
    logging.debug('iscsi LUN %s is already loged in, lets go ahead and' \
        'get the iscsi device name', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', logout[1], startTime, endTime)

command = 'cat /var/log/devd.log | grep %s | grep logout' \
        %(vol_mntPoint.lower())
logs = getControllerInfoAppend(nodeIP, passwd, command, "results/result.csv")
logging.debug('Logout alerts from devd.log is: %s', logs)
print logs

endTime = ctime()
resultCollection('ISCSI login/logout alerts(devd logs), '\
    'testcase is', ['PASSED',' '],startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
if setNone[0] == 'FAILED':
    logging.error('Not able to set auth group to None, not deleting volume')
    exit()
else:
    logging.debug('Initiator group is set to "none"')

delvol = delete_volume(volid, stdurl)
if 'FAILED' in delvol:
    print 'Failed to deleted the volume \"%s\"' %(vol['name'])
    logging.debug('Failed to deleted the volume \"%s\"', \
                            vol['name'])
else:
    print 'Volume \"%s\" Deleted successfully' %(vol['name'])
    logging.debug('Volume \"%s\" Deleted successfully', \
                        vol['name'])

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)



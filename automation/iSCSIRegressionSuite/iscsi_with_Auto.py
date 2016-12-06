import os
import sys
import json
import time
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new, get_tsm_info
from volumeUtils import create_volume, delete_volume, getDiskAllocatedToISCSI,\
    listVolumeWithTSMId_new, get_volume_info
from cbrequest import executeCmd, get_url, configFile, sendrequest, \
    resultCollection, getControllerInfo, get_apikey, executeCmdNegative,\
    getoutput, resultCollectionNew
from utils import logAndresult, assign_iniator_gp_to_LUN, discover_iscsi_lun, \
    iscsi_login_logout, update_iscsi_services

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

testcase = 'Discover Lun by setting Discovery Auth Method to Auto'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Argument are not correct, Please provide as follows"
    print "python iscsi_with_Autho.py conf.txt "
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

#----config/basic details---------------------------------------
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM1"]
#------------Vsm details------------------
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
#------------------------------------------------------------------------
#------------Volume details-------------------
vol = {'name': 'iscsiAuto', 'tsmid': tsmID, 'datasetid': datasetID, \
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

volume =  {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}
#----------------------------------------------------------------------

#-------------iscsi details----------------------------
#set auth method & initator grp....
services = {'auth_method': 'Auto', 'init_group': 'ALL'}
startTime = ctime()
auto = update_iscsi_services(stdurl, volid, account_id, services)
if auto[0] == 'PASSED':
    msg = 'Successfully update Auth method to "%s" for volume "%s"' \
            %(services.get('auth_method'), volname)
    logging.debug('%s', msg)
    print msg
else:
    endTime = ctime()
    msg = 'Failed to update Auth method to "%s" for volume "%s"' \
        %(services.get('auth_method'), volname)
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

#discover, login....
startTime = ctime()
discover = discover_iscsi_lun(tsmIP, iqnName)
if discover[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', discover[1], startTime, endTime)
else:
    print discover[1]
    logging.debug('lun discovered : %s', discover[1])

ilogin = iscsi_login_logout(iqnName, tsmIP, 'login')
if result[0] == 'PASSED':
    logging.debug('Login successfully for iSCSI LUN %s', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'FAILED', result[1], startTime, endTime)

endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED', ' '], \
        startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

logging.debug('getting iSCSI LUN logged device...')
time.sleep(2)
result = getDiskAllocatedToISCSI(tsmIP, volume['mountPoint'])
print result
logging.debug('iSCSI LUN logged in device: %s', result)

#--------------------------------------------------------------------------

#removing configurations
ilogout = iscsi_login_logout(iqnName, tsmIP, 'logout')

logging.info('Setting initiator group to "None"')
setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
if setNone[0] == 'FAILED':
    logging.error('Not able to set auth group to None, do not delete volume')
    exit()
else:
    logging.debug('Initiator group is set to "none"')

logging.info('Deleting volume "%s"', volume['name'])
deleteVolume = delete_volume(volid, stdurl)
if deleteVolume[0] == 'PASSED':
    print 'Volume \"%s\" Deleted successfully' %(volname)
    logging.debug('Volume \"%s\" Deleted successfully', volname)
else:
    print 'Failed to deleted the volume \"%s\"' %(volname)

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)

#------------------------------------------------------------------------------







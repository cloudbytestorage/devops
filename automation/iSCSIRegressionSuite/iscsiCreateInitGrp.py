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
    getoutput, resultCollectionNew, get_ntwInterfaceAndIP
from utils import logAndresult, assign_iniator_gp_to_LUN, discover_iscsi_lun, \
    iscsi_login_logout, add_initator_group, deleteiscsiInitiatorGrp

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

testcase = 'Create a initiator group using all the mandatory feilds'

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

#getting this client IP
logging.info('Getting local client IP')
localClientIP = get_ntwInterfaceAndIP(tsmIP)
if localClientIP[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', localClientIP[1], startTime, endTime)
else:
    localClientIP = localClientIP[1]
    logging.debug('local client IP : "%s"', localClientIP)

ntw = "%s/8" %localClientIP
logging.debug('Network to be provided during initiator grp creation is: %s', \
        ntw)

#getting this client iqn
logging.info('Getting Intiator IQN of local machine from /etc/iscsi Directory')
InitIqn = getoutput('cat /etc/iscsi/initiatorname.iscsi '\
              '| grep iqn | cut -d  "=" -f 2')
InitIqn = InitIqn[0].rstrip('\n')
logging.debug('Got client IQN : "%s"', InitIqn)
print 'IQN of Local client is : %s' %InitIqn

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
#creating initator group....
initGrpName = 'InitNewGrp'
add_init = add_initator_group(account_id, initGrpName, InitIqn, ntw, stdurl)
if add_init[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', add_init[1], startTime, endTime)
else:
    logging.debug('%s')

logging.info('Created initiator grp, now validating it by logging into client')

#------------Volume details-------------------
vol = {'name': 'iscsiNewInit', 'tsmid': tsmID, 'datasetid': datasetID, \
                'protocoltype': 'ISCSI', 'iops': 100}

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
#set initator grp to created grp....
setInitGroup = assign_iniator_gp_to_LUN(stdurl, volid, account_id, initGrpName)
if setInitGroup[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', setInitGroup[1], startTime, endTime)
else:
    logging.debug('Successfully updated initiator group "%s" for '\
                 'volume "%s"', initGrpName, volname)
    print "sucessfully updated iscsi initiator group '%s' for '%s' "\
            "volume" %(initGrpName, volname)

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

logging.info('Deleting initator group "%s"', initGrpName)
del_init_grp = deleteiscsiInitiatorGrp(stdurl, account_id, initGrpName)
if del_init_grp[0] == 'FAILED':
    logging.error('%s', del_init_grp[1])
else:
    logging.debug('Successfully deleted initiator group "%s"', initGrpName)

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







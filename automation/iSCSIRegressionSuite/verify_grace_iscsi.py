import os
import sys
import json
import time
from time import ctime
import subprocess
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
    get_apikey, executeCmd, getoutput
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, mountPointDetails, assign_iniator_gp_to_LUN, \
    iscsi_login_logout, iscsi_mount_flow
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

##-----steps------
#provision volume and expose to client
#run IO
#deprovision it
#verify tsm IOPs after deprovision
#repeat the process for required number of times
#----------------------------------------------------

testcase = 'provisioning and deprovisioning of volumes(NFS and ISCSI)'

logging.info('----Start of testcase "%s"----', testcase)
if len(sys.argv) < 2:
    print "Argument are not correct, Please provide as follows"
    print "python provision_deprovision_nfs_iscsi.py conf.txt "
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
otherClientIP = config["Client1_IP"]
tsmIP = config["ipVSM1"]

startTime = ctime()
tsmList = listTSMWithIP_new(stdurl, tsmIP)
endTime = ctime()
if tsmList[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', tsmList[1], startTime, endTime)

get_tsmInfo = get_tsm_info(tsmList[1])
tsmID = get_tsmInfo[0]
tsmName = get_tsmInfo[1]
datasetID = get_tsmInfo[2]
account_id = tsmList[1][0].get('accountid')
poolName = tsmList[1][0].get('hapoolname')
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, poolName:%s, account_id:%s', \
        tsmName, tsmID, datasetID, poolName, account_id)

startTime = ctime()
for i in range(1, 6):
	vol = {'name': 'iscsiPD%s' %i, 'tsmid': tsmID, 'datasetid': datasetID, \
		'protocoltype': 'ISCSI', 'iops': 100, 'quotasize': '5G'}
	volname = vol['name']
	result = create_volume(vol, stdurl)
	endTime = ctime()
	if result[0] == 'FAILED':
		logAndresult(testcase, 'FAILED', result[1], startTime, endTime)
	logging.debug('"%s" was created successfully',volname)
	logging.info('volume provision was successful for "%s times"', i)
	
	volList = listVolumeWithTSMId_new(stdurl, tsmID)
	endTime = ctime()
	if volList[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

	get_volInfo = get_volume_info(volList[1], volname)
	volid, vol_mntPoint, vol_iqn = get_volInfo[2], get_volInfo[3], get_volInfo[4]
	print volid, vol_mntPoint
	logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_Iqn: %s',\
		volname, volid, vol_mntPoint, vol_iqn)

	startTime = ctime()
	init_grp = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'ALL')
	endTime = ctime()
	if init_grp[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', init_grp[1], startTime, endTime)
	logging.debug('Iscsi Initiator group is set to "ALL" for the volume')

	volume = {'TSMIPAddress' : tsmIP, 'mountPoint': volname, 'name' : volname}

	mnt_iscsi = iscsi_mount_flow(volname, tsmIP, vol_iqn, vol_mntPoint, 'ext3')
	endTime = ctime()
	if mnt_iscsi[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', mnt_iscsi[1], startTime, endTime)
	logging.debug('%s', mnt_iscsi[1])
	device, iqn = mnt_iscsi[3], mnt_iscsi[2]

	mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
			    %(volume['name']))
	mount_point = mount_point[0].strip('\n')

	executeVdbenchFile(volume, 'filesystem_nfs')
	check_vdbench = is_vdbench_alive(volname)
	time.sleep(1)
	while True:
	    mountDetails = mountPointDetails('-m', mount_point)
	    Used = mountDetails[2]
	    if int(Used) >= 1000:
		logging.debug('vdbench has successfully created 1 GB file of the')
		logging.debug('going to stop vdbench after 10 seconds...')
		time.sleep(10)
		break
	    check_vdbench = is_vdbench_alive(volname)
	    if check_vdbench:
		continue
	    else:
		logging.debug('vdbench has stopped unexpectedly....')
		break

	kill_vdbench()
	logging.info('waiting for 10s')
	time.sleep(10)

	umount_output = executeCmd('umount -l /dev/%s1' %device)
	if umount_output[0] == 'FAILED':
	    logging.error('Not able to umount %s, still go ahead and delete '\
		'the Iscsi volume', volname)
	else:
	    logging.debug('Iscsi volume %s umounted successfully', volname)

	logout_result = iscsi_login_logout(iqn, tsmIP, 'logout')
	if logout_result[0] == 'FAILED':
	    logging.error('%s', logout_result[1])
	logging.debug('%s', logout_result[1])

	logging.info('Setting initiator group to "None"')
	setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
	if setNone[0] == 'FAILED':
	    logging.error('Not able to set initiator group to None, do not delete volume')
	    exit()
	else:
	    logging.debug('Initiator group is set to "none"')


	delete_result = delete_volume(volid, stdurl)
	endTime = ctime()
	if delete_result[0] == 'FAILED':
	    logAndresult(testcase, 'FAILED', delete_result[1], startTime, endTime)
	logging.debug('Volume "%s" deleted successfully', volname)
	logging.info('volume provision was successful for "%s times"', i)
endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED',' '], \
                startTime, endTime)




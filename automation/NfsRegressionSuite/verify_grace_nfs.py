import os
import sys
import json
import time
from time import ctime
import subprocess
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
    get_apikey, executeCmd, mountNFS, getoutput
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, mountPointDetails
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
accName = tsmList[1][0].get('accountname')
poolName = tsmList[1][0].get('hapoolname')
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, poolName:%s', \
        tsmName, tsmID, datasetID, poolName)

startTime = ctime()
for n in range(1, 6):
	vol = {'name': 'nfsPD%s' %n, 'tsmid': tsmID, 'datasetid': datasetID, \
		'protocoltype': 'NFS', 'iops': 100, 'quotasize': '5G'}
	volname = vol['name']
	result = create_volume(vol, stdurl)
	endTime = ctime()
	if result[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
	logging.debug('"%s" was created successfully',volname)
	logging.info('volume provision was successful for "%s times"', n)
	
	volList = listVolumeWithTSMId_new(stdurl, tsmID)
	endTime = ctime()
	if volList[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

	get_volInfo = get_volume_info(volList[1], volname)
	volid, vol_mntPoint = get_volInfo[2], get_volInfo[3]
	print volid, vol_mntPoint
	logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
		volname, volid, vol_mntPoint)

	startTime = ctime()
	addClient = addNFSclient(stdurl, volid, 'ALL')
	endTime = ctime()
	if addClient[0] == 'FAILED':
	    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)
	logging.debug('Added nfs client "ALL" to the volume')

	volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
		'name' : volname}

	nfsMount = mountNFS(volume)
	if nfsMount[0] == 'FAILED':
	    msg = 'failed to mount NFS share "%s"' %(volume['name'])
	    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
	logging.info('Mounted Nfs Share "%s" successfully', volname)

	mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
			    %(volume['mountPoint']))
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

	umount_output = executeCmd('umount -l mount/%s' %(volume['mountPoint']))
	if umount_output[0] == 'FAILED':
	    logging.error('Not able to umount %s, still go ahead and delete '\
		'the NFS share', volname)
	else:
	    logging.debug('NFS share %s umounted successfully', volname)

	delete_result = delete_volume(volid, stdurl)
	endTime = ctime()
	if delete_result[0] == 'FAILED':
	    logAndresult(testcase, 'FAILED', delete_result[1], startTime, endTime)
	
	logging.debug('Volume "%s" deleted successfully', volname)
	logging.info('volume provision was successful for "%s times"', n)
endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED',' '], \
                startTime, endTime)




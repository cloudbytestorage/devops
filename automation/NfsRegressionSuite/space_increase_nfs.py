import os
import sys
import json
import time
from time import ctime
import subprocess

from cbrequest import get_url, configFile, sendrequest, resultCollection, \
    get_apikey, executeCmd, mountNFS, getoutput
from tsmUtils import get_tsm_info, listTSMWithIP_new, tsm_creation_flow, \
    verify_tsmIP_from_configFile, delete_tsm
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new, edit_vol_quota
from utils import logAndresult, mountPointDetails
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_process
from poolUtils import pool_creation_flow, delete_pool

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

##-----steps------
#provision volume and expose to client
#run IO
#increase space, verify if increased and dump some data on increased space
#----------------------------------------------------

testcase = 'Increase Space of NFS volume'

logging.info('----Start of testcase "%s"----', testcase)
if len(sys.argv) < 2:
    print "Argument are not correct, Please provide as follows"
    print "python increase_space_nfs.py conf.txt "
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
link_iso = 'http://20.10.1.101/dailybuilds/1.4.0.p5/Apr22-1.4.0.891/ElastiStor_1_4_0_Apr22_1.4.0.891.iso'

startTime = ctime()
verify_tsmIP = verify_tsmIP_from_configFile(config, stdurl)
endTime = ctime()
if verify_tsmIP[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', verify_tsmIP[1], startTime, endTime)

tsmIP = verify_tsmIP[1]
tsmInterface = verify_tsmIP[2]

#---------create pool--------
poolName = 'nPoolspace'
pool_create =  pool_creation_flow(stdurl, poolName, 2, 'SAS', 'mirror')
endTime = ctime()
if pool_create[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', pool_create[1], startTime, endTime)
logging.debug('Pool "%s" is created successfully', poolName)
#------------------------------------
#----------create tsm---------------------
startTime = ctime()
acctName = 'Account'
tsm_params = {'name': 'nTsmSpace', 'ipaddress': tsmIP, 'tntinterface': tsmInterface}
tsm_create = tsm_creation_flow(stdurl, poolName, acctName, tsm_params)
endTime = ctime()
if tsm_create[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', tsm_create[1], startTime, endTime)
logging.debug('%s', tsm_create[1])
#----------------------------------------------


tsmList = listTSMWithIP_new(stdurl, tsmIP)
endTime = ctime()
if tsmList[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', tsmList[1], startTime, endTime)

get_tsmInfo = get_tsm_info(tsmList[1])
tsmID = get_tsmInfo[0]
tsmName = get_tsmInfo[1]
datasetID = get_tsmInfo[2]
pool_id = tsmList[1][0].get('poolid')

logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s', \
        tsmName, tsmID, datasetID)

startTime = ctime()
vol = {'name': 'nfsSpace', 'tsmid': tsmID, 'datasetid': datasetID, \
		'protocoltype': 'NFS', 'iops': 100, 'quotasize': '2G'}
volname = vol['name']
result = create_volume(vol, stdurl)	
endTime = ctime()
if result[0] == 'FAILED':
   logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
   
logging.debug('"%s" was created successfully',volname)

volList = listVolumeWithTSMId_new(stdurl, tsmID)
endTime = ctime()
if volList[0] == 'FAILED':
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

get_volInfo = get_volume_info(volList[1], volname)
volid, vol_mntPoint, vol_quota = get_volInfo[2], get_volInfo[3], get_volInfo[6]

logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_quota: %s',
		volname, volid, vol_mntPoint, vol_quota)
		
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
print mount_point

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

kill_process(volname)
#kill_vdbench()
logging.info('waiting for 10s')
time.sleep(10)

mountDetails = mountPointDetails('-h', mount_point)
Used1 = mountDetails[2].strip('G')
logging.debug('Before increasing size, used space of nfs share is: %s', Used1)

logging.info('Increasing space of NFS volume')
quota = '5G'
quota1 = quota.rstrip('G')
edit_quota = edit_vol_quota(volid, quota, stdurl)
if edit_quota[0] == 'FAILED':
    logAndresult(testcase, 'FAILED', edit_quota[1], startTime, endTime)
logging.debug('Successfully updated quota of volume "%s" from %s to %s'\
	,volname, vol_quota, quota)
time.sleep(5)
logging.info('verifying quota update of client side')
mountDetails1 = mountPointDetails('-h', mount_point)
size = mountDetails1[1].strip('G')
if float(size) == float(quota1):
    logging.debug('Quota of Nfs share has been updated on client side')
else:
    msg = 'Size is not updated on client side, current size is : %s' %size
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

logging.info('Dumping some data to nfs share after increasing space')
copy_data = os.system('wget -P %s/ %s' %(mount_point, link_iso))

time.sleep(3)  
mountDetails1 = mountPointDetails('-h', mount_point)
Used2 = mountDetails1[2]
logging.debug('After dumping data used space is %s', Used2)

if str(Used2) > str(Used1):
    logging.debug('Data is written into the share')

endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED',' '], \
                startTime, endTime)

umount_output = executeCmd('umount -l mount/%s' %(volume['mountPoint']))
if umount_output[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete '\
		'the NFS share', volname)
else:
    logging.debug('NFS share %s umounted successfully', volname)

delete_result = delete_volume(volid, stdurl)
endTime = ctime()
if delete_result[0] == 'FAILED':
	    logging.debug('%s',delete_result[1])
logging.debug('Volume "%s" deleted successfully', volname)

del_tsm = delete_tsm(tsmID, stdurl)
if del_tsm[0] == 'FAILED':
    logging.error('%s', del_tsm[1])
    logging.error('Tsm deletion failed, hence not deleting pool')
    exit()
logging.debug('%s', del_tsm[1])

del_pool = delete_pool(pool_id, stdurl)
if del_pool[0] == 'FAILED':
    logging.error('%s', del_pool[1])
logging.debug('%s', del_pool[1])

logging.info('----End of testcase "%s"----', testcase)


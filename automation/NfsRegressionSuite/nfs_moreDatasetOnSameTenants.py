import os
import sys
import json
import time
import subprocess
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    executeCmd, resultCollection, resultCollectionNew, sendrequest, \
    configFile
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new
from tsmUtils import get_tsm_info, listTSMWithIP_new
from utils import  logAndresult
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_process

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

#covers 2 testcase
#1.After enabling NFS on a dataset add one more dataset to the same \
        #Tenant and check whether it affects
#2.Mount the NFS share on a client machine and perform IO on it and \
        #during that time add a second dataset

testcase = 'After enabling NFS on a dataset add one more dataset to the same '\
        'Tenant and check whether it affects'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfs_moreDatasetOnSameTenants.py conf.txt vdb_file(optional)"
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

VdbFile = 'filesystem_nfs'
#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]
ClientIP = 'all'

#---------------------------Methods--------------------------------------------
#to create volume and mount the same
def addVol_client_Mount(vol, stdurl, tsmID, tsmName, ClientIP):
    startTime = ctime()
    result = create_volume(vol, stdurl)
    if result[0] == 'FAILED':
        endTime = ctime()
        print result[1]
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
    volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3]
    logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
            volname, volid, vol_mntPoint)

    startTime = ctime()        
    addClient = addNFSclient(stdurl, volid, ClientIP)
    if addClient[0] == 'PASSED':
        print 'Added NFS client "%s" to volume "%s"' %(ClientIP, volname)
        logging.info('Added NFS client "%s" to volume "%s"', \
                        ClientIP, volname)
    else:
        endTime = ctime()
        logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

    volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}

    startTime = ctime()
    logging.info("Mounting NFS Share '%s'", volname)
    nfsMount = mountNFS(volume)
    if nfsMount == 'PASSED':
        logging.info('Mounted Nfs Share "%s" successfully', volume['name'])
    else:
        endTime = ctime()
        msg = 'failed to mount NFS share "%s"' %volume['name']
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    
    return [volume, volid]

#*************************************************************************
#to delete volume
def delete_dataset(volname, volid, stdurl):
    deleteVolume =  delete_volume(volid, stdurl)
    if 'PASSED' in deleteVolume:
        print 'Volume \"%s\" Deleted successfully' %(volname)
        logging.debug('Volume \"%s\" Deleted successfully', volname)
    else:
        print 'Failed to deleted the volume \"%s\"' %(volname)
        logging.debug('Failed to deleted the volume \"%s\"',volname)

#**************************************************************************
#to unmount the nfs share
def umount_share(volume):
    umount = umountVolume_new(volume)
    if 'FAILED' in umount[0] and 'device is busy' in umount[1]:
        print 'Unmount is failing as device is busy, hence unmounting forcefully'
        logging.info('unmount is failing hence unmounting forcefully')
        umount_output = executeCmd('umount -l mount/%s' \
                    %(volume['mountPoint']))
        if umount_output[0] == 'PASSED':
            logging.debug('Forceful unmount passed for volume "%s"', \
                            volume['name'])
        else:
            logging.debug('Forcefull umount failed due to: %s', \
                umount_output[1])
    elif 'FAILED' in umount[0]:
        logging.debug('Unmount failed for the volume "%s" due to: %s', \
            volume['name'], umount[1])        
    else:
        print umount[1]
        logging.debug('Volume "%s" umounted successfully', volume['name'])

#-------------------------------------------------------------------------------

#listing tsm and getting required details
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

					
vol1 = {'name': 'nfsDataset1', 'tsmid': tsmID, \
    'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 200}

#creating volume and mouting the same
final_result1 = addVol_client_Mount(vol1, stdurl, tsmID, tsmName, ClientIP)

#running vdbench on the first volume
logging.info('Running vdbench  by using file')
exe1 = executeVdbenchFile(final_result1[0], VdbFile)
logging.info('waiting for 30s for vdbench to run on first dataset')
time.sleep(30)
check_vdbench1 = is_vdbench_alive(vol1['name'])

if check_vdbench1:
    logging.info('vdbench is running on first dataset....')
    logging.info('Adding one more NFS dataset to the same VSM and '\
            'mounting it on the same client and running vdbench on it')
    
    #while Ios are running creating another volume to the same tenant
    vol2 = {'name': 'nfsDataset2', 'tsmid': tsmID, \
        'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 200}
    final_result2 = addVol_client_Mount(vol2, stdurl, tsmID, tsmName, ClientIP)
    time.sleep(2)
    logging.info('Checking whether vdbench is running on first dataset after' \
            'adding another dataset to same tenant')

    #verifying if IOs are affected on first volume
    check_vdbench1 = is_vdbench_alive(vol1['name'])
    if not check_vdbench1:
        msg = 'After adding another dataset to same tenant the vdbench of '\
                'first dataset is stopped'
        print msg
        logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
    logging.debug('After adding another dataset to same tenant, IOs are still '\
            'running on first dataset')
    
    #Starting vdbench on second volume
    logging.info('Starting vdbench on second dataset')
    exe2 = executeVdbenchFile(final_result2[0], VdbFile)
    logging.info('waiting for 30s for vdbench to run on second dataset')
    time.sleep(30)
    #Verifying vdbench is running or not
    check_vdbench2 = is_vdbench_alive(vol2['name'])
    if check_vdbench2:
        logging.info('vdbench is running on second dataset...')
    else:
        endTime = ctime()
        msg = 'Vdbench has stopped running on second dataset....'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
else:
    endTime = ctime()
    msg = 'Vdbench has stopped running on first dataset'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
        startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
logging.debug('%s, testcase PASSED', testcase)

logging.info('Checking whether vdbench is still running or not....')
check_vdbench = is_vdbench_alive(vol1['name'])
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_process(vol1['name'])
    time.sleep(2)
    check_vdbench = is_vdbench_alive(vol2['name'])
    if check_vdbench:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_process(vol2['name'])
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

# clearing the configurations
logging.info('Unmounting volume "%s"', vol1['name'])
u1 =  umount_share(final_result1[0])
logging.info('Unmounting volume "%s"', vol2['name'])
u2 = umount_share(final_result2[0])

logging.info('Deleting volume "%s"', vol1['name'])
d1 = delete_dataset(vol1['name'], final_result1[1], stdurl)
logging.info('Deleting volume "%s"', vol2['name'])
d2 =  delete_dataset(vol2['name'], final_result2[1], stdurl)

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----' %testcase)


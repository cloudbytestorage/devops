import sys
import os
import json
import logging 
import time
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, executeCmd
from tsmUtils import get_tsm_info, editNFSthreads, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, delete_volume, \
    addNFSclient, edit_vol_quota, edit_qos_iops, listVolumeWithTSMId_new
from utils import logAndresult
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_process

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

###Steps followed for this this case
#1. while IOS are running editing vol properties like iops, quota and nfs threads
#2. if vdbench stops/any error occurs testcase is failed

testcase = 'Edit the properties of the dataset while IOs are running'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print 'python nfsPropEdit.py conf.txt vdbFile'
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()

VdbFile = 'filesystem_nfs'
logging.info('standard file taken to run vdbench is "%s"', VdbFile)

#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]

#parameters to edit while IOs are running....
quota = '20G'
iops = 200
nfsThread = 256

#listing tsm and getting required details
startTime = ctime()
list_tsm = listTSMWithIP_new(stdurl, tsmIP)
if list_tsm[0] == 'PASSED':
    logging.info('TSM present with the given IP "%s"', tsmIP)
    logging.info('Getting tsm_name, tsm_id, and dataset_id...')
    get_tsmInfo = get_tsm_info(list_tsm[1])
    tsm_id = get_tsmInfo[0]
    tsm_name = get_tsmInfo[1]
    dataset_id = get_tsmInfo[2]
    logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
                        tsm_name, tsm_id, dataset_id)
else:
    endTime = ctime()
    print list_tsm[1]
    logAndresult(testcase, 'BLOCKED', list_tsm[1], startTime, endTime)

#creating volume and getting required details
startTime = ctime()
vol = {'name': 'NfsPropEdit', 'tsmid': tsm_id, 'datasetid': dataset_id, \
        'protocoltype': 'NFS', 'iops': 100}
result = create_volume(vol, stdurl)
if result[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(vol['name'])

startTime = ctime()
logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
volList = listVolumeWithTSMId_new(stdurl, tsm_id)
if volList[0] == 'PASSED' :
    logging.info('Volumes present in the TSM "%s"', tsm_name)
else:
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + volList[1]
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = vol['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_mntPoint, vol_grpID, vol_quota = get_volInfo[1], \
        get_volInfo[2], get_volInfo[3], get_volInfo[5], get_volInfo[6]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
                volname, volid, vol_mntPoint)
logging.debug('vol_grpID: %s, vol_quota: %s', vol_grpID, vol_quota)

#adding nfs client as all
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'PASSED':
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

#mounting nfs share
volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}
startTime = ctime()
logging.info("Mounting NFS Share '%s'", volname)
nfsMount = mountNFS(volume)
if nfsMount == 'PASSED':
    logging.info('Mounted Nfs Share "%s" in "mount/%s" successfully',\
                    volume['name'], volume['mountPoint'])
else:
    endTime = ctime()
    msg = 'Failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

#running vdbench
logging.info('Running vdbench  by using file')
exe = executeVdbenchFile(volume, VdbFile)
logging.info('waiting for 30s for vdbench to run')
time.sleep(30)

logging.info('Checking whether vdbench is running or not....')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('vdbench is running')
    logging.info('Editing volume properties while IOs are running....')
    
    #Editting quota while IOs are running 
    logging.info('Editing Quota....')
    startTime = ctime()
    edit_quota = edit_vol_quota(volid, quota, stdurl)
    if edit_quota[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to update quota while IOs are running due to: %s'\
                , edit_quota[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                startTime, endTime)
    else:
        endTime = ctime()
        print 'Successfully updated quota of volume "%s" from %s to %s' \
                'while IOs are running' %(volname, vol_quota, quota)
        logging.debug('Successfully updated quota of volume "%s" from %s to %s'\
                ' while IOs are running' ,volname, vol_quota, quota)
        resultCollection('Successfully updated quota while IOs are running', \
            ['PASSED', ''], startTime, endTime)
 
    logging.info('Sleeping for 10s before editing another property....')
    time.sleep(10) #waiting 10s before editing other properties 
    logging.info('Checking whether vdbench is still running or not....')
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing Quota'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    
    #Editting Iops while Ios are running
    logging.info('Editing IOPS....')
    startTime = ctime()
    edit_iops = edit_qos_iops(vol_grpID, iops, stdurl) 
    if edit_iops[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to update iops while IOs are running due to: %s',\
                edit_iops[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                startTime, endTime)
    else:
        endTime = ctime()
        print 'Successfully updated iops of volume "%s" from %s to %s' \
               ' while IOs are running' %(volname, vol['iops'], iops)
        logging.debug('Successfully updated iops of volume "%s" from %s to %s '\
                'while IOs are running' ,volname, vol['iops'], iops)
        resultCollection('Successfully updated IOPS while IOs are running', \
            ['PASSED', ''], startTime, endTime)
    
    logging.info('Sleeping for 10s before editing another property....')
    time.sleep(10) #waiting 10s before editing other properties 
    logging.info('Checking whether vdbench is still running or not....')
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing IOPs'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
        
    #Editting nfs thread while IOs are running    
    logging.info('Editing NFS threads....')
    startTime = ctime()
    edit_threads = editNFSthreads(tsm_id, nfsThread, stdurl)
    if edit_threads[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to update nfs threads while IOs are '\
                'running due to: %s', edit_threads[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
                startTime, endTime)
    else:
        endTime = ctime()
        print 'Successfully updated nfs threads for volume "%s" to %s'\
                ' while IOs are running' %(volname, nfsThread)
        logging.debug('Successfully updated nfs threads for volume "%s" to %s'\
                ' while IOs are running' ,volname, nfsThread)
        resultCollection('Successfully updated nfs threads while IOs are '\
                'running', ['PASSED', ''], startTime, endTime)
    
    time.sleep(10)#after editing threads waiting for 10s
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing nfs threads'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)

else:
    endTime = ctime()
    msg = 'Vdbench has stopped running'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

#collecting results in result.csv
endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
        startTime, endTime)
logging.debug('%s, testcase PASSED', testcase)

logging.info('Checking whether vdbench is still running or not....')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_process(volname)
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

#Clearing configurations
time.sleep(2)
startTime = ctime()
logging.info("UnMounting NFS Share '%s'", volume['name'])
count = 0
while True:
    umount = umountVolume_new(volume)
    if 'FAILED' in umount[0] and 'device is busy' in umount[1]:
        if count < 5 :
            print 'Unmount is failing as device is busy, hence waiting for 5s'
            logging.info('Since device is busy waiting for 5s and '\
                'then trying to umount')
            time.sleep(5)
            count = count + 1
            continue
        else:
            total_time = count * 5
            logging.info('waited for %s seconds still unmount is failing, '\
                    'hence unmounting forcefully', total_time)
            print 'waited for %s seconds still unmount is failing, '\
                    'hence unmounting forcefully' %total_time
            umount_output = executeCmd('umount -l mount/%s' \
                    %(volume['mountPoint']))
            if umount_output[0] == 'PASSED':
                logging.debug('Forceful unmount passed for volume "%s"', \
                        volume['name'])
                break
            else:
                logging.debug('Forcefull umount failed due to: %s', \
                        umount_output[1])
                break
    elif 'FAILED' in umount[0]:
        logging.debug('Unmount failed for the volume "%s" due to: %s', \
                volume['name'], umount[1])
        break
    else:
        print umount[1]
        logging.debug('Volume "%s" umounted successfully', volume['name'])
        break

startTime = ctime()
logging.info('Deleting volume "%s"', volume['name'])
deleteVolume =  delete_volume(volid, stdurl)
if 'PASSED' in deleteVolume:
    print 'Volume \"%s\" Deleted successfully' %(volume['name'])
    logging.debug('Volume \"%s\" Deleted successfully', \
             volume['name'])
else:
    print 'Failed to deleted the volume \"%s\"' %(volume['name'])
    logging.debug('Failed to deleted the volume \"%s\"', \
        volume['name'])

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----' %testcase)

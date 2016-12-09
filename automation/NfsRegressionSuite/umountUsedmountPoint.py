import sys
import os
import time
import json
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, executeCmd, getoutput
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, delete_volume, \
    addNFSclient, listVolumeWithTSMId_new
from utils import logAndresult
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_process

TC_name = sys.argv[0]
TC_name = TC_name.replace('.py','.log')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
            filename='logs/'+TC_name,filemode='a',level=logging.DEBUG)

###steps followed for this testcase.....
#1. mount the share, 
#2. run vdbench on that share
#3. the file in mountPoint is in use, now unmount the mountPoint
#4. if umount failed testcase passed else failing the testcase

testcase = "Unmount the mount point when the file from the mount point is in use"

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2 :
    print "Arguments are not correct, Please provide as follows..."
    print "python umountUsedmountPoint.py conf.txt"
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()

VdbFile = 'filesystem_nfs'
logging.info('standard file taken to run vdbench is "%s"', VdbFile)

#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
file_name = sys.argv[0]
tsmIP = config["ipVSM2"]

###flag for checking umount within mount point, initally considering false
umountFail = False

###----------------------Method------------------------------------------------
##this method is for unmounting inside mount point
def UseFileInMountPoint(volume):
    output = getoutput('mount | grep %s | awk \'{print $3}\'' \
            %(volume['mountPoint']))
    mount_point = output[0].strip('\n')
    exe_vdb = executeVdbenchFile(volume, VdbFile)
    time.sleep(20)
    #sleeping for 30s before trying to umount the volume on which vdbench is running
    logging.info('Now unmounting the mountPoint which is in use')
    check_vdbench = is_vdbench_alive(volume['name'])
    if check_vdbench:
        umount_output = executeCmd('umount mount/%s' %(volume['mountPoint']))
        if umount_output[0] == 'FAILED':
            print 'expected result : %s' %(umount_output[1])
            logging.debug('expected result: %s', umount_output[1])
            umountFail = True
            return ['PASSED', umountFail]
        else:
            print 'Unexpected Result: Unmount happened when file in '\
                    'mountPoint is in use'
            kill_process(volume['name'])
            return ['FAILED', 'Unmount happened when file in mountPoint is in use']
    else:
        return ['FAILED', 'Vdbench stopped, MountPoint not in use']
#------------------------------------------------------------------------------

#listing tsm and getting required details
startTime = ctime()
list_tsm = listTSMWithIP_new(stdurl, tsmIP)
if 'PASSED' in list_tsm:
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

## creating volume and getting required details
vol = {'name': 'nfsVolInUse', 'tsmid': tsm_id, 'datasetid': dataset_id, \
                        'protocoltype': 'NFS', 'iops': 100}
startTime = ctime()
result = create_volume(vol, stdurl)
if result[0] == 'FAILED':
    endTime = ctime()
    print result[1]
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(vol['name'])

startTime = ctime()
logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
volList = listVolumeWithTSMId_new(stdurl, tsm_id)
if volList[0] == 'PASSED':
    logging.info('Volumes present in the TSM "%s"', tsm_name)
else:
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + volList[1]
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = vol['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3] 
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
        volname, volid, vol_mntPoint)

##adding nfs client as All
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] ==  'PASSED':
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

# mounting nfs share
volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}
startTime = ctime()
logging.info("Mounting NFS Share '%s'", volname)
nfsMount = mountNFS(volume)
if nfsMount == 'PASSED':
    logging.info('Mounted Nfs Share "%s" in "mount/%s" successfully',\
                    volume['name'], volume['mountPoint'])
   
    #Trying to unmount the share which is in use
    withinMountPoint = UseFileInMountPoint(volume)  
    if 'FAILED' in withinMountPoint:
        endTime = ctime()
        logAndresult(testcase, 'FAILED', withinMountPoint[1], startTime, endTime)
else:
    endTime = ctime()
    msg = 'failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

if withinMountPoint[1] == True:
    time.sleep(5) #before killing vdbench process waiting for 5s
    kill_process(volname)

## collecting the results
endTime = ctime()
resultCollection('Unmount the mount point when the file from the mount point '\
        'is in use, testcase is', ['PASSED',' '], startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
logging.debug('%s, testcase PASSED', testcase)

# unmounting the share
##some m/c takes time to umount so putting some sleep before unmounting
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
            print umount_output
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

## deleting volume
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

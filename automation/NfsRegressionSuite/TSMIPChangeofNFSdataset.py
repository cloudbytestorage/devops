import sys
import os
import time
import json
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, \
    executeCmd, sendrequest, umountVolume
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new
from utils import logAndresult
from tsmUtils import listTSMWithIP_new, get_tsm_info, updateTsmIP
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_vdbench

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

###steps followed for this testcase....
#1. mount the nfs share 
#2. change the tsm ip and try to access old tsm ip
#3. old mount point shd be unavailable and then umount it
#4. mount again with new tsm ip and run vdbench on that share

testcase = 'Change Tenant IP of the NFS dataset'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'Parameters are not correct, please provide as follows'
    print 'python TSMIPChangeOfNFSdataset.py conf.txt vdbench_file_to_run'
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

if len(sys.argv) >= 3:
    VdbFile = sys.argv[2]
    file_exists = os.path.isfile('./vdbench/templates/%s' %VdbFile)
    if file_exists == False:
        VdbFile = 'filesystem_nfs' #taking this as default file to run vdbench
        print 'Given vdbench file does not exists in the vdbench template '\
                'folder, Hence taking the file "%s"' %(VdbFile)
        logging.debug('Given vdbench file does not exists in the vdbench '\
                 'template folder, Hence taking the file "%s"', (VdbFile))
else:
    VdbFile = 'filesystem_nfs'

logging.info('standard file taken to run vdbench is "%s"', VdbFile)

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
confName = sys.argv[1]
tsmIP = config["ipVSM2"]
print tsmIP
tsmChangeIP = config["extra_VSMip"]
print tsmChangeIP
NfsClient = 'All'

def nfsShareMount(volume):
       ### Mounting NFS shares
    logging.info("Mounting NFS Shares '%s'",volume['name'])
    nfsMount = mountNFS(volume)
    if nfsMount == 'PASSED':
        logging.info('Mounted Nfs Share "%s" successfully', volume['name'])
    else:
        endTime = ctime()
	msg = 'failed to mount NFS share "%s"' %volume['name']
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
        
def nfsShareUnmount(volume):
    ### Unmounting NFS shares
    logging.info('Unmounting NFS shares "%s"', volume['name'])
    nfsUnmount = umountVolume(volume)
    if nfsUnmount == 'PASSED':
        logging.info('NFS share "%s" unmounted successfully', volume['name'])
    else:
        endTime = ctime()
        msg = 'failed to Unmount NFS share "%s"' %volume['name']
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)

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

vol = {'name': 'TsmNewIPVol', 'tsmid': tsmID, 'datasetid': datasetID, \
                'protocoltype': 'NFS', 'iops': 400}
result = create_volume(vol, stdurl)
logging.debug('%s', result)
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
volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
                volname, volid, vol_mntPoint)

startTime = ctime()
logging.info('Adding NFS client "%s" to volume "%s"', \
                NfsClient, vol['name'])
addClient = addNFSclient(stdurl, volid, NfsClient)
if addClient[0] == 'PASSED':
    print 'Added NFS client "%s" to volume "%s"' %(NfsClient, volname)
    logging.info('Added NFS client "%s" to volume "%s"', NfsClient, volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

#logging.info('Pinging the TSMIP "%s" to check its connectivity', tsmIP)
#os.system("ping -c 4 %s" %tsmIP) 

volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                    'name' : volname}

startTime = ctime()
#mounting nfs share
logging.info('Mounting Nfs share before TSM IP cahnge')
nfsMount1 =  nfsShareMount(volume)

logging.info('Calling function to update TSMIP')
tsmUpdate = updateTsmIP(tsmID, tsmChangeIP, stdurl)
if tsmUpdate[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', tsmUpdate[1], startTime, endTime)
else:
    print tsmUpdate[1]
    logging.debug('TSM is updated with new IP "%s"', tsmChangeIP)

logging.info('Pinging the old TSMIP "%s" to check its connectivity '\
                'after updating with new TSMIP', tsmIP)
ping = os.system("ping -c 4 %s" %tsmIP)
if ping != 0:
    logging.warning('Mount point not available after  TSM IP change')
    print "mount point is not available after Tsm IP change"

startTime = ctime()
#unmounting nfs share
logging.info('Unmounting Nfs share with old Tsm Ip')
nfsUnmount1 =  nfsShareUnmount(volume)

volume = {'TSMIPAddress' : tsmChangeIP, 'mountPoint': vol_mntPoint,\
                    'name' : volname}

logging.info('mounting NFS share after TSMIP is updated')
#Again mounting nfs share after chaning tsm ip
logging.info('Mounting Nfs after TSM IP cahnge')
nfsMount2 =  nfsShareMount(volume)

logging.info('After mounting nfs share running vdbench on that')
exe = executeVdbenchFile(volume, VdbFile) 
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('waiting for 2mins for vdbench to run....')
    time.sleep(120) #waiting for 2mins for vdbench to run
else:
    logging.debug('vdbench dint start')

startTime = ctime()
logging.info('Checking whether vdbench is still running or not....')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_vdbench()
    time.sleep(2)
    check_vdbench = is_vdbench_alive(volname)
    if check_vdbench:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_vdbench()
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

endTime = ctime()
resultCollection('Change Tenant IP of the NFS dataset'\
            'testcase is', ['PASSED',' '], startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

##some m/c takes time to umount so putting some sleep before unmounting
time.sleep(2)
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

##changing back to old IP
logging.info('Changing back TSM IP to old IP')
tsmUpdate = updateTsmIP(tsmID, tsmIP, stdurl)
if tsmUpdate[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', tsmUpdate[1], startTime, endTime)
else:
    print tsmUpdate[1]
    logging.debug('TSM is updated with old IP "%s"', tsmIP)

logging.info('Pinging the old TSMIP "%s" to check its connectivity '\
                'after updating with old TSMIP', tsmIP)
ping = os.system("ping -c 2 %s" %tsmIP)
if ping != 0:
    print "Tsm with old IP '%s' not available after changing baxk" %tsmIP
    logging.debug("Tsm with old IP '%s' not available after changing back", \
            tsmIP)
else:
    print "Tsm with old IP '%s' is available after Tsm IP change" %tsmIP
    logging.debug("Tsm with old IP '%s' is available after changing back", \
            tsmIP)

logging.info('Deleting volume "%s"', volume['name'])
deleteVolume =  delete_volume(volid, stdurl)
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

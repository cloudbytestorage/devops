import sys
import os
import json
import time
import subprocess
from time import ctime
from tabulate import tabulate #using this to represent o/p in form of table
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
        delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, mountPointDetails
from vdbenchUtils import is_vdbench_alive, kill_process

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

testcase = 'Large File Read & Write across NFS Volumes(20GB)'
logging.info('----Start of testcase "%s"----\n', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsLargeFileReadWrite.py conf.txt  vdbench_file_to_run"
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()

VdbFile = 'filesystem_nfs'
#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]
ClientIP = 'all'

#---------------------------METHODS-----------------------------------------------------
# to overwrite size for the given vdbench file....
def writingVDBfile(volume, vdbFile, vol_size):
    executeCmd('yes | cp -rf vdbench/templates/%s vdbench/%s' %(vdbFile, volume['name']))
    logging.info('copying vdbench/templates/%s file to vdbench as "%s"', \
                    vdbFile, volume['name'])
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    old_size = getoutput("cat vdbench/%s | grep ',size=' | cut -d '=' -f 7" \
            %(volume['name']))
    old_size = old_size[0].strip('\n')
    vdb_path = 'vdbench/%s' %volume['name']
    res = executeCmd("sed -i 's/%s/%s/' %s " \
        %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), vdb_path))
    res = executeCmd("sed -i 's/%s/%s/' %s " \
        %(old_size.replace('/', '\/'), vol_size.replace('/', '\/'), vdb_path))
    logging.info('executing vdbench....')
    out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' \
            %(volume['name']))
#*******************************************************************************
# create volume, add nfs client and getting required details....
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
#*****************************************************************************
# to delete volume
def delete_dataset(volname, volid, stdurl):
    deleteVolume =  delete_volume(volid, stdurl)
    if 'PASSED' in deleteVolume:
        print 'Volume \"%s\" Deleted successfully' %(volname)
        logging.debug('Volume \"%s\" Deleted successfully', volname)
    else:
        print 'Failed to deleted the volume \"%s\"' %(volname)
        logging.debug('Failed to deleted the volume \"%s\"',volname)
#******************************************************************************
# to unmount share
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

# creating volume and mounting the same
vol1 = {'name': 'nfslargeVol1', 'tsmid': tsmID, 'quotasize': '25G', \
    'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 200}

final_result1 = addVol_client_Mount(vol1, stdurl, tsmID, tsmName, ClientIP)

# creating another volume and mounting the same
vol2 = {'name': 'nfslargeVol2', 'tsmid': tsmID, 'quotasize': '25G', \
        'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 200}
final_result2 = addVol_client_Mount(vol2, stdurl, tsmID, tsmName, ClientIP)

# writting 20GB of data 
vol_size = '20G'
vol_size1 = vol_size.strip('G')
vol_size1 = int (vol_size1)*1024
exe = writingVDBfile(final_result1[0], VdbFile, vol_size)
check_vdbench = is_vdbench_alive(vol1['name'])

mount_point1 = getoutput('mount | grep %s | awk \'{print $3}\'' \
                %(final_result1[0]['mountPoint']))
mount_point1 = mount_point1[0].strip('\n')

startTime = ctime()
while True:
    mountDetails = mountPointDetails('-m', mount_point1)
    Used = mountDetails[2]
    if int(Used) >= int(vol_size1):
	logging.info('Vdbench has filed large file of 20G, waiting for 30s')
        time.sleep(30)
        break
    else:
        check_vdbench = is_vdbench_alive(vol1['name'])
        if check_vdbench:
            continue
        else:
            endTime = ctime()
            msg = 'vdbench has stopped unexpectedly, File filed by vdbench '\
                    'was : %sM' %Used
            logAndresult(testcase, 'FAILED', msg, startTime, endTime)

check_vdbench = is_vdbench_alive(vol1['name'])
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_process(vol1['name'])
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

mount_point2 = getoutput('mount | grep %s | awk \'{print $3}\'' \
                %(final_result2[0]['mountPoint']))
mount_point2 = mount_point2[0].strip('\n')

# copying data from one share to another
logging.info('Copying file from one share to another')
startTime = ctime
copy_large = executeCmd('yes | cp -rf %s/* %s' %(mount_point1, mount_point2))
if copy_large[0] == 'FAILED':
    endTime = ctime()
    msg = 'Failed to copy data from one volume to other'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
else: 
    logging.debug('copying of  data from one share to other was successful')

# verifying whether data copy was successful or not
mountDetails1 = mountPointDetails('-h', mount_point1)
Used1 = mountDetails1[2]
mountDetails2 = mountPointDetails('-h', mount_point1)
Used2 = mountDetails2[2]

startTime = ctime()
if Used1 == Used2:
    logging.debug('Both shares used size is same, copy was successfull')
else:
    endTime = ctime()
    msg = 'Both shares used size is different, copy didnt happen properly'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

# collecting result
endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
        startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
logging.debug('%s, testcase PASSED', testcase)

# clearing the configurations....
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


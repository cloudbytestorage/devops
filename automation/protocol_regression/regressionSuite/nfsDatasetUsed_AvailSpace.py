import sys
import os
import json
import time
import subprocess
from time import ctime
#from tabulate import tabulate #using this to represent o/p in form of table
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
        delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, mountPointDetails
from vdbenchUtils import is_vdbench_alive, kill_process

TC_name = sys.argv[0]
TC_name = TC_name.replace('.py','.log')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
            filename='logs/'+TC_name,filemode='a',level=logging.DEBUG)

##steps followed for this testcase....
#1. mount the NFS share
#2. collecting initial data like : used, available space, use percentage
#3. running vdbench 
#4. after filling some data verifying used , available space, use percentage

testcase = 'Verify the usedspace and available space of the mountpoint by '\
        'adding files to the mountpoint'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsDatasetUsed_AvailSpace.py conf.txt  vdbench_file_to_run"
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

###-----------------Methods------------------------------------------------
## passing size in vdbench file

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
#--------------------------------------------------------------------------

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

## Creating volume and getting required details
vol = {'name': 'NfsVolInfo', 'tsmid': tsm_id, 'datasetid': dataset_id, \
            'protocoltype': 'NFS', 'iops': 100}
startTime = ctime()
result = create_volume(vol, stdurl)
if result[0] == 'FAILED':
    endTime = ctime()
    print result
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

## adding nfs client as All
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'PASSED':
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}

## mounting nfs share
startTime = ctime()
logging.info("Mounting NFS Share '%s'", volname)
nfsMount = mountNFS(volume)
if nfsMount == 'PASSED':
    logging.info('Mounted Nfs Share "%s" in "mount/%s" successfully',\
                        volume['name'], volume['mountPoint'])
else:
    endTime = ctime()
    msg = 'failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

# getting mountPoint path 
mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
            %(volume['mountPoint']))
mount_point = mount_point[0].strip('\n')

# getting mountPoint details like size, used, available & so on
mountDetails = mountPointDetails("-h", mount_point)
if mountDetails[0] == 'FAILED':
    logAndresult(testcase, 'FAILED', mountDetails[1], startTime, endTime)
totalSize, usedSize, availableSize, usepercentage = mountDetails[1], \
        mountDetails[2], mountDetails[3], mountDetails[4]


print 'Before adding file(s), the used space is' 
space_data = [[totalSize, usedSize, availableSize, usepercentage]]
#initial_data = tabulate(space_data, \
#        headers=['Size', 'Used', 'Avail', 'Use%'], tablefmt="psql") 

#returning o/p in the form of table
#print initial_data
#logging.info('Before adding file(s), the  space details is shown below')
#logging.debug('\n%s', initial_data)

# filing 5GB of data into the share
vol_size = '5G'
vol_size1 = vol_size.strip('G')
vol_size1 = int (vol_size1)*1024
exe = writingVDBfile(volume, VdbFile, vol_size)
check_vdbench = is_vdbench_alive(volname)
while True:
    mountDetails = mountPointDetails('-m', mount_point)
    Used = mountDetails[2]
    if int(Used) >= int(vol_size1):
        time.sleep(10)
        break
    else:
        check_vdbench = is_vdbench_alive(volname)
        if check_vdbench:
            continue
        else:
            logging.debug('vdbench has stopped unexpectedly....')
            print 'vdbench has stopped unexpectedly'
            break

check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_process(volname)
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

## after filling data collecting mountPoint details
print 'After adding file(s), the used space is' 
mountDetails = mountPointDetails('-h',mount_point)
totalSize, usedSize, availableSize, usepercentage = mountDetails[1], \
    mountDetails[2], mountDetails[3], mountDetails[4]
space_data2 = [[totalSize, usedSize, availableSize, usepercentage]]
#later_data = tabulate(space_data2, \
#        headers=['Size', 'Used', 'Avail', 'Use%'], tablefmt="psql") 
#returning o/p in the form of table..
#print later_data
#logging.info('After adding file(s), the space details is shown below')
#logging.debug('\n%s', later_data)

# collecting results
endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED',' '], \
        startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
logging.debug('%s, testcase PASSED', testcase)

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

import os
import sys
import json
from time import ctime
import time
import subprocess
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    get_ntwInterfaceAndIP, sendrequest, passCmdToController
from volumeUtils import get_volume_info, listVolumeWithTSMId_new, \
    create_volume, addNFSclient, delete_volume, deleteNFSclient
from utils import logAndresult
from tsmUtils import get_tsm_info, listTSMWithIP_new
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_vdbench

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

###steps followed for this testcase....
#1. mount Nfs share and run IOs
#2. while Ios are running remove client from export 
#3. verifying on controller side in /etc/exports
#4. verify if IOs are running or not

testcase = 'Remove clients from exports while IOs are running'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python removeClientFromexports.py conf.txt vdbench_file_to_run"
    logging.debug('----Ending script because of parameter mismatch----\n')
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
tsmIP = config["ipVSM2"]

startTime = ctime()
logging.info('Getting local client IP')
localClientIP = get_ntwInterfaceAndIP(tsmIP)
if localClientIP[0] == 'FAILED':
    endTime = ctime()
    print localClientIP[1]
    logAndresult(testcase, 'BLOCKED', localClientIP[1], startTime, endTime)
else:
    localClientIP = localClientIP[1]
    logging.debug('local client IP : "%s"', localClientIP)

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

vol = {'name': 'removeClientNFSVol', 'tsmid': tsmID, \
        'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 400}
startTime = ctime()
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
volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
                volname, volid, vol_mntPoint)

startTime = ctime()
addClient = addNFSclient(stdurl, volid, localClientIP)
if addClient[0] == 'PASSED':
    print 'Added NFS client "%s" to volume "%s"' \
                %(localClientIP, volname)
    logging.info('Added NFS client "%s" to volume "%s"', \
                    localClientIP, volname)
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
    msg = 'failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

logging.info('Running vdbench  by using file')
exe = executeVdbenchFile(volume, VdbFile)
logging.info('waiting for 1min for vdbench to run....')
time.sleep(60) #waiting for 60s for vdbench to run

nodeIP = tsmList[1][0].get('controlleripaddress')
startTime = ctime()
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('vdbench is running')
    logging.info('While IOs are running removing client from exports')
    startTime = ctime()
    delClient = deleteNFSclient(stdurl, volid, localClientIP)
    if delClient[0] == 'PASSED':
        print 'Deleted NFS client "%s" from volume "%s"' \
                    %(localClientIP, volume['name'])
        logging.debug('Deleted NFS client "%s" from volume "%s"', \
                        localClientIP, volume['name'])
        
        #login to node and verify exports
        logging.info('Logging to node and verifying exports....')
        cmd1 = "jls | grep %s | awk '{print $4'} | cut -d '/' -f 3" %(tsmIP)
        get_jid = passCmdToController(nodeIP, 'test', cmd1).strip()
        if not get_jid:
            msg = 'Not able to get jID for given tsm IP "%s"' %tsmIP
            print msg
            logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
        else:
            logging.debug('JID of tsm "%s" : %s', tsmIP, get_jid)
        cmd2 = "cat /tenants/%s/etc/exports" %(get_jid)
        exports =  passCmdToController(nodeIP, 'test', cmd2).strip()
        logging.info('Clients in exports is as below....')
        logging.debug('%s', exports)
        if not localClientIP in exports:
            print 'Successfully deleted nfs client "%s" from exports '\
                    'while IOs are running' %localClientIP
            logging.debug('Successfully deleted nfs client "%s" from exports '\
                    'while IOs are running', localClientIP)
        else:
            endTime = ctime()
            msg = 'Failed to delete client "%s" from exports '\
                    'while IOs are running' %localClientIP
            logAndresult(testcase, 'FAILED', msg, startTime, endTime)

        time.sleep(5) #after deleting client waiting fo 5s 
        logging.info('After deleting client checking whether vdbench is '\
                'still running or not')
        check_vdbench = is_vdbench_alive(volname)
        if not check_vdbench:
            msg = 'Vdbench has stopped running after deleting client'
            endTime = ctime()
            logAndresult(testcase, 'FAILED', msg, startTime, endTime)
        logging.debug('After adding client vdbench is still running')
    else:
        endTime = ctime()
        print delClient[1]
        logAndresult(testcase, 'FAILED', delClient1[1], startTime, endTime)

else:
    endTime = ctime()
    msg = 'Vdbench has stopped unexpectedly....'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

endTime = ctime()
resultCollection('Remove clients from exports while IOs are running, '\
        'testcase is', ['PASSED',' '], startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

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



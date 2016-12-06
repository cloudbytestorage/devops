import os
import sys
import json
import time
import subprocess
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume, mountNFS, \
    executeCmd, resultCollection, resultCollectionNew, sendrequest, \
    configFile
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new
from tsmUtils import get_tsm_info, listTSMWithIP_new
from utils import  logAndresult

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

###steps followed for this testcase
#1. create volume and mount the volume with soft/hard mount

testcase = 'Nfs soft/hard mount'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv)<3:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsSoftmount.py conf.txt soft/hard"
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

if not (sys.argv[2].lower() == 'soft' or sys.argv[2].lower() == 'hard'):
    print "Parameter given  for mount type is wrong. "\
            "Please specify as shown below"
    print "python nfsSoftmount.py conf.txt soft/hard"
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]
mountType = sys.argv[2]
ClientIP = 'all'

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

					
vol = {'name': 'NFS%sMount' %(mountType), 'tsmid': tsmID, \
        'datasetid': datasetID, 'protocoltype': 'NFS', 'iops': 500}
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
executeCmd('mkdir -p mount/%s' %(volume['mountPoint']))
mountResult = executeCmd('mount -o mountproto=tcp,sync,%s %s:/%s '\
        'mount/%s' %(mountType, volume['TSMIPAddress'], \
        volume['mountPoint'], volume['mountPoint']))
if mountResult[0] == 'PASSED':
    logging.info('Mounted Nfs Share "%s" with mount option "%s" '\
            'successfully', volname, mountType)
    print 'NFS volume \"%s\" mounted successfully' \
            %(volume['name'])
    print'\nExecuting command "nfsstat -m" to verify mount'
    logging.info("Executing 'nfsstat -m' cmd to verify mount")
    mountStatus = os.popen('nfsstat -m').read()
    mountStatus = mountStatus.strip()
    print mountStatus
    logging.debug('Output of "nfsstat -m" cmd is shown below:\n %s', \
            mountStatus)
else:
    endTime = ctime()
    print mountResult[1]
    #print 'NFS volume \"%s\" failed to mount' %(volume['name'])
    #msg = 'failed to mount NFS share "%s"' %volume['name']
    logAndresult(testcase, 'FAILED', mountResult[1], startTime, endTime)
   
endTime = ctime()
resultCollection('NFS soft/hard mount, testcase is', ['PASSED', ' '],\
                startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

time.sleep(2) #before unmounting waiting for 2s
logging.info("UnMounting NFS Share '%s'", volume['name'])
umount = umountVolume(volume)
if umount == 'PASSED':
    logging.debug('Volume "%s" umounted successfully', volume['name'])
else:
    logging.debug('Failed to umount the volume "%s"', volume['name'])

logging.info('Deleting volume "%s"', volume['name'])
deleteVolume =  delete_volume(volid, stdurl)
if deleteVolume[0] == 'PASSED':
    print 'Volume \"%s\" Deleted successfully' %(volume['name'])
    logging.debug('Volume \"%s\" Deleted successfully', volume['name'])
else:
    print 'Failed to deleted the volume \"%s\"' %(volume['name'])
    logging.debug('Failed to deleted the volume \"%s\"', volume['name'])

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)


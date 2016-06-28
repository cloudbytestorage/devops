import sys
import os 
import json
import time
import subprocess
import logging
from time import ctime
from volumeUtils import get_volume_info, listVolumeWithTSMId_new, \
        create_volume, addNFSclient, delete_volume
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    getControllerInfoAppend
from utils import logAndresult
from tsmUtils import get_tsm_info, listTSMWithIP_new

logging.basicConfig(format='%(asctime)s %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)


testcase = 'Verify NFS share mount/umount alerts(devd logs)'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows...\n'
    print 'python NFSAlerts.py conf.txt'
    logging.debug('----Ending script because of parameter mismatch----')
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

conf = configFile(sys.argv)
apikey = get_apikey(conf)
stdurl = get_url(conf, apikey[1])
tsmIP = conf['ipVSM2']

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

vol = {'name': 'nfsMountUmount', 'tsmid': tsmID, 'datasetid': datasetID, \
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
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'PASSED':
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"',volname)
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

nodeIP = tsmList[1][0].get('controlleripaddress')
passwd = "test"
command = 'cat /var/log/devd.log | grep %s | grep -w  mount' \
        %(volume['mountPoint'])
logs = getControllerInfoAppend(nodeIP, passwd, command, "results/result.csv")
logging.debug('Mount alerts from devd.log is: %s', logs)
print logs

#unmounting the NFS volume
time.sleep(10)
nfsUnmount = umountVolume_new(volume)
if nfsUnmount == 'FAILED':
    endTime = ctime()
    msg = 'failed to Unmount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
else:
    logging.debug('Volume "%s" umounted successfully', volume['name'])

command = 'cat /var/log/devd.log | grep %s | grep -w  unmount' \
        %(volume['mountPoint'])

logs = getControllerInfoAppend(nodeIP, passwd, command, "results/result.csv")
logging.debug('Mount alerts from devd.log is: %s', logs)
print logs

endTime = ctime()
resultCollection('NFS share mount/umount alerts(devd logs), '\
    'testcase is', ['PASSED',' '],startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

delvol = delete_volume(volid, stdurl)
if 'FAILED' in delvol:
    print 'Failed to deleted the volume \"%s\"' %(volume['name'])
    logging.debug('Failed to deleted the volume \"%s\"', \
                        volume['name'])
else:
    print 'Volume \"%s\" Deleted successfully' %(volume['name'])
    logging.debug('Volume \"%s\" Deleted successfully', \
                    volume['name'])

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)


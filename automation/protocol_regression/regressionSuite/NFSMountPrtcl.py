import sys
import json
import requests
import time
import subprocess
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new, get_tsm_info
from cbrequest import  executeCmd, configFile, get_apikey, get_url, \
    nfsMountPrtcl, resultCollection, umountVolume, resultCollectionNew
from volumeUtils import create_volume, delete_volume, addNFSclient, \
    listVolumeWithTSMId_new, get_volume_info
from utils import  logAndresult

logging.basicConfig(format = '%(asctime)s %(message)s',\
        filename = 'logs/automation_execution.log',\
                filemode = 'a', level = logging.DEBUG)

testcase = 'Specify the NFS mount to use the TCP/UDP protocol'
logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv)<3:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsSoftmount.py conf.txt soft/hard"
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

if not (sys.argv[2].lower() == 'tcp' or sys.argv[2].lower() == 'udp'):
    print "Parameter given  for mount type is wrong. "\
            "Please specify as shown below"
    print "python nfsSoftmount.py conf.txt soft/hard"
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
prtcl = sys.argv[2]
tsm_ip = config['ipVSM1']

startTime =ctime()
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsm_ip)
tsm_list = listTSMWithIP_new(stdurl, tsm_ip)
if tsm_list[0] == 'PASSED':
    logging.info('TSM present with the given IP "%s"', tsm_ip)
else:
    endTime = ctime()
    print 'Not able to list TSMs due to: ' + tsm_list[1]
    logAndresult(testcase, 'BLOCKED', tsm_list[1], startTime, endTime)

logging.info('Getting tsm_name, tsm_id, and dataset_id...')
get_tsmInfo = get_tsm_info(list_tsm[1])
tsm_id, tsm_name, dataset_id = get_tsmInfo[0], get_tsmInfo[1], get_tsmInfo[2]
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
                    tsm_name, tsm_id, dataset_id)

volume1 = {'name': 'NFS%sPrtcl'%prtcl, 'tsmid': tsm_id, \
        'datasetid': dataset_id, 'protocoltype': 'NFS'}
startTime = ctime()
create_vol = create_volume(volume1, stdurl)
if create_vol[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', create_vol[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(volume1['name'])

logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
if vol_list[0] == 'PASSED':
    logging.info('Volumes present in the TSM "%s"', tsm_name)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', vol_list[1], startTime, endTime)

volume_name = volume1['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
            volname, volid, vol_mntPoint)

startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'PASSED':
    print 'Added NFS client "all" to volume "%s"' %(volname)
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                    'name' : volname}
#mounting with one of the protocol....
mount_result = nfsMountPrtcl(prtcl, volume)
if mount_result[0] == 'PASSED':
    print 'volume is mounted succesfully with %s protocol' %prtcl
    logging.debug('volume is mounted succesfully with %s protocol', prtcl)
else:
    msg = 'Failed to mount nfs share with %s protocol' %prtcl
    endTime = ctime()
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED', ' '],\
                startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

time.sleep(2) #before unmounting waiting for 2s
logging.debug('Unmounting Nfs share %s', (volname))
nfsUmount2 = umountVolume(vol)
if nfsUmount2 == 'PASSED':
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

import sys
import os
import json
import logging 
import time
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume, mountNFS, executeCmd, \
    resultCollection, resultCollectionNew, sendrequest, configFile
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, \
    addNFSclient, delete_volume, listVolumeWithTSMId_new
from utils import logAndresult


TC_name = sys.argv[0]
TC_name = TC_name.replace('.py','.log')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
                    filename='logs/'+TC_name,filemode='a',level=logging.DEBUG)

##steps followed for this testcase...
#1. enabled readonly 
#2. mount the share, try to create directory
#3. creation shd fail

testcase = 'Enable NFS on a Read-only Dataset and '\
        'try adding files to that after mounting'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'wrong arguments'
    print 'python nfsReadOnlyDataset.py conf.txt'
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()

#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]

###--------------------------Method--------------------------------------
##method for setting readonly
###operation = true/false
def set_readonly(vol_id, operation, stdurl):
    logging.info('Setting read only method...')
    querycommand = 'command=updateFileSystem&id=%s&readonly=%s' \
            %(vol_id, operation)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for setting readonly: %s', str(rest_api))
    response_read = sendrequest(stdurl,querycommand)
    data = json.loads(response_read.text)
    logging.debug('response for ready only: %s', str(data))
    if 'errorcode' in str(data['updatefilesystemresponse']):
        errormsg = str(data['updatefilesystemresponse'].get('errortext'))
        print errormsg
        return ['FAILED', errormsg]
    else:
        return ['PASSED', 'Successfully updated readonly']
##---------------------------------------------------------------------------

#list Tsm and getting required details
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

##create volume and getting required details
startTime = ctime()
vol = {'name': 'NfsReadOnly', 'tsmid': tsm_id, 'datasetid': dataset_id, \
            'protocoltype': 'NFS', 'iops': 100}
result = create_volume(vol, stdurl)
if 'FAILED' in result:
    endTime = ctime()
    print result
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(vol['name'])

startTime = ctime()
logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
volList = listVolumeWithTSMId_new(stdurl, tsm_id)
if 'PASSED' in volList:
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

## adding nfs client
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if 'PASSED' in addClient:
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}

# setting readonly state as yes for the volume
startTime = ctime()
operation = 'true'
readonly = set_readonly(volid, operation, stdurl)
if 'FAILED' in readonly:
    endTime = ctime()
    logAndresult(testcase, 'FAILED', readonly[1], startTime, endTime)
else:
    logging.debug('Successfully updated readonly for the volume "%s"' ,volname)
    print readonly[1]

# mounting the share
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

#trying to create directory on readonly enabled share, and verifying the same
startTime = ctime()
logging.info('Verifying readonly property....')
writefile = executeCmd('mkdir -p mount/%s/newFolder' %(volume['mountPoint']))
if (writefile[0] == 'PASSED' and operation == 'true'):
    endTime = ctime()
    msg = 'Unexpected result: Directory "newFolder" created successfully in '\
            'mountPoint with readonly enabled'
    print msg
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
elif (writefile[0] == 'FAILED' and operation == 'true'):
    msg =  'Expected Result' + writefile[1] 
    print msg
    logging.debug('%s', msg)

# collecting results
endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
        startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

# unmounting the share
time.sleep(2) #before unmount sleeping for 2s
startTime = ctime()
logging.info("UnMounting NFS Share '%s'", volume['name'])
umount = umountVolume(volume)
if umount == 'PASSED':
    logging.debug('Volume "%s" umounted successfully', volume['name'])

else:
    logging.debug('Failed to umount the volume "%s"', volume['name'])

# deleting the volume
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

logging.info('----Completed the testcase "%s"----', testcase)
print ('----End of testcase "%s"----' %testcase)

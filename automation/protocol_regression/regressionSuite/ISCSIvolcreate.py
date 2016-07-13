import sys
import json
import logging
import time
from time import ctime
#from tabulate import tabulate
from volumeUtils import create_volume, delete_volume, listVolumeWithTSMId_new, \
        get_volume_info
from tsmUtils import listTSMWithIP_new, get_tsm_info
from cbrequest import get_apikey, get_url, resultCollection, configFile, \
        resultCollectionNew, getControllerInfoAppend
from utils import logAndresult

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
    'automation_execution.log', filemode = 'a', level = logging.DEBUG)

testcase = "Create a LUN by editing the multiple attributes while creation"

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows..'
    print 'python ISCSIvolcreate.py conf.txt'
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
else:
    endTime = ctime()
    print 'Not able to list Tsm  "%s" due to: ' \
            %(tsmIP) + tsmList[1]
    logAndresult(testcase, 'BLOCKED', tsmList[1], startTime, endTime)

get_tsmInfo = get_tsm_info(tsmList[1])
tsmID = get_tsmInfo[0]
tsmName = get_tsmInfo[1]
datasetID = get_tsmInfo[2]
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
            tsmName, tsmID, datasetID)
path = tsmList[1][0]['storageBuckets'][0]['path']

volume = {'name': 'iscsiVolcreate', 'tsmid': tsmID, 'datasetid': datasetID, \
        'protocoltype': 'ISCSI', 'iops': 123, 'compression': 'on', \
        'recordsize': '64k', 'latency': 25}

startTime = ctime()
result = create_volume(volume, stdurl)
if result[0] == 'PASSED':
    print "Volume '%s' created successfully" %(volume['name'])
else:
    endTime = ctime()
    print result[1]
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)

startTime = ctime()
volList = listVolumeWithTSMId_new(stdurl, tsmID)
if volList[0] == 'PASSED':
    logging.info('Volumes present in the TSM "%s"', tsmName)
else:
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
                            %(tsmName) + volList[1]
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = volume['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_quota = get_volInfo[1], get_volInfo[2], get_volInfo[6]
logging.debug('volname: %s, volid: %s', volname, volid)

nodeIP = tsmList[1][0].get('controlleripaddress')
passwd = "test"
command = 'zfs get volsize,compression,volblocksize  %s/%s' %(path,volume['name'])
logs = getControllerInfoAppend(nodeIP, passwd, command, \
        'logs/automation_execution.log')

print 'Details given during volume creation'
creation_details = [['iops', volume['iops']], ['quota', vol_quota],\
    ['compression', volume['compression']],['recordsize', volume['recordsize']]]
#creation_table = tabulate(creation_details, headers=['Property', 'value'], \
#        tablefmt="psql")
#print creation_table
#logging.info('Details given during volume creation')
#logging.debug('\n%s', creation_table)

print 'verifying the parameters given during volume creation using '\
        '"%s" cmd in controller' %command
logging.info('verifying the parameters given during volume creation using '\
            '"%s" cmd in controller', command)
print logs
logging.debug('\n%s', logs)

endTime = ctime()
resultCollection('%s, testcase is' %testcase, ['PASSED',' '], \
                startTime, endTime)
resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

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


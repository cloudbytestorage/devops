import os
import sys
import json
from time import ctime
import time
import subprocess
import logging
from tsmUtils import listTSMWithIP_new
from utils import *
from cbrequest import *
from volumeUtils import *


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
        filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)
logging.info('--------Starting the script for testcase "Mount 20 iscsi dataset, '\
        'run IO overnight, unmount and mount"---------')


if len(sys.argv)<2:
    print "Arguments are not correct, Please provide as follows..."
    print "python ISCSIOvernightio.py conf.txt  vdbench_file"
    logging.debug('------Ending script because of parameter mismatch--------')
    exit()

startTime = ctime()
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = tsmip = config['ipVSM2']
VdbFile =  'moreVol'

def verify_getDiskAllocatedToISCSI(result, mountpoint):
     if result[0] == 'PASSED' and mountpoint in str(result[1]):
         logging.debug('iscsi logged device... %s', result[1][mountpoint])
         return result[1][mountpoint]
     logging.error('Not able to get iscsi legged device')

##for more mountpoint within a single file
def writingVDBfile(x, volume):
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory%s' %x
    new_str = output[0].rstrip('\n')
    path = 'vdbench/%s' %vdbNewFile
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), path ))


def iscsiMount():
    discover = discover_iscsi_lun(tsmip, iqnName)
    if 'FAILED' in discover:
        result = ['FAILED', discover]
        return result[1]
    login = iscsi_login_logout(iqnName, tsmip, 'login')
    result = getDiskAllocatedToISCSI(tsmip,volume1['mountPoint'])
    device = verify_getDiskAllocatedToISCSI(result, volume1['mountPoint'])
    #device = get_iscsi_device() 
    #device = device[1]
    print device
    if 'FAILED' in device:
        result = ['FAILED', device]
        return result[1]

    fs =  execute_mkfs(device, 'ext3')
    if 'FAILED' in fs:
        result = ['FAILED', fs]
        return result[1]

    mountOutput =  mount_iscsi(device, volume1['mountPoint'])
    if 'FAILED' in mountOutput:
        result = ['FAILED', mountOutput]
        return result[1]
    result = ['PASSED', ""]
    return result

def umountLogout():
    unmountISCSI = umountVolume(volume1)
    if "FAILED" in unmountISCSI:
        result = ['FAILED', unmountISCSI]
        return result[1]
    logout = iscsi_login_logout(iqnName, tsmIP, 'logout')
    result = ['PASSED', '']
    return result


TSM = listTSMWithIP_new(stdurl, tsmip)
if 'PASSED' in TSM:
    logging.info('TSM present with the given IP "%s"', tsmip)
    pass
else:
    endTime = ctime()
    print 'Not able to list TSMs due to: ' + TSM[1]
    logging.debug('ISCSI login/logout alerts(devd logs), '\
                'testcase is Blocked due to %s', TSM[1])
    logging.debug('-------Ending script because this testcase is blocked------')
    resultCollection('ISCSI login/logout alerts(devd logs), '\
        'testcase is', ['BLOCKED',' '], startTime, endTime)
    exit()

logging.info('Getting tsm_name, tsm_id, and dataset_id...')
tsmid = TSM[1][0].get('id')
tsmName = TSM[1][0].get('name')
datasetid = TSM[1][0].get('datasetid')
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
        tsmName, tsmid, datasetid)
logging.info('Getting account Name and ID')
accountName = TSM[1][0].get('accountname')
account_id = TSM[1][0].get('accountid')
logging.debug('account_Name: %s, account_id: %s', accountName, account_id)


for x in range(1, 21):
    vol = {'name': 'IscsiVol%d' %x, 'tsmid': tsmid, 'datasetid': datasetid, \
            'protocoltype': 'ISCSI', 'iops': 100}
    result = create_volume(vol, stdurl)
    if "FAILED" in result:
        endTime = ctime()
        print result
        logging.debug('running IOs overnight on more iscsi dataset, '\
                'testcase is Blocked due to %s', TSM[1])
        logging.debug('-------Ending script because this testcase is blocked------')
        resultCollection('running IOs overnight on more iscsi dataset, '\
                'testcase is', ['BLOCKED',' '], startTime, endTime)
        exit()
    else:
        print "Volume '%s' created successfully" %(vol['name'])

logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsmName)
volList = listVolumeWithTSMId_new(stdurl, tsmid)
if 'PASSED' in volList:
    logging.info('Volumes present in the TSM "%s"', tsmName)
    pass
else:
    endTime = ctime()
    print 'Not able to list Volumes in TSM "%s" due to: ' \
            %(tsmName) + volList[1]
    logging.debug('running IOs overnight on more iscsi dataset, '\
            'testcase is Blocked due to %s', TSM[1])
    logging.debug('-------Ending script because this testcase is blocked------')
    resultCollection('running IOs overnight on more iscsi dataset, '\
                'testcase is', ['BLOCKED',' '], startTime, endTime)
    exit()

##vdbench file 
vdbNewFile = 'iscsi20'
executeCmd('yes | cp -rf vdbench/%s vdbench/%s' %(VdbFile, vdbNewFile))

for x in range(1, 21):
    vol1 = {'name' : 'IscsiVol%d' %x}
    for filesystem in volList[1]:
        if filesystem['name'] == vol1['name']:
            volume1 = {'TSMIPAddress' : filesystem['ipaddress'], 'mountPoint': \
                    filesystem['mountpoint'], 'name': filesystem['name']}
            filesystem_name = filesystem['name']
            filesystem_id = filesystem['id']
            iqnName = filesystem['iqnname']
            setGroup = assign_iniator_gp_to_LUN\
                            (stdurl, filesystem_id, account_id, 'ALL')
            imount = iscsiMount()
            if 'FAILED' in imount:
                print imount
                exit()
            writingVDBfile(x, volume1)

logging.info('executing vdbench command')
out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' %vdbNewFile)
vdbench_pid(vdbNewFile)

for x in range(1, 21):
    vol1 = {'name' : 'IscsiVol%d' %x}
    for filesystem in volList[1]:
        if filesystem['name'] == vol1['name']:
            iqnName = filesystem['iqnname']
            volume1 = {'TSMIPAddress' : filesystem['ipaddress'], 'mountPoint': \
                filesystem['mountpoint'], 'name': filesystem['name']}
            iumount = umountLogout()
            print iumount
            if 'FAILED' in iumount:
                exit()

for x in range(1, 21):
    vol1 = {'name' : 'IscsiVol%d' %x}
    for filesystem in volList[1]:
        if filesystem['name'] == vol1['name']:
            iqnName = filesystem['iqnname']
            volume1 = {'TSMIPAddress' : filesystem['ipaddress'], 'mountPoint': \
                filesystem['mountpoint'], 'name': filesystem['name']}
            imount2 = iscsiMount()
            if 'FAILED' in imount2:
                exit()
time.sleep(1)
for x in range(1, 21):
    vol1 = {'name' : 'IscsiVol%d' %x}
    for filesystem in volList[1]:
        if filesystem['name'] == vol1['name']:
            iqnName = filesystem['iqnname']
            volume1 = {'TSMIPAddress' : filesystem['ipaddress'], 'mountPoint': \
                filesystem['mountpoint'], 'name': filesystem['name']}
            filesystem_id = filesystem['id']
            iumount2 = umountLogout()
            if 'FAILED' in iumount2:
                exit()
            setGroup = assign_iniator_gp_to_LUN\
                (stdurl, filesystem_id, account_id, 'None')
            delete_volume(filesystem_id, stdurl)

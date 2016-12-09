import os
import sys
import json
import time
from time import ctime
import subprocess
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    get_ntwInterfaceAndIP, passCmdToController, executeCmdNegative
from volumeUtils import get_volume_info, listVolumeWithTSMId_new, \
    create_volume, addNFSclient, delete_volume
from utils import logAndresult, get_IOPS_values_from_node
from tsmUtils import get_tsm_info, listTSMWithIP_new
from vdbenchUtils import is_vdbench_alive, executeVdbenchFile, kill_process

TC_name = sys.argv[0]
TC_name = TC_name.replace('.py','.log')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/'+TC_name,filemode='a',level=logging.DEBUG)

###steps followed for this testcase....
#1. mount Nfs share and run IOs
#2. while Ios are running add client to export 
#3. verifying on controller side in /etc/exports
#4. verify if IOs are running or not

testcase = 'Add clients to exports while IOs are running'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python addClientsToExports.py conf.txt  vdbench_file_to_run"
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
clientIP = config["Client1_IP"]

###-----------Methods Defined for this test case---------------------------####
###Description: compare two files......
###Parameters details....
##...state => before/after, checking file before/after any process
def file_compare(file1, file2, state):
    logging.info('Comparing Iops result files...')
    cmp_output = executeCmdNegative('diff %s %s' %(file1, file2))
    logging.debug('compared result is %s', (cmp_output))
    endTime = ctime()
    if cmp_output[0] == 'FAILED':
        msg = 'IOPs are not running %s adding clients to exports' %state
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    elif cmp_output[0] == 'PASSED':
        msg = 'IOPs are running fine %s adding clients to exports' %(state)
        logging.debug('%s', msg)
    else:
        logging.error('Failed to compare files having IOPS values')
        print "problem in comparing files"
#------------------------------------------------------------------------------

##Getting local client IP
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

##Listing Tsm and getting requried details
startTime = ctime()
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsmIP)
tsmList = listTSMWithIP_new(stdurl, tsmIP)
if tsmList[0] == 'PASSED':
    logging.info('TSM present with the given IP "%s"', tsmIP)
else:
    endTime = ctime()
    print 'Not able to list Tsm  "%s" due to: ' \
            %(tsmIP) + tsmList[1]
    logAndresult(testcase, 'BLOCKED', tsmList[1], startTime, endTime)
exit()
logging.info('Getting tsm_name, tsm_id, and dataset_id...')
get_tsmInfo = get_tsm_info(tsmList[1])
tsmID = get_tsmInfo[0]
tsmName = get_tsmInfo[1]
datasetID = get_tsmInfo[2]
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
        tsmName, tsmID, datasetID)
accName = tsmList[1][0].get('accountname')
poolName = tsmList[1][0].get('hapoolname')
node_pwd = 'test'

##Creating Volume
vol = {'name': 'addClientNFSVol', 'tsmid': tsmID, 'datasetid': datasetID, \
                'protocoltype': 'NFS', 'iops': 100}
startTime = ctime()
result = create_volume(vol, stdurl)
if result[0] == 'FAILED':
    endTime = ctime()
    print result
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)
else:
    print "Volume '%s' created successfully" %(vol['name'])

##Listing Volume and getting requried details
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

##Adding Nfs Client to the volume
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

##Mounting Nfs share
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

##Executing vdbench
logging.info('Running vdbench  by using file')
exe = executeVdbenchFile(volume, VdbFile)
logging.info('waiting for 10s for vdbench to run....')
time.sleep(10)

datapath = poolName+'/'+accName+tsmName+'/'+volname
nodeIP = tsmList[1][0].get('controlleripaddress')

##While IOs are running, adding client to export and verifying IOs
startTime = ctime()
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.info('vdbench is running')
    logging.info('While IOs are running adding client to exports')
    startTime = ctime()
    #Adding another client to the volume
    addClient1 = addNFSclient(stdurl, volid, clientIP)
    if addClient1[0] == 'PASSED':
        print 'Added NFS client "%s" to volume "%s"' \
                %(clientIP, volume['name'])
        logging.info('Added NFS client "%s" to volume "%s"', \
                        clientIP, volume['name'])
        
        #login to node, getting JID of the tenant
        logging.info('Logging to node and verifying exports....')
        cmd1 = "jls | grep %s | awk '{print $4'} | cut -d '/' -f 3" %(tsmIP)
        get_jid = passCmdToController(nodeIP, 'test', cmd1).strip()
        if not get_jid:
            msg = 'Not able to get jID for given tsm IP "%s"' %tsmIP
            print msg
            logAndresult(testcase, 'BLOCKED', msg, startTime, endTime)
        else:
            logging.debug('JID of tsm "%s" : %s', tsmIP, get_jid)
        
        #verifying whether client is added to exports in the node
        cmd2 = "cat /tenants/%s/etc/exports" %(get_jid)
        exports =  passCmdToController(nodeIP, 'test', cmd2).strip()
        logging.info('Clients in exports is as below....')
        logging.debug('%s', exports)
        if clientIP in exports:
            print 'Added nfs client "%s" to exports while IOs are running' \
                    %(clientIP)
            logging.debug('Added nfs client "%s" to exports '\
                    'while IOs are running',clientIP)
        else:
            endTime = ctime()
            msg = 'Failed to add client "%s" to exports while IOs are running'\
                    %clientIP
            logAndresult(testcase, 'FAILED', msg, startTime, endTime)
        
        #Verifying whether Ios are running after adding client to export
        time.sleep(2)#after adding client waiting fo 2s
        logging.info('Verifying Iops....')
        check_iops = get_IOPS_values_from_node(datapath, nodeIP, node_pwd, \
                'logs/afterAddingClient1.txt')
        time.sleep(5)
        check_iops = get_IOPS_values_from_node(datapath, nodeIP, node_pwd, \
                'logs/afterAddingClient2.txt')
        #Comparing files having IOps value
        file_cmp = file_compare('logs/afterAddingClient1.txt', \
                'logs/afterAddingClient2.txt', 'after')
	
        logging.info('After adding client checking whether vdbench is '\
                'still running or not')
        check_vdbench = is_vdbench_alive(volname)
        if not check_vdbench:
            endTime = ctime()
            msg = 'Vdbench has stopped running after adding client'
            logAndresult(testcase, 'FAILED', msg, startTime, endTime)
        logging.debug('After adding client vdbench is still running')
    else:
        endTime = ctime() 
	print addClient[1]
        logAndresult(testcase, 'FAILED', addClient1[1], startTime, endTime)
else:
    logging.debug('Vdbench has stopped running')
    endTime = ctime()
    msg = 'Vdbench has stopped running'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

##Adding result to result.csv
endTime = ctime()
resultCollection('Add clients to exports while IOs are running, '\
              'testcase is', ['PASSED',' '], startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])

#kill vdbench
kill_process(volname)

#removing the files created for comparsion
os.system('rm -rf logs/afterAddingClient1.txt logs/afterAddingClient2.txt')

#Unmounting the share
logging.info("UnMounting NFS Share '%s'", volume['name'])
startTime = ctime()
logging.info("UnMounting NFS Share '%s'", volume['name'])
umount = umountVolume_new(volume)
if 'FAILED' in umount[0] or 'device is busy' in umount[1]:
    logging.debug('Unmount failed, hence doing force unmount for volume "%s"', \
            volume['name'])
    umount_output = executeCmd('umount -l mount/%s' %(volume['mountPoint']))
    if umount_output[0] == 'PASSED':
        logging.debug('Forceful unmount passed for volume "%s"', \
                        volume['name'])
    else:
        logging.debug('Forcefull umount failed due to: %s', \
                        umount_output[1])
else:
    print umount[1]
    logging.debug('Volume "%s" umounted successfully', volume['name'])

#clearing the configurations
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


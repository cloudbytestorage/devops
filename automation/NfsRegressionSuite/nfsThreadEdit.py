import sys
import os
import json
import time
import subprocess
from time import ctime
import logging
from cbrequest import get_apikey, get_url, umountVolume_new, mountNFS, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd, \
    sendrequest, executeCmdNegative
from tsmUtils import get_tsm_info, listTSMWithIP_new, editNFSthreads
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
        delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, get_IOPS_values_from_node
from vdbenchUtils import is_vdbench_alive, kill_process, executeVdbenchFile

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)


testcase = 'Increase the threads as the IOs are running' 

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsThreadEdit.py conf.txt  vdbench_file_to_run"
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

#--------------------------METHODS---------------------------------------------
## to get nfs thread value.....
def get_nfs_thread_value(stdurl, tsm_id):
    logging.info('listing Tsm\'s Nfs option method...')
    querycommand = 'command=listTsmNfsOptions&tsmid=%s' %(tsm_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing Tsm\'s Nfs option: %s', str(rest_api))
    tsm_nfs = sendrequest(stdurl, querycommand)
    data = json.loads(tsm_nfs.text)
    logging.debug('response for listing Tsm\'s Nfs option: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['listTsmNfsOptionsResponse'].get('errortext'))
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result
    else:
        thread_value = data['listTsmNfsOptionsResponse'].get('nfsworkerthreads')
        result = ['PASSED', thread_value]
        return result

def verify_thread_result(thread_result):
    if thread_result[0] == 'PASSED':
        logging.debug('Nfs thread value is : %s', thread_result[1])
        return thread_result[1]
    else:
        logging.debug('Not able to get thread value due to :%s', thread_result[1])
        return thread_result[1]

# to call edit thread method repeatedly
def calling_edit_thread(tsm_id, nfsThread, stdurl):
    startTime = ctime()
    edit_threads = editNFSthreads(tsm_id, nfsThread, stdurl)
    if edit_threads[0] == 'FAILED':
        endTime = ctime()
        logging.debug('Failed to update nfs threads while IOs are '\
            'running due to: %s', edit_threads[1])
        resultCollection('%s ,testcase is' %testcase, ['BLOCKED', ''], \
            startTime, endTime)
        return 'BLOCKED'
    else:
        endTime = ctime()
        print 'Successfully updated nfs threads for volume "%s" to %s'\
            ' while IOs are running' %(volname, nfsThread)
        logging.debug('Successfully updated nfs threads for volume "%s" to %s'\
            ' while IOs are running' ,volname, nfsThread)
        return 'PASSED'

# compare file with values....
def file_compare(file1, file2, value, state):
    logging.info('Comparing Thread result files...')
    cmp_output = executeCmdNegative('diff %s %s' %(file1, file2))
    logging.debug('compared result is %s', (cmp_output))
    endTime = ctime()
    if cmp_output[0] == 'FAILED':
        msg = 'IOPs are not running %s editing thread' %state
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    elif cmp_output[0] == 'PASSED':
        msg = 'IOPs are running fine %s editing thread to %s' %(state, value)
        logging.debug('%s', msg)
    else:
        logging.error('Failed to compare files having IOPS values')
        print "problem in comparing files"

#----------------------------------------------------------------------------------

# listing tsm and getting details
startTime = ctime()
list_tsm = listTSMWithIP_new(stdurl, tsmIP)
if list_tsm[0] == 'PASSED':
    logging.info('TSM present with the given IP "%s"', tsmIP)
else:
    endTime = ctime()
    print list_tsm[1]
    logAndresult(testcase, 'BLOCKED', list_tsm[1], startTime, endTime)

logging.info('Getting tsm_name, tsm_id, and dataset_id...')
get_tsmInfo = get_tsm_info(list_tsm[1])
tsm_id = get_tsmInfo[0]
tsm_name = get_tsmInfo[1]
dataset_id = get_tsmInfo[2]
accName = list_tsm[1][0].get('accountname')
poolName = list_tsm[1][0].get('hapoolname')
node_ip = list_tsm[1][0].get('controlleripaddress')
node_pwd = 'test'

logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
            tsm_name, tsm_id, dataset_id)

# creating volume and getting required details
vol = {'name': 'nfsThreadsVol', 'tsmid': tsm_id, 'datasetid': dataset_id, \
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

# adding nfs client 
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'all')
if addClient[0] == 'PASSED':
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)

# mounting nfs share
volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
                'name' : volname}
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

datapath = poolName+'/'+accName+tsm_name+'/'+volname
logging.info('Running vdbench  by using file')

#running vdbench
exe = executeVdbenchFile(volume, VdbFile)
logging.info('waiting for 10s for vdbench to run')
time.sleep(10)


logging.info('Checking whether vdbench is running or not....')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    # while vdbench is running changing nfs thread values \
            #and verfying Ios are running fine or not
    logging.info('vdbench is running')
    logging.info('Editing NFS thread while IOs are running....')

    thread1 = get_nfs_thread_value(stdurl, tsm_id)
    logging.info('Getting present nfs thread value....')
    tvalue1 = verify_thread_result(thread1)
    t256 = calling_edit_thread(tsm_id, 256, stdurl)
    logging.info('Verifying IOPS....')
    # getting Iops value after changing thread
    get_iops = get_IOPS_values_from_node(datapath, node_ip, node_pwd, \
            'logs/afterThreadEdit1_256.txt')
    logging.debug('Iops value after editing thread to 256: \n%s',get_iops)
    logging.info('waiting for 5s and again taking iops value')
    time.sleep(5)
    get_iops = get_IOPS_values_from_node(datapath, node_ip, node_pwd, \
        'logs/afterThreadEdit2_256.txt')
    logging.debug('Iops value after editing thread to 256: \n%s',get_iops)
    # comparing the files 
    file_cmp = file_compare('logs/afterThreadEdit1_256.txt', \
            'logs/afterThreadEdit2_256.txt', 256, 'after')
    logging.info('Checking vdbench....')
    check_vdbench = is_vdbench_alive(volname)
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing threads'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    os.system('rm -rf logs/afterThreadEdit1_256.txt')
    os.system('rm -rf logs/afterThreadEdit2_256.txt')
    
    # Again changing thread value and validating
    logging.info('waiting for 10s before increasing thread again')
    time.sleep(10)
    thread1 = get_nfs_thread_value(stdurl, tsm_id)
    tvalue1 = verify_thread_result(thread1)
    t512 = calling_edit_thread(tsm_id, 512, stdurl)
    logging.info('Verifying IOPS....')
    get_iops = get_IOPS_values_from_node(datapath, node_ip, node_pwd, \
            'logs/afterThreadEdit1_512.txt')
    logging.debug('Iops value after editing thread to 512: \n%s',get_iops)
    logging.info('waiting for 5s and again taking iops value')
    time.sleep(5)
    get_iops = get_IOPS_values_from_node(datapath, node_ip, node_pwd, \
        'logs/afterThreadEdit2_512.txt')
    logging.debug('Iops value after editing thread to 512: \n%s',get_iops)
    file_cmp = file_compare('logs/afterThreadEdit1_512.txt', \
            'logs/afterThreadEdit2_512.txt', 512, 'after')
    logging.info('Checking vdbench....')
    if not check_vdbench:
        endTime = ctime()
        msg = 'Vdbench has stopped running after editing threads'
        logAndresult(testcase, 'FAILED', msg, startTime, endTime)
    os.system('rm -rf logs/afterThreadEdit1_256.txt logs/afterThreadEdit2_256.txt')

# verfying and collecting result
if 'BLOCKED' in (t256 and t512):
    endTime = ctime()
    msg = 'failed to increase nfs thread values'
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
else: 
    endTime = ctime()
    resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
            startTime, endTime)
    resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
    logging.debug('%s, testcase PASSED', testcase)

# killing vdbench process
time.sleep(2)
logging.info('Checking whether vdbench is still running or not....')
check_vdbench = is_vdbench_alive(volname)
if check_vdbench:
    logging.debug('vdbench is running, going to kill the vdbench process...')
    kill_process(volname)
    time.sleep(2)
    check_vdbench = is_vdbench_alive(volname)
    if check_vdbench:
        logging.debug('Failed to kill vdbench process, going to kill again...')
        kill_process(volname)
    else:
        logging.debug('Successfully killed vdbench process')
        print 'Successfully killed vdbench process'
else:
    logging.debug('Vdbench process has stopped unexpectedly...')
    print 'Vdbench process has stopped'

##putting some sleep before unmounting
time.sleep(2)
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


### Clearing the configurations....
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

logging.info('Changing back threads to 128')
edit_threads = editNFSthreads(tsm_id, 128, stdurl)
if edit_threads[0] == 'FAILED':
    logging.info('Could not change the thread value to 128')
else:
    logging.debug('Changed threads value to 128')

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----' %testcase)

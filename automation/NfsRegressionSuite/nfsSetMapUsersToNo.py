import sys
import os
import json
import time
import subprocess
from subprocess import Popen, PIPE, check_call, CalledProcessError
from time import ctime
import logging
from cbrequest import get_apikey, get_url, sshToOtherClient, sendrequest, \
    resultCollection, resultCollectionNew, configFile, getoutput, executeCmd
from tsmUtils import get_tsm_info, listTSMWithIP_new
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
        delete_volume, listVolumeWithTSMId_new
from utils import logAndresult

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)


testcase ='Set map all users to root to NO and verify if the roots user '\
        'permission are not set for the nfs mount point'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print "Arguments are not correct, Please provide as follows..."
    print "python nfsSetMapUsersToNo.py conf.txt"
    logging.debug('----Ending script because of parameter mismatch----\n')
    exit()


#resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
tsmIP = config["ipVSM2"]

client_public_ip = config['Client_IP']
usr = 'User2'
pwd = 'test@123'

#------------------------------METHODS-----------------------------------------
###Function to mount NFS share...
def mount_nfs_volume(volume):
    executeCmd('mkdir -p /mnt/%s' %(volume['mountPoint']))
    mountResult = executeCmd('mount -t nfs %s:/%s /mnt/%s' \
        %(volume['TSMIPAddress'], volume['mountPoint'], volume['mountPoint']))
    if mountResult[0] == 'PASSED':
        print 'NFS volume \"%s\" mounted successfully' %(volume['name'])
        return 'PASSED'
    else:
        print 'NFS volume \"%s\" failed to mount' %(volume['name'])
        return 'FAILED'
#*****************************************************************************
##to unmount nfs share....
def umount_nfs_volume(volume):
    mountCheck = executeCmd('mount | grep %s' %(volume['mountPoint']))
    if mountCheck[0] == 'PASSED':
        umountResult = executeCmd('umount /mnt/%s' %(volume['mountPoint']))
        if umountResult[0] == 'PASSED':
            print 'Volume \"%s\" umounted successfully' %(volume['name'])
            return ['PASSED', '']
        else:
            print umountResult[1]
            print 'Volume \"%s\" failed to umount' %(volume['name'])
            return ['FAILED', umountResult[1]]
    else:
        print 'Volume \"%s\" is not mounted' %(volume['name'])
        return ['PASSED', 'Volume is not mounted']
#*****************************************************************************
#to add user....
def addUserToHomeDir(usr, pwd):
    try:
        x = check_call(['useradd', '-m', usr])
        proc = Popen(['passwd', usr],stdin=PIPE,stderr=PIPE)
        proc.stdin.write('%s\n' %pwd)
        proc.stdin.write(pwd)
        proc.stdin.flush()
        stdout,stderr = proc.communicate()
        result = ['PASSED', 'User "%s" added successfully' %usr]
        return result
    except subprocess.CalledProcessError as e:
        result = ['FAILED', 'Failed to add user "%s" to home dir' %usr]
        return result
#*****************************************************************************
###to delete user added...
def deleteUser(usr):
    try:
        x = check_call(['userdel', usr])
        result = ['PASSED', 'User "%s" deleted successfully' %usr]
        return result
    except subprocess.CalledProcessError as e:
        result = ['FAILED', 'user "%s" does not exist' %(usr)]
        return result
#------------------------------------------------------------------------------

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

#creating volume and getting details
vol = {'name': 'NfsMapRootNo', 'tsmid': tsm_id, 'datasetid': dataset_id, \
            'protocoltype': 'NFS', 'iops': 500}
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

# adding nfs client as all
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
nfsMount = mount_nfs_volume(volume)
if nfsMount == 'PASSED':
    logging.info('Mounted Nfs Share "%s" in "mount/%s" successfully',\
                        volume['name'], volume['mountPoint'])
else:
    endTime = ctime()
    msg = 'failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
                            %(volume['mountPoint']))
mount_point = mount_point[0].strip('\n')
logging.info('mountPoint is : %s', mount_point)

# adding user
user_add = addUserToHomeDir(usr, pwd)
if user_add[0] == 'FAILED':
    endTime = ctime()
    logAndresult(testcase, 'FAILED', user_add[1], startTime, endTime)
else:
    logging.debug('%s', user_add[1])
    print user_add[1]

# validating map user to NO
cmd1 = 'touch %s/a' %mount_point
exe = executeCmd(cmd1)
cmd2 = 'rm -rf %s/*' %mount_point
logging.info('logging as other user to verify root permission')
other_user = sshToOtherClient(client_public_ip, usr, pwd, cmd2)
logging.debug('%s', other_user)
print other_user
if ('Operation not permitted') in other_user:
    logging.debug('%s', other_user)
    msg  = 'Expected result: user could not delete file even if map root '\
        'is set to No'
else:
    endTime = ctime()
    msg = 'Unexpected Result: user has no root permission, yet could delete'\
        ' file'
    logging.debug('%s', other_user)
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)

# collecting results
endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
                startTime, endTime)
#resultCollectionNew('"%s" testcase ends....' %testcase, ['', '\n'])
logging.debug('%s, testcase PASSED', testcase)

## clearing configuration
del_usr = deleteUser(usr)
if del_usr[0] == 'FAILED':
    logging.debug('%s', del_usr[1])
else:
    logging.debug('%s', del_usr[1])

time.sleep(2) #before unmounting waiting for 2s
logging.info("UnMounting NFS Share '%s'", volume['name'])
umount = umount_nfs_volume(volume)
if umount == 'PASSED':
    logging.debug('Volume "%s" umounted successfully', volume['name'])
else:
    logging.debug('Failed to umount the volume "%s"', volume['name'])

startTime = ctime()
logging.info('Deleting volume "%s"', volname)
deleteVolume =  delete_volume(volid, stdurl)
if 'PASSED' in deleteVolume:
    print 'Volume \"%s\" Deleted successfully' %(volname)
    logging.debug('Volume \"%s\" Deleted successfully', \
             volname)
else:
    print 'Failed to deleted the volume \"%s\"' %(volname)
    logging.debug('Failed to deleted the volume \"%s\"', \
        volname)

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----' %testcase)

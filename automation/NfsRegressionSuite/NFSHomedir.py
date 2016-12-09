import sys
import os
import json
import md5
import time
import subprocess
from subprocess import Popen, PIPE, check_call, CalledProcessError
from time import ctime
import logging
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
         delete_volume, listVolumeWithTSMId_new
from time import ctime
from cbrequest import get_apikey, get_url,  umountVolume, mountNFS, \
        executeCmd, resultCollection, resultCollectionNew, sendrequest, \
        configFile, replace_data, getoutput, sshToOtherClient
from utils import logAndresult
from tsmUtils import get_tsm_info, listTSMWithIP_new

logging.basicConfig(format='%(asctime)s %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

###steps followed for this testcase
#1. create volume and mount the volume (mounted share in /mnt directory)
#2. change the home directory path "/home" to mount path of the nfs share in \
        #/etc/default/useradd file
#3. adding two user
#4. login to one of the user and delete folder of other user
#5. for above opertion permission should be denied else testcase is blocked
#6. then deleting the users and changing back to home directory path in the file

testcase = 'Mount NFS share on home directory'

logging.info('----Start of testcase "%s"----', testcase)

if len(sys.argv) < 2:
    print 'Arguments are not correct, Please provide as follows...\n'
    print 'python NFSHome.py conf.txt\n'
    logging.debug("----Ending script because of parameter mismatch----\n")
    exit()

resultCollectionNew('\n"%s" testcase starts....' %testcase, ['', ''])
print ('----Start of testcase "%s"----' %testcase)

conf = configFile(sys.argv)
apikey = get_apikey(conf)
stdurl = get_url(conf, apikey[1])
tsm_ip = conf["ipVSM2"]
client_ip = conf["Client_IP"]

###Function to add user to home dir...
def addUserToHomeDir(usr, pwd):
    try:
        x = check_call(['useradd', '-m', usr])
        proc = Popen(['passwd', usr],stdin=PIPE,stderr=PIPE)
        proc.stdin.write('%s\n' %pwd)
        proc.stdin.write(pwd)
        proc.stdin.flush()
        stdout,stderr = proc.communicate()
        result = ['PASSED', 'User added successfully']
        return result
    except subprocess.CalledProcessError as e:
        result = ['FAILED', 'Failed to add user to home dir']
        return result

###Function to delete user added...
def deleteUser(usr):
    try:
        x = check_call(['userdel', usr])
        result = ['PASSED', 'User deleted successfully']
        return result
    except subprocess.CalledProcessError as e:
        result = ['FAILED', 'user "%s" does not exist' %(usr)]
        return result

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
    
###----------------------------------------------------------------------------

startTime = ctime()
infile = '/etc/default/useradd'
HOME = getoutput('cat /etc/default/useradd | grep HOME | cut -d  "=" -f 2')
HOME = HOME[0].rstrip('\n')
usr1 = 'user1'
pwd = 'test123'
usr2 = 'user2'

list_tsm = listTSMWithIP_new(stdurl, tsm_ip)
if list_tsm[0] == 'PASSED' :
    logging.info('Tsm present with the given IP "%s"', tsm_ip)
else:
    endTime = ctime()
    print 'Not able to list list_tsms due to: ' + list_tsm[1]
    logAndresult(testcase, 'BLOCKED', list_tsm[1], startTime, endTime)

logging.info('Getting tsm_name, tsm_id, and dataset_id...')
get_tsmInfo = get_tsm_info(list_tsm[1])
tsm_id = get_tsmInfo[0]
tsm_name = get_tsmInfo[1]
dataset_id = get_tsmInfo[2]
logging.debug('tsm_name: %s, tsm_id: %s, dataset_id: %s',\
            tsm_name, tsm_id, dataset_id)

vol = {'name': 'NFSHome', 'tsmid': tsm_id, 'datasetid': dataset_id, \
        'protocoltype': 'NFS', 'iops': 500} 

result = create_volume(vol, stdurl)
if result[0] == 'PASSED':
    print "Volume '%s' created successfully" %(vol['name'])
else:
    endTime = ctime()
    print result[1]
    logAndresult(testcase, 'BLOCKED', result[1], startTime, endTime)

volList = listVolumeWithTSMId_new(stdurl, tsm_id)
if 'PASSED' in volList:
    logging.info('Volumes present in the Tsm "%s"', tsm_name)
else:
    endTime = ctime()
    print 'Not able to list Volumes in list_tsm "%s" due to: '\
            %(tsm_name) + volList[1]
    logAndresult(testcase, 'BLOCKED', volList[1], startTime, endTime)

volume_name = vol['name']
get_volInfo = get_volume_info(volList[1], volume_name)
volname, volid, vol_mntPoint = get_volInfo[1], get_volInfo[2], get_volInfo[3]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s',\
                volname, volid, vol_mntPoint)
addClient = addNFSclient(stdurl, volid, 'all')
if 'PASSED' in addClient:
    print 'Added NFS client "all" to volume "%s"' %volname
    logging.info('Added NFS client "all" to volume "%s"', volname)
else:
    endTime = ctime()
    logAndresult(testcase, 'BLOCKED', addClient[1], startTime, endTime)
    
volume = {'TSMIPAddress' : tsm_ip, 'mountPoint': vol_mntPoint,\
                'name' : volname}

mount_nfs = mount_nfs_volume(volume)
if mount_nfs == 'FAILED':
    endTime = ctime()
    msg = 'Failed to mount NFS share "%s"' %(volume['name'])
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)
else:
    logging.debug('NFS volume \"%s\" mounted successfully', (volume['name']))

###Seting Share path as home Dir
mount_path = getoutput('mount | grep %s | awk {\'print $3\'}' \
        %(volume['mountPoint']))
mount_path =  mount_path[0].rstrip('\n')

#replacing home path in  /etc/default/useradd file....
HOME = getoutput('cat /etc/default/useradd | grep HOME | cut -d  "=" -f 2')
HOME = HOME[0].rstrip('\n')

replace_data(infile, HOME, mount_path)
logging.debug("replacing home path as %s in %s file", mount_path, infile)

#adding user's to the new home path....
useradd1 = addUserToHomeDir(usr1, pwd)
if "FAILED" in  useradd1:
    endTime = ctime()
    print useradd1[1]
    logAndresult(testcase, 'FAILED', useradd1[1], startTime, endTime)

useradd2 = addUserToHomeDir(usr2, pwd)
if "FAILED" in  useradd2:
    endTime = ctime()
    print useradd2[1]
    logAndresult(testcase, 'FAILED', useradd2[1], startTime, endTime)

#as user1 changing directory to user2...
logging.info('Logging as user1')
cmd1 = 'touch a; mkdir ../user2/new'
logging.info('executing cmd "%s" in user1', cmd1)
login_as_user1 = sshToOtherClient(client_ip, 'user1', pwd, cmd1).strip()
print login_as_user1
if ("mkdir" and "Permission denied") in login_as_user1:
    logging.debug('%s', login_as_user1)
    logging.debug('expected result: user1 has no permission to do any '\
            'operation on user2')
else:
    endTime = ctime()
    msg = 'Unexpected result: please verify user permission'
    logging.debug('%s', msg)
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)    

#as user2 removing folder of user1....
logging.info('Logging as user2')
cmd2 = 'rm -rf ../user1/a'
logging.info('executing cmd "%s" in user2', cmd2)
login_as_user2 = sshToOtherClient(client_ip, 'user2', pwd, cmd2).strip()
print login_as_user2
logging.info('checking user permission')
if ("rm" and "Permission denied") in login_as_user2:
    logging.debug('%s', login_as_user2)
    logging.debug('expected result: user2 has no permission to do any '\
            'operation on user1')
else:
    endTime = ctime()
    msg = 'Unexpected result: please verify user permission'
    logging.debug('%s', msg)
    logAndresult(testcase, 'FAILED', msg, startTime, endTime)    

endTime = ctime()
resultCollection("%s, testcase is" %testcase, ['PASSED', ' '], \
        startTime, endTime)

#deleting the created user's....
userdel1 = deleteUser(usr1)
if userdel1[0] == 'FAILED':
    logging.debug('Failed to delete user "%s"', usr1)
    print 'Failed to delete user "%s"' %usr1
else:
    logging.debug('Successfully deleted user "%s"', usr1)
    print 'Successfully deleted user "%s"' %usr1

userdel2 = deleteUser(usr2)
if userdel2[0] == 'FAILED':
    logging.debug('Failed to delete user "%s"', usr2)
    print 'Failed to delete user "%s"' %usr2
else:
    logging.debug('Successfully deleted user "%s"', usr2)
    print 'Successfully deleted user "%s"' %usr2

#changing back home path....
HOME = getoutput('cat /etc/default/useradd | grep HOME | cut -d  "=" -f 2')
HOME = HOME[0].rstrip('\n')
replace_data(infile, HOME, '/home')
logging.debug('replacing back Home path as "/home" in %s file', infile)
print 'replacing back Home path as "/home" in %s file' %infile

#unmounting and deleting the volume....
umount = umount_nfs_volume(volume)
if umount == 'PASSED':
    logging.debug('Volume "%s" umounted successfully', volume['name'])
else:
    logging.debug('Failed to umount the volume "%s"', volume['name'])

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

logging.info('----End of testcase "%s"----\n', testcase)
print ('----End of testcase "%s"----\n' %testcase)

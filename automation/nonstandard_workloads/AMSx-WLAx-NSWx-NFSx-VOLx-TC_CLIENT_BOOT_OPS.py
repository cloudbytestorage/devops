# SMGLNSN
'''
###############################################################################################################
# Testcase Name : Ocassional Client reboot                      		                              #               
#                                                                                                             #
# Testcase Description : This test performs the following actions continuously for fixed set of iterations :  #
#                        a) take ssh to another client(client details taken from config file)                 #
#			 b) mount the share (mount details written in /etc/fstab file)                        #
#                        b) dump some data                                                                    #
#                        c) reboot the client and wait till it is up and accessable                           #
#                        d) again take ssh and mount the share and verify mount and dump data                 #
#                                                                                                             # 
# Testcase Pre-Requisites : Pool has to be created                                                            #
#                                                                                                             #
# Testcase Creation Date : 16/05/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 16/05/2016                                                                         #  
#                                                                                                             #  
# Modifications made : None                                                                                   #  
#                                                                                                             #
# Testcase Author : Prathima                                                                                  #
###############################################################################################################
'''
# Import necessary packages and methods
import os
import sys
import json
import time
from time import ctime
import subprocess
import paramiko
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
    get_apikey, executeCmd, mountNFS, getoutput, sshToOtherClient
from tsmUtils import get_tsm_info, listTSMWithIP_new, tsm_creation_flow, \
    verify_tsmIP_from_configFile, delete_tsm
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new, edit_vol_quota
from utils import logAndresult, mountPointDetails, UMain
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_process
from poolUtils import pool_creation_flow, delete_pool
import logging

#***************Initialization for Logging location****************************
tcName = sys.argv[0]
tcName = tcName.split('.py')[0]
logFile = tcName + '.log'
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/'+logFile,filemode='a',level=logging.DEBUG)
#*****************************************************************************
#testcase = 'Ocassional client reboot'
logging.info('----Start of testcase "%s"----', tcName)

#***************Check proper agruments are passed******************************
if len(sys.argv) < 2:
    print "Argument are not correct, Please provide as follows"
    print "python %s.py conf.txt" %(tcName)
    logging.debug('----Ending script because of parameter mismatch----')
    exit()
#******************************************************************************

#***************Get necessary params and value from config file****************
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])

disk_type = config["pool_disk_type"]
pool_type = config["pool_type"]
pool_iops =  config["pool_iops"]
no_of_disk = config["num_pool_disks"]
tsmIP = config['ipVSM1']
tsmInterface = config['interfaceVSM1']
acctName = config["AccountName"]

####Client details to take ssh for the same......
other_client_ip = config["Client1_IP"]
other_client_pwd = config["Client1_pwd"]
other_client_username = config["Client1_user"]
####.............................................

####This is to copy some data into the share.....
copy_file = 'http://20.10.1.101/dailybuilds/1.4.0.p5/Apr12-1.4.0.883/patch_1.4.0.p5_883.tar.gz'
####.............................................
#******************************************************************************

#***************Methods Defined for this testcase******************************

##....Method Description : Appending data into given file through ssh........##
#..........Parameter details...........
#...filename => into which file data has to be written, Eg: /etc/fstab
#...data => what has to be written
def write_data_into_file(client_ip, username, pwd, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(client_ip, username=username, password=pwd)
    sftp = ssh.open_sftp()
    f = sftp.open(filename, 'a')
    f.write(data)
    f.close()
    ssh.close()

##....Method Description : Deleting data from the given file through ssh.....##
#..........Parameter details...........
#...filename => into which file data has to be written, Eg: /etc/fstab
#...data => what has to be deleted
def remove_data_from_file(machinename, username, pwd, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machinename, username=username, password=pwd)
    sftp = ssh.open_sftp()
    # open file and reading the data
    f = sftp.open(filename, 'r')
    data_list = f.readlines()
    f.close
    #print data_list
    
    # deleting the last line
    del data_list[-1:]

    #write the changed data(list) to a file) #here writting to the same file
    fout = sftp.open(filename, 'w')
    fout.writelines(data_list)
    fout.close()
    ssh.close()

#******************************************************************************

#**************PREREQUSITES: POOL AND VSM CREATION*****************************

####-------------------------Pool creation---------------------------------####
startTime = ctime()
poolName = 'nPoolClient'
pool_paras = {'name': poolName, 'grouptype': pool_type, \
                'iops': pool_iops}

pool_create =  pool_creation_flow(stdurl, pool_paras, no_of_disk, disk_type)
endTime = ctime()
if pool_create[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', pool_create[1], startTime, endTime)
logging.debug('Pool "%s" is created successfully', poolName)

####--------------------------Vsm creation---------------------------------####
startTime = ctime()
tsm_params = {'name': 'nTsmClient', 'ipaddress': tsmIP, 'totaliops': (pool_iops), \
        'tntinterface': tsmInterface}
tsm_create = tsm_creation_flow(stdurl, poolName, acctName, tsm_params)
endTime = ctime()
if tsm_create[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', tsm_create[1], startTime, endTime)
logging.debug('%s', tsm_create[1])
#******************************************************************************

#***************Listing VSM and extracting IDs*********************************
startTime = ctime()
tsmList = listTSMWithIP_new(stdurl, tsmIP)
endTime = ctime()
if tsmList[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', tsmList[1], startTime, endTime)

get_tsmInfo = get_tsm_info(tsmList[1])
tsmID = get_tsmInfo[0]
tsmName = get_tsmInfo[1]
datasetID = get_tsmInfo[2]
pool_id = tsmList[1][0].get('poolid')
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s', \
        tsmName, tsmID, datasetID)
#******************************************************************************

#***************************Volume Operations**********************************

####----------------------Volume Creation----------------------------------####
startTime = ctime()
vol = {'name': 'nfsClient', 'tsmid': tsmID, 'datasetid': datasetID, \
		'protocoltype': 'NFS', 'iops': (pool_iops), 'quotasize': '10G'}
volname = vol['name']
result = create_volume(vol, stdurl)	
endTime = ctime()
if result[0] == 'FAILED':
   logAndresult(tcName, 'BLOCKED', result[1], startTime, endTime)
   pass
logging.debug('"%s" was created successfully',volname)

####-----------Listing Volume and getting requried details-----------------####
volList = listVolumeWithTSMId_new(stdurl, tsmID)
endTime = ctime()
if volList[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', volList[1], startTime, endTime)

get_volInfo = get_volume_info(volList[1], volname)
volid, vol_mntPoint, vol_quota = get_volInfo[2], get_volInfo[3], get_volInfo[6]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_quota: %s',
		volname, volid, vol_mntPoint, vol_quota)

####------------Adding Nfs Client All to the volume------------------------####
startTime = ctime()
addClient = addNFSclient(stdurl, volid, 'ALL')
endTime = ctime()
if addClient[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', addClient[1], startTime, endTime)
    pass
logging.debug('Added nfs client "ALL" to the volume')

#******************************************************************************

#***************Execution's on different client by taking SSH******************
volume = {'TSMIPAddress' : tsmIP, 'mountPoint': vol_mntPoint,\
		'name' : volname}
####------------Writing mountpoint into /etc/fstab-------------------------####
startTime = ctime()
logging.info('Writting mountpoint into /etc/fstab')
cmd = '\n%s:/%s /mnt/client nfs rw,sync,mountproto=tcp 0 0' \
				%(tsmIP, vol_mntPoint)
write_data = write_data_into_file(other_client_ip, other_client_username, \
	other_client_pwd, '/etc/fstab', cmd)
	
####------------Verifying whether mountpoint written-----------------------####
logging.info('Verifying whether mountpoint is written in /etc/fstab')
cmd2 = 'cat /etc/fstab | grep %s' %(vol_mntPoint)
check_data = sshToOtherClient(other_client_ip, other_client_username,\
	other_client_pwd, cmd2).strip('\n')
if vol_mntPoint in check_data:
    logging.debug('MountPoint is added to fstab successfully')
else:
    endTime = ctime()
    msg = 'MountPoint is not added to fstab'
    logAndresult(tcName, 'BLOCKED', msg, startTime, endTime)
	
####------Creating directory and mounting the share and verify the same----####
logging.info('Creating directory and mounting the share and verify the same')
cmd3 = 'mkdir /mnt/client; mount -a; df -h /mnt/client'
verify_mount = sshToOtherClient(other_client_ip, other_client_username,\
	other_client_pwd, cmd3).strip('\n')
logging.debug('%s', verify_mount)
msg1 = 'mount.nfs: Connection timed out'
msg2 = 'No such file or directory'
if str(verify_mount) in msg2 or  str(verify_mount) in msg1:
    endTime = ctime()
    logging.error('Failed to mount the given mountpoint in fstab')
    logAndresult(tcName, 'BLOCKED', verify_mount, startTime, endTime)
####------------Dumping some data into the share---------------------------####
logging.info('Dumping some data into the share')
cmd4 = 'wget -P /mnt/client %s' %copy_file
dump_data = sshToOtherClient(other_client_ip, other_client_username,\
            other_client_pwd, cmd4).strip('\n')
logging.debug('%s',dump_data)
if 'Cannot write to' in dump_data:
    msg = 'Failed to write data into mountpoint'
    logAndresult(tcName, 'BLOCKED', dump_data, startTime, endTime)

####-----Loop: To reboot client multiple times and verfiy mount------------####	
logging.info('Verifying client reboot and IO run on the mount point '\
        'multiple times')

for x in range(1, 5):
    ####---------------Reboot Client---------------------------------------####
    logging.debug('Rebooting Client')
    cmd5 = 'reboot'
    reboot_client = sshToOtherClient(other_client_ip, other_client_username,\
            other_client_pwd, cmd5)
    logging.info('Waiting for 1min for client to come up and verifying it')
    time.sleep(60) 
    startTime = ctime()
    ####------------Verifying whether client is UP by pinging its IP-------####
    count = 1
    while True:
        ping_client =  os.system("ping -c 4 %s" %other_client_ip)
        if ping_client != 0:
            logging.debug('Client is not up.. hence waiting for another 2min')
            time.sleep(120)
            count = count + 1
        else:
            logging.debug('Client is up....')
            break
        if count == 3:
            ping_client =  os.system("ping -c 4 %s" %other_client_ip)
            if ping_client != 0:
                break
            endTime = ctime()
            msg = 'Waited for more than 5min, client still not up'
            logAndresult(tcName, 'BLOCKED', msg, startTime, endTime)
    
    logging.debug('client is reachable, waiting for 1min before taking ssh')
    time.sleep(60)
    ####---------Trying to login to client after it is reachable-----------####
    for y in range(1, 4):
        test = sshToOtherClient(other_client_ip, other_client_username,\
                    other_client_pwd, ' ').strip('\n')
        if ('No route to host' in test):
            logging.debug('not able to take ssh as client is not completely up')
            logging.debug('waiting for another 30s')
            time.sleep(30)
        else:
            logging.debug('Client is up and able to take ssh')
            break
    else:
        msg = 'SSh to client failed, even if client is reachble'
        logAndresult(tcName, 'BLOCKED', msg, startTime, endTime)
	
    ####-------After reboot of client, trying to mount the share-----------####
    logging.info('After reboot verifying mount and dumping data to mount point')
    cmd6 = 'mount -a; df -h /mnt/client'
    connect_to_client = sshToOtherClient(other_client_ip, other_client_username,\
                other_client_pwd, cmd6).strip('\n')
    logging.debug('%s', connect_to_client)
    if (vol_mntPoint in connect_to_client)  and \
            ('/mnt/client' in connect_to_client):
        logging.debug('After reboot mounpoint is present in the client')
    else:
        endTime = ctime()
        logging.error('After client reboot not able to mount the share')
        logAndresult(tcName, 'BLOCKED', connect_to_client, startTime, endTime)
	
    ####--------Again Dumping some data into the share---------------------####
    logging.debug('Dumping data into share after reboot')
    cmd4 = 'wget -P /mnt/client %s' %copy_file
    dump_data = sshToOtherClient(other_client_ip, other_client_username,\
                other_client_pwd, cmd4).strip('\n')
    logging.debug('%s',dump_data)
    if 'Cannot write to' in dump_data:
        msg = 'Failed to write data into mountpoint after reboot'
        logAndresult(tcName, 'FAILED', dump_data, startTime, endTime)
    logging.debug('Successfully written data into the share')    
    logging.debug('Verfying client reboot process is done for %s times', x)
####-------------------------End of loop-----------------------------------####
#**************Exection's on other  client Ends********************************

#**********************Update result in result.csv*****************************
endTime = ctime()
resultCollection('%s, testcase is' %tcName, ['PASSED',' '], \
                        startTime, endTime)
#******************************************************************************

#***************Clear Configurations*******************************************

####--------------------------Unmount Share--------------------------------####
logging.debug('Unmounting nfs share from the client')
umount_cmd = 'umount -l /mnt/client'
umount = sshToOtherClient(other_client_ip, other_client_username,\
            other_client_pwd, umount_cmd).strip('\n')
logging.debug('%s',umount)

###---------------Removing mount point from the /etc/fstab file------------####
logging.debug('Removing mountPoint from /etc/fstab on other client through ssh')
cmd = '%s:/%s /mnt/client nfs rw,sync,mountproto=tcp 0 0' \
                        %(tsmIP, vol_mntPoint)
remove_data_from_file(other_client_ip, other_client_username,\
                other_client_pwd, '/etc/fstab', cmd)

####--------------------------Volume Deletion------------------------------####
delete_result = delete_volume(volid, stdurl)
endTime = ctime()
if delete_result[0] == 'FAILED':
    logging.debug('%s',delete_result[1])
logging.debug('Volume "%s" deleted successfully', volname)

####--------------------------Vsm Deletion---------------------------------####
del_tsm = delete_tsm(tsmID, stdurl)
if del_tsm[0] == 'FAILED':
    logging.error('%s', del_tsm[1])
    logging.error('Tsm deletion failed, hence not deleting pool')
    exit()
logging.debug('%s', del_tsm[1])

####--------------------------Pool Deletion--------------------------------####
del_pool = delete_pool(pool_id, stdurl)
if del_pool[0] == 'FAILED':
    logging.error('%s', del_pool[1])
logging.debug('%s', del_pool[1])

#******************************************************************************

logging.info('----End of testcase "%s"----', tcName)

####***********************************END*********************************####

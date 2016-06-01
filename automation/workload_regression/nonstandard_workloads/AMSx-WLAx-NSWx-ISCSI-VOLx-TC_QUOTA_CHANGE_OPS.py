# SMGLNSN
'''
###############################################################################################################
# Testcase Name : Space Increase of Iscsi volume			                                      #
#                                                                                                             #
# Testcase Description : This test performs the following actions continuously for fixed set of iterations :  #
#                        a) Increase space of iscsi volume                                                    #
#			 b) perform logout and login of the lun                                               #
#                        b) get the size of iscsi device                                                      #
#                        c) verifying if space is updated on server and client side                           #
#                                                                                                             #
#                                                                                                             # 
# Testcase Pre-Requisites : Pool has to be created                                                            #
#                                                                                                             #
# Testcase Creation Date : 04/05/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 06/05/2016                                                                         #  
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

from cbrequest import get_url, configFile, sendrequest, resultCollection, \
    get_apikey, executeCmd, getoutput
from tsmUtils import get_tsm_info, listTSMWithIP_new, tsm_creation_flow, \
    verify_tsmIP_from_configFile, delete_tsm
from volumeUtils import get_volume_info, create_volume, addNFSclient, \
    delete_volume, listVolumeWithTSMId_new, edit_vol_quota, \
    getDiskAllocatedToISCSI
from utils import logAndresult, mountPointDetails, assign_iniator_gp_to_LUN, \
    iscsi_login_logout, iscsi_mount_flow, discover_iscsi_lun, UMain
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

#testcase = 'Increase Space of Iscsi volume'
logging.info('----Start of testcase "%s"----', tcName)

#***************Check proper arguments are passed******************************
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
#******************************************************************************

#***************Methods Defined for this testcase******************************

##....Method Description : discover lun, login and get device and its size...## 

def iscsi_get_quota(tsm_ip, vol_iqn, vol_mntPoint):
    discover_lun = discover_iscsi_lun(tsm_ip, vol_iqn)
    if discover_lun[0] == 'FAILED':
        return ['FAILED', discover_lun[1]]
    logging.debug('IQN of discovered lun is "%s"', discover_lun[1])
    lun_login = iscsi_login_logout(discover_lun[1], tsm_ip, 'login')
    if lun_login[0] == "FAILED":
        return ["FAILED", lun_login[1]]
    time.sleep(3)
    result = getDiskAllocatedToISCSI(tsm_ip, vol_mntPoint)
    if result[0] == 'PASSED' and vol_mntPoint in str(result[1]):
        logging.debug('iscsi logged device... %s', result[1][vol_mntPoint])
        device =  result[1][vol_mntPoint]
    else:
        return ['FAILED', 'Not able to get logged in device']
    time.sleep(5)
	
	#Getting device size and converting into GB
    quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device))
    quota1= int(quota[0])/(1024*1024*1024)
    return ['PASSED', quota1]

##....Method Description : Edit volume quota, 
##                         verifying on client whether size is updated.......##
def space_increase_iscsi(stdurl, tsmID, tsmIP, volname, volid, vol_iqn, vol_mntPoint):
    startTime = ctime()
    logout_result = iscsi_login_logout(vol_iqn, tsmIP, 'logout')
    if logout_result[0] == 'FAILED':
        logging.error('%s', logout_result[1])
    logging.debug('%s', logout_result[1])
    volList = listVolumeWithTSMId_new(stdurl, tsmID)
    endTime = ctime()
    if volList[0] == 'FAILED':
        logAndresult(tcName, 'BLOCKED', volList[1], startTime, endTime)
    get_volInfo = get_volume_info(volList[1], volname)
    vol_quota = get_volInfo[6]
    logging.debug('volume size is: %s', vol_quota)
    logging.info('Increasing space of Iscsi volume')
    vol_quota1 = vol_quota.strip('G')
    quota = int(vol_quota1) + 2
    quota = '%sG' %quota
    quota1 = quota.rstrip('G')
    edit_quota = edit_vol_quota(volid, quota, stdurl)
    if edit_quota[0] == 'FAILED':
	logAndresult(tcName, 'FAILED', edit_quota[1], startTime, endTime)
    logging.debug('Successfully updated quota of volume "%s" from %s to %s'\
			,volname, vol_quota, quota)
    get_quota = iscsi_get_quota(tsmIP, vol_iqn, vol_mntPoint)
    endTime = ctime()
    if get_quota[0] == 'FAILED':
    	logginig.error('After editting quota: %s', get_quota[1])
	logAndresult(tcName, 'BLOCKED', volList[1], startTime, endTime)
    quota2 = get_quota[1]
    quota3 = '%sG' %quota2
    logging.debug('Size of lun after quota update on client : %s',quota3)
    if float(quota2) == float(quota1):
    	logging.debug('Quota of iSCSI has been updated on client side ')
    else:
	msg = 'Size is not updated on client side, current size is : %s' %size
	logAndresult(tcName, 'FAILED', msg, startTime, endTime)
#******************************************************************************

#**************PREREQUSITES: POOL AND VSM CREATION*****************************

####-------------------------Pool creation---------------------------------####
startTime = ctime()
poolName = 'iPoolspace'
pool_paras = {'name': poolName, 'grouptype': pool_type, \
                        'iops': pool_iops}
pool_create =  pool_creation_flow(stdurl, pool_paras, no_of_disk, disk_type)
endTime = ctime()
if pool_create[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', pool_create[1], startTime, endTime)
logging.debug('Pool "%s" is created successfully', poolName)

####--------------------------Vsm creation---------------------------------####
startTime = ctime()
tsm_params = {'name': 'iTsmSpace', 'ipaddress': tsmIP, 'totaliops': pool_iops, \
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
account_id = tsmList[1][0].get('accountid')
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s', \
        tsmName, tsmID, datasetID)
#******************************************************************************

#***************************Volume Operations**********************************

####----------------------Volume Creation----------------------------------####
startTime = ctime()
vol = {'name': 'iscsiSpace' , 'tsmid': tsmID, 'datasetid': datasetID, \
     'protocoltype': 'ISCSI', 'iops': pool_iops, 'quotasize': '3G'}
volname = vol['name']
result = create_volume(vol, stdurl)
endTime = ctime()
if result[0] == 'FAILED':
    logAndresult(tcName, 'FAILED', result[1], startTime, endTime)
    #pass
logging.debug('"%s" was created successfully',volname)

####-----------Listing Volume and getting required details-----------------####
volList = listVolumeWithTSMId_new(stdurl, tsmID)
endTime = ctime()
if volList[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', volList[1], startTime, endTime)

get_volInfo = get_volume_info(volList[1], volname)
volid, vol_mntPoint, vol_iqn = get_volInfo[2], get_volInfo[3], get_volInfo[4]
vol_quota = get_volInfo[6]
logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_Iqn: %s',\
        volname, volid, vol_mntPoint, vol_iqn)
logging.debug('vol_quota: %s', vol_quota)

####------------Setting InitiatorGroup to All------------------------------####
startTime = ctime()
init_grp = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'ALL')
endTime = ctime()
if init_grp[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', init_grp[1], startTime, endTime)
logging.debug('Iscsi Initiator group is set to "ALL" for the volume')

####------------Mounting Iscsi volume--------------------------------------####
volume = {'TSMIPAddress' : tsmIP, 'mountPoint': volname, 'name' : volname}
mnt_iscsi = iscsi_mount_flow(volname, tsmIP, vol_iqn, vol_mntPoint, 'ext3')
endTime = ctime()
if mnt_iscsi[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', mnt_iscsi[1], startTime, endTime)
logging.debug('%s', mnt_iscsi[1])

device, iqn = mnt_iscsi[3], mnt_iscsi[2]

####------------UnMounting Iscsi volume------------------------------------####
umount_output = executeCmd('umount -l /dev/%s1' %device)
if umount_output[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and '\
            'increase the space', volname)
else:
    logging.debug('Iscsi volume %s umounted successfully', volname)

####----Loop: Increasing space multiple Times and verifying the same-------####
for x in range(1, 5):
    check_space = space_increase_iscsi(stdurl, tsmID, tsmIP, volname, volid, \
        vol_iqn, vol_mntPoint)
    time.sleep(5)
    logging.debug('The space increase process was successful for : %s time', x)
####--------------------Loop Ends------------------------------------------####
#******************************************************************************

#**********************Update result in result.csv*****************************
endTime = ctime()
resultCollection('%s, testcase is' %tcName, ['PASSED',' '], \
                startTime, endTime)
#******************************************************************************

#*************************Clear Configurations*********************************

####--------------------------Unmount lun----------------------------------####
mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
                             %(volume['name']))
mount_point = mount_point[0].strip('\n')
umount_other = UMain(mount_point)

umount_output = executeCmd('umount /dev/%s1' %device)
if umount_output[0] == 'FAILED':
    logging.error('Not able to umount %s, still go ahead and delete '\
        'the Iscsi volume', volname)
else:
    logging.debug('Iscsi volume %s umounted successfully', volname)

####---------------------Logout from session-------------------------------####
logout_result = iscsi_login_logout(iqn, tsmIP, 'logout')
if logout_result[0] == 'FAILED':
    logging.error('%s', logout_result[1])
logging.debug('%s', logout_result[1])

####------------Setting InitiatorGroup to None-----------------------------####
logging.info('Setting initiator group to "None"')
setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
if setNone[0] == 'FAILED':
    logging.error('Not able to set initiator group to None, do not delete volume')
    exit()
else:
    logging.debug('Initiator group is set to "none"')

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




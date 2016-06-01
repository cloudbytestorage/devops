# SMGLNSN
'''
###############################################################################################################
# Testcase Name : Provision and deprovision of Iscsi volume			                              #               
#                                                                                                             #
# Testcase Description : This test performs the following actions continuously for fixed set of iterations :  #
#                        a) Create iscsi volume                                                               #
#			 b) Expose lun to client and run IOs                                                  #
#                        b) Stop Ios and Umount the lun                                                       #
#                        c) delete the iscsi volume                                                           #
#                                                                                                             #
#                                                                                                             # 
# Testcase Pre-Requisites : Pool has to be created                                                            #
#                                                                                                             #
# Testcase Creation Date : 28/04/2016                                                                         #
#                                                                                                             #
# Testcase Last Modified : 28/04/2016                                                                         #  
#                                                                                                             #  
# Modifications made : None                                                                                   #  
#                                                                                                             #
# Testcase Author : Prathima                                                                                  #
###############################################################################################################
'''

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
    delete_volume, listVolumeWithTSMId_new
from utils import logAndresult, mountPointDetails, assign_iniator_gp_to_LUN, \
    iscsi_login_logout, iscsi_mount_flow, UMain
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

####**********************************START*********************************####
#testcase = 'Provisioning and deprovisioning of volumes (ISCSI)'
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
tsmIP = config['ipVSM2']
tsmInterface = config['interfaceVSM2']
acctName = config["AccountName"]
#******************************************************************************

#**************Pre-requisites: Pool and Vsm Creation***************************

####-------------------------Pool creation---------------------------------####
startTime = ctime()
poolName = 'iPoolPD'
pool_paras = {'name': poolName, 'grouptype': pool_type, \
            'iops': pool_iops}

pool_create = pool_creation_flow(stdurl, pool_paras, no_of_disk, disk_type)
endTime = ctime()
if pool_create[0] == 'FAILED':
    logAndresult(tcName, 'BLOCKED', pool_create[1], startTime, endTime)
logging.debug('%s', pool_create[1])

####--------------------------Vsm creation---------------------------------####
startTime = ctime()
tsm_params = {'name': 'iTsmPD', 'ipaddress': tsmIP, 'totaliops': pool_iops, \
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

#*********Loop: Create volume, expose to client, run IOs and delete volume*****
startTime = ctime()

for i in range(1, 6):
    ####----------------------Volume Creation------------------------------####
    vol = {'name': 'iscsiPD%s' %i, 'tsmid': tsmID, 'datasetid': datasetID, \
            'protocoltype': 'ISCSI', 'iops': pool_iops, 'quotasize': '5G'}
    volname = vol['name']
    result = create_volume(vol, stdurl)
    endTime = ctime()
    if result[0] == 'FAILED':
            logAndresult(tcName, 'FAILED', result[1], startTime, endTime)
    logging.debug('"%s" was created successfully',volname)
    logging.info('volume provision was successful for "%s times"', i)
    
    ####-----------Listing Volume and getting requried details-------------####
    volList = listVolumeWithTSMId_new(stdurl, tsmID)
    endTime = ctime()
    if volList[0] == 'FAILED':
        logAndresult(tcName, 'BLOCKED', volList[1], startTime, endTime)

    get_volInfo = get_volume_info(volList[1], volname)
    volid, vol_mntPoint, vol_iqn = get_volInfo[2], get_volInfo[3], get_volInfo[4]
    logging.debug('volname: %s, volid: %s, vol_mntPoint: %s, vol_Iqn: %s',\
            volname, volid, vol_mntPoint, vol_iqn)
    
    ####------------Setting Initiator group to All-------------------------####
    startTime = ctime()
    init_grp = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'ALL')
    endTime = ctime()
    if init_grp[0] == 'FAILED':
        logAndresult(tcName, 'BLOCKED', init_grp[1], startTime, endTime)
    logging.debug('Iscsi Initiator group is set to "ALL" for the volume')
    
    ####------------Mounting Iscsi volume----------------------------------####
    volume = {'TSMIPAddress' : tsmIP, 'mountPoint': volname, 'name' : volname}

    mnt_iscsi = iscsi_mount_flow(volname, tsmIP, vol_iqn, vol_mntPoint, 'ext3')
    endTime = ctime()
    if mnt_iscsi[0] == 'FAILED':
        logAndresult(tcName, 'BLOCKED', mnt_iscsi[1], startTime, endTime)
    logging.debug('%s', mnt_iscsi[1])
    device, iqn = mnt_iscsi[3], mnt_iscsi[2]
    
    ####------------Getting mount path-------------------------------------####
    mount_point =  getoutput('mount | grep %s | awk \'{print $3}\'' \
                        %(volume['name']))
    mount_point = mount_point[0].strip('\n')
    
    ####------------Execute Vdbench----------------------------------------####
    executeVdbenchFile(volume, 'filesystem_iscsi')
    check_vdbench = is_vdbench_alive(volname)
    time.sleep(1)
    while True:
        mountDetails = mountPointDetails('-m', mount_point)
        Used = mountDetails[2]
        if int(Used) >= 1000:
            logging.debug('vdbench has successfully created 1 GB file of the')
            logging.debug('going to stop vdbench after 10 seconds...')
            time.sleep(10)
            break
        check_vdbench = is_vdbench_alive(volname)
        if check_vdbench:
            continue
        else:
            logging.debug('vdbench has stopped unexpectedly....')
            break
    ####------------Kill Vdbench-------------------------------------------####
    kill_process(volname)
    logging.info('waiting for 10s')
    time.sleep(10)
    
    ####------------Unmount lun--------------------------------------------####
    umount_other = UMain(mount_point)
    umount_output = executeCmd('umount /dev/%s1' %device)
    logging.debug('%s', umount_output)
    if umount_output[0] == 'FAILED':
        logging.error('Not able to umount %s, still go ahead and delete '\
            'the Iscsi volume', volname)
    else:
        logging.debug('Iscsi volume %s umounted successfully', volname)
    
    ####------------Logout Session-----------------------------------------####
    logout_result = iscsi_login_logout(iqn, tsmIP, 'logout')
    if logout_result[0] == 'FAILED':
        logging.error('%s', logout_result[1])
    logging.debug('%s', logout_result[1])
    
    ####------------Setting Initiator group to None------------------------####
    logging.info('Setting initiator group to "None"')
    setNone = assign_iniator_gp_to_LUN(stdurl, volid, account_id, 'None')
    if setNone[0] == 'FAILED':
        endTime = ctime()
        msg = 'Not able to set initiator group to None, '\
                'hence not deleting volume'
        logAndresult(tcName, 'FAILED', msg, startTime, endTime)
        #exit()
    else:
        logging.debug('Initiator group is set to "none"')

    ####------------Volume Deletion----------------------------------------####
    delete_result = delete_volume(volid, stdurl)
    endTime = ctime()
    if delete_result[0] == 'FAILED':
        logAndresult(tcName, 'FAILED', delete_result[1], startTime, endTime)
    logging.debug('Volume "%s" deleted successfully', volname)
    logging.info('volume deprovision was successful for "%s times"', i)

#****************End of Loop***************************************************

#*****************************Update result************************************
endTime = ctime()
resultCollection('%s, testcase is' %tcName, ['PASSED',' '], \
                startTime, endTime)
#******************************************************************************

#***********************Clear Configurations***********************************

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

logging.info('----End of testcase "%s"----\n', tcName)

####***********************************END*********************************####

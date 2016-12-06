#This test case will cover iscsi LUN login with CHAP method
#Negative scenarrio has to be written, e.g. login with wrong credentials

#-----------------------------import start----------------------------
import os
import sys
import json
import time
import logging
from time import ctime
from tsmUtils import listTSMWithIP_new
from volumeUtils import create_volume, delete_volume, getDiskAllocatedToISCSI,\
        listVolumeWithTSMId_new
from utils import check_mendatory_arguments, is_blocked, get_logger_footer, \
        assign_iniator_gp_to_LUN, discover_iscsi_lun, iscsi_login_logout, \
        get_iscsi_device, add_auth_group, update_iscsi_services
from cbrequest import executeCmd, get_url, configFile, sendrequest, \
        resultCollection, getControllerInfo, get_apikey, executeCmdNegative,\
        getoutput
#-----------------------------import done-----------------------------

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

logging.info('-------iSCSI login with CHAP method test case started--------\n')
startTime = ctime()


#Global definations---------------------------------------------------
EXECUTE_SYNTAX = 'python iscsiWithCHAP.py conf.txt auth_groupName user(CHAP) '\
        'paswd(CHAP) user(MCHAP) paswd(MCHAP), init_groupName'
FOOTER_MSG = 'iSCSI login with CHAP method test case is completed'
BLOCKED_MSG = 'iSCSI login with CHAP method test case is blocked'
check_mendatory_arguments(sys.argv, 8, EXECUTE_SYNTAX, FOOTER_MSG, \
        BLOCKED_MSG, startTime)

fileName = '/etc/iscsi/iscsid.conf'
auth_groupName = sys.argv[2]
chap_userName = sys.argv[3]
chap_passwd = sys.argv[4]
mchap_userName = sys.argv[5]
mchap_passwd = sys.argv[6]
init_groupName = sys.argv[7]
conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
VSM_IP = conf['ipVSM1']
APIKEY = get_apikey(conf)
NODE1_IP = None

APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)
logging.debug('DEVMAN_IP: %s', DEVMAN_IP)
logging.debug('USER: %s', USER)
logging.debug('PASSWORD: %s', PASSWORD)
logging.debug('VSM_IP: %s', VSM_IP)
logging.debug('APIKEY: %s', APIKEY)
logging.debug('STDURL: %s', STDURL)
#Global definations done----------------------------------------------


#defining of local methods--------------------------------------------
def replace_text(fileName, sourceText, replaceText):
    print 'Source Text: ' +sourceText
    print 'Replace Text: ' +replaceText
    file = open('/etc/iscsi/iscsid.conf', 'r') #open the file in read mode
    text = file.read() #Reads the file and assigns the value to a variable
    file.close() #Closes the file (read session)
    file = open(fileName, "w") #Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText)) 
    #replaces all instances of our keyword and writes the whole output 
    #when done, wiping over the old contents of the file
    file.close() #Closes the file (write session)
    print sourceText +' replace with ' + replaceText

def get_sourceText(fileName, searchText):
    fp = open(fileName)
    sourceText = None
    for i, line in enumerate(fp):
        if '%s =' %(searchText) in line or '%s=' %(searchText) in line:
            #searching for the given string
            sourceText = line #getting entire line into sourceText
            #fp.close() #close the file
            isText = False
            continue
        else:
            continue
    fp.close() #close the file
    return sourceText

def verify_sourceText(sourceText):
    if sourceText is None:
        print 'There is no string as \"%s\" in file \"%s\"' \
                %(searchText, fileName)
        exit()
    else:
        sourceText = sourceText.strip('\n')
        return sourceText

def getTsmInfo(tsms):
    if tsms[0] == 'PASSED':
        tsm = tsms[1]
        return tsm[0].get('name'), tsm[0].get('id'), tsm[0].get('datasetid'), \
                tsm[0].get('controllerid'), tsm[0].get('accountname'), \
                tsm[0].get('hapoolname')
    logging.error('iSCSI login with CHAP method test case is blocked' \
            'due to %s', tsms[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_create_volume(result):
    if result[0] == 'PASSED':
        return
    logging.error('iSCSI login with CHAP method test case is blocked Volume '\
            'creation failed')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_list_volumes(volumes):
    if volumes[0] == 'PASSED':
        logging.debug('volumes listed successfullly')
        return volumes[1]
    logging.error('Not able to list volumes due to %s', volumes[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def get_vol_id(volumes, vol_name):
    volid = None
    voliqn = None
    accountid = None
    mntpoint = None
    for volume in volumes:
        if volume['name'] != vol_name:
            continue
        volid = volume.get('id')
        accountid = volume.get('accountid')
        voliqn = volume.get('iqnname')
        mntpoint = volume.get('mountpoint')
        break
    if volid is None or accountid is None or voliqn is None or mntpoint is None:
        logging.error('iSCSI login with CHAP method test case is blocked getting '\
                'volid: %s, accountid: %s, voliqn: %sand mntpoint: %s', \
                volid, accountid, voliqn, mntpoint)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return volid, voliqn, accountid, mntpoint

def verify_assign_init_gp(add_auth_group, auth_gp):
    if add_auth_group[0] == 'FAILED':
        logging.error('iSCSI login with CHAP method test case is blocked Not '\
                'able to assign auth group %s to LUN', auth_gp)
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)
    return

def verify_add_auth_group(result):
    if result[0] == 'PASSED':
        return
    logging.error('iSCSI login with CHAP method test case is blocked Not '\
            'able to add authentication group Error: %s', result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_update_iscsi_services(result):
    if result[0] == 'PASSED':
        return
    logging.error('iSCSI login with CHAP method test case is blocked Not '\
            'able to update iSCSI services, Error: %s', result[1])
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def take_backup(fileName, backup_filename):
    #taking backup of '/etc/iscsi/iscsid.conf' file...
    backup_filename = 'backup_%s' %(fileName.split('/')[-1])
    cmd = 'yes | cp %s %s' %(fileName, backup_filename)
    take_backup = executeCmd(cmd)
    if take_backup[0] == 'PASSED':
        print 'backup has been taken successfully'
        logging.debug('Successfully taken bakup of iscsid.conf')
    else:
        print 'Not able to take backup'
        print take_backup[1]
        logging.error('iSCSI login with CHAP method test case is blocked Not '\
                'able to take backup of iscsid.conf, Error: %s', take_backup[1])
        is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def modify_iscsi_configuration(fileName, chap_userName, chap_passwd):
    # starting of updating iscsid.conf file for CHAP authentication...
    searchText1 = 'node.session.auth.authmethod'
    sourceText1 = get_sourceText(fileName, searchText1)
    sourceText1 = verify_sourceText(sourceText1)
    # sourceText should be present to replace
    replaceText1 = 'node.session.auth.authmethod = CHAP'
    replace_text(fileName, sourceText1, replaceText1)

    searchText2 = 'node.session.auth.username'
    sourceText2 = get_sourceText(fileName, searchText2)
    sourceText2 = verify_sourceText(sourceText2)
    # sourceText should be present to replace
    replaceText2 = 'node.session.auth.username = %s' %(chap_userName)
    replace_text(fileName, sourceText2, replaceText2)

    searchText3 = 'node.session.auth.password'
    sourceText3 = get_sourceText(fileName, searchText3)
    sourceText3 = verify_sourceText(sourceText3)
    # sourceText should be present to replace
    replaceText3 = 'node.session.auth.password = %s' %(chap_passwd)
    replace_text(fileName, sourceText3, replaceText3)

    #Make system to read newly updated file
    executeCmd('service iscsid restart')
    #in some old machines above command will nor work, try with different command
    executeCmd('/sbin/iscsid restart')
    # updating iscsid.conf file has been done...

def verify_iqn(iqn):
    if iqn[0] == 'PASSED':
        return iqn[1]
    logging.debug('iSCSI login with CHAP method test case is blocked '\
            'getting iqn is None')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def verify_iscsi_device(iscsi_device, iqn, VSM_IP):
    if iscsi_device[0] == 'PASSED':
        device = iscsi_device[1]
        return device
    logging.debug('executing iscsi logout, since not able to get iscsi device')
    result = iscsi_login_logout(iqn, VSM_IP, 'logout')
    is_blocked(startTime, FOOTER_MSG, BLOCKED_MSG)

def make_iscsid_conf_original(backup_filename, fileName):
    #replacing iscsid.conf file with oriognal file...
    cmd = 'yes | cp %s %s' %(backup_filename, fileName)
    replace_backup_file = executeCmd(cmd)
    if replace_backup_file[0] == 'PASSED':
        print 'backup has been replaced successfully'
        logging.debug('iscsid.conf has been revert back to original file')
    else:
        print 'Not able to replace backup file'
        logging.error('Not able to revert iscsid.confi to original file, '\
                'please update it manually, Error: %s', replace_backup_file[1])
        print replace_backup_file[1]
    # replaced iscsid.conf file...
#defination of methods done-------------------------------------------


#getting TSM/VSM info-------------------------------------------------
logging.info('listing TSMs with IP...')
tsms = listTSMWithIP_new(STDURL, VSM_IP)
logging.info('getting tsm_name, tsm_id, and dataset_id...')
tsm_name, tsm_id, dataset_id, controllerid, accName, poolName = getTsmInfo(tsms)
logging.debug('tsm_name:%s, tsm_id:%s, dataset_id:%s, controllerid:%s, '\
        'accName:%s, poolName:%s', tsm_name, tsm_id, dataset_id, \
        controllerid, accName, poolName)
#TSM/VSM info part done-----------------------------------------------


#creating volume------------------------------------------------------
volumeDict = {'name': 'chapiSCSI1', 'tsmid': tsm_id, 'datasetid': \
        dataset_id, 'protocoltype': 'ISCSI', 'iops': 500}
result = create_volume(volumeDict, STDURL)
verify_create_volume(result)
logging.info('listing volume...')
volumes = listVolumeWithTSMId_new(STDURL, tsm_id)
volumes = verify_list_volumes(volumes)
vol_id, vol_iqn, account_id, mnt_point = get_vol_id(volumes, volumeDict['name'])
logging.debug('volume_id: %s, aacount_id: %s, mountpoint: %s and vol_iqn: %s', \
        vol_id, account_id, mnt_point, vol_iqn)
#volume creation done-------------------------------------------------


#creating iSCSI Authentication Group----------------------------------
result = add_auth_group(STDURL, account_id, auth_groupName, chap_userName, \
        chap_passwd, mchap_userName, mchap_passwd)
verify_add_auth_group(result)
#iSCSI Authentication Group created-----------------------------------


#creating iSCSI Initiator Group---------------------------------------
#variable name to create iniator group is 'init_groupName'
#has to write method for add new iniator group, as of now will use 'ALL'
#take the local clent iqn and create a iniator group 
#iSCSI Initiator Group created---------------------------------------

#Assigning Authentication Group to volume-----------------------------
services = {'auth_method': 'CHAP', 'auth_group': auth_groupName, ''\
        'init_group': init_groupName}
result = update_iscsi_services(STDURL, vol_id, account_id, services)
verify_update_iscsi_services(result)
#Authentication Group assign to volume--------------------------------


#update iscsid.con file-----------------------------------------------
#filename is a variable that contains iscsid.conf file
backup_filename = 'backup_%s' %(fileName.split('/')[-1])
take_backup(fileName, backup_filename)
modify_iscsi_configuration(fileName, chap_userName, chap_passwd)
#iscsid.conf updated--------------------------------------------------

#login iscsi LUN------------------------------------------------------
logging.debug('getting iqn for volume %s', volumeDict['name'])
iqn = discover_iscsi_lun(VSM_IP, vol_iqn)
iqn = verify_iqn(iqn)
logging.debug('iqn for discovered iSCSI LUN... %s', iqn)

login_result = iscsi_login_logout(iqn, VSM_IP, 'login')
endTime = ctime()
LUN_logged = True
if login_result[0] == 'PASSED':
    logging.debug('iSCSI login with CHAP method test case is passed...')
    resultCollection('iSCSI login with CHAP method test case is', \
            ['PASSED', ''], startTime, endTime)
else:
    LUN_logged = False
    logging.error('iSCSI login with CHAP method test case is failed Error:%s', \
            login_result[1])
    resultCollection('iSCSI login with CHAP method test case is', \
            ['FAILED', ''], startTime, endTime)

if LUN_logged:
    logging.debug('getting iSCSI LUN legged device...')
    time.sleep(2)
    result = getDiskAllocatedToISCSI(VSM_IP, mnt_point)
    print result
    logging.debug('iSCSI LUN logged in device: %s', result)
#---------------------------------------------------------------------

#updating iscsid.conf to original file--------------------------------
make_iscsid_conf_original(backup_filename, fileName)

#removing configuration-----------------------------------------------
logging.debug('iSCSI login CHAP execution done, removing configuration...')
if LUN_logged:
    iscsi_login_logout(iqn, VSM_IP, 'logout')

result = assign_iniator_gp_to_LUN(STDURL, vol_id, account_id, 'None')
if result[0] == 'PASSED':
    logging.debug('Go and delete the volume')
    delete_volume(vol_id, STDURL)
    get_logger_footer('iSCSI login with CHAP method test case is completed')
else:
    logging.error('Not able to set auth group to None, do not delete volume')
    get_logger_footer('iSCSI login with CHAP method test case is completed')
#configuration removed-------------------------------------------------------

import sys
import os
import json
import time
import logging
import subprocess
from time import ctime
from cbrequest import sendrequest, getoutput, executeCmd, getoutput_with_error,\
        resultCollection, getControllerInfoAppend
from volumeUtils import getDiskAllocatedToISCSI, mount_iscsi

#logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
#        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

def get_logger_footer(message):
    logging.info('----------- %s -------------', message)

def listGlobalSettings_param(stdurl):
    logging.info('Inside the Global setting update method...')
    querycommand = 'command=listConfigurations'
    rest_api = str(stdurl) + str(querycommand)
    listGlobalSettings_param = sendrequest(stdurl, querycommand)
    data = json.loads(listGlobalSettings_param.text)
    logging.debug('response for  global settings list: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['listglobalsettingsresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result
    else:
        global_config = data["listconfigurationsresponse"]["configuration"]
        result = ['PASSED', global_config]
        return result

#filePath = in which file u want to save output
def get_IOPS_values_from_node(datapath, node_ip, node_passwd, filePath):
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 1 ;'\
            'echo "-----------------";'\
            'reng stats access dataset %s qos | head -n 4' \
            %(datapath, datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_value = getControllerInfoAppend(node_ip, node_passwd, cmd, filePath)
    logging.debug('iops result is %s', (iops_value))
    return iops_value

#para can be -m or -h or any other parameter
def mountPointDetails(para, mountPoint):
    df = subprocess.Popen(["df", para, "%s" %(mountPoint)], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_output, std_error = df.communicate()
    if df.returncode != 0 or std_error:
        std_error = std_error.strip()
        return ['FAILED', std_error]
    std_output = ' '.join(std_output.splitlines()[1:])
    filesystem, size, used, available, percent, mountpoint = std_output.split()
    return [filesystem, size, used, available, percent, mountpoint]

def updateGlobalSettings(config_name , value, stdurl):
    logging.info('Inside the Global setting update method...')
    querycommand = 'command=updateConfiguration&name=%s&value=%s' \
            %(config_name, value)
    logging.info('updating the global setting : %s', config_name)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for global settings update: %s', str(rest_api))
    update_global = sendrequest(stdurl, querycommand)
    data = json.loads(update_global.text)
    logging.debug('response for  global settings update: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['updateconfigurationresponse'].get('errortext'))
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully updated global configuration']
        return result

def assign_iniator_gp_to_LUN(stdurl, vol_id, account_id, iniator_gp_name):
    #vol_id is volume id and iniator_gp_name is iniator group name
    #iniator_gp_name can be ALL, None, or whatever created by you
    querycommand = 'command=listVolumeiSCSIService&storageid=%s' %(vol_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listVolumeiSCSIService...%s', rest_api)
    logging.debug('executing sendrequest command...')
    resp_listVolumeiSCSIService = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listVolumeiSCSIService.text)
    logging.debug('listVolumeiSCSIService response...%s', data)
    if 'errorcode' in str(data):
        errormsg = str(data['listVolumeiSCSIServiceResponse'].get('errortext'))
        logging.error('Failed to list listiSCSIService due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result
    #iscsi_id as iscsi_service_id
    iscsi_id = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]['id']
    logging.debug('iscsi service id: %s', iscsi_id)
    ag_id = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]['ag_id']
    logging.debug('ag_id: %s', ag_id)
    unmap = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]['unmap']
    if unmap == True:
        unmap = 'true'
    else:
        unmap = 'false'
    logging.debug('unmap status: %s', unmap)
    physrecordlength = data['listVolumeiSCSIServiceResponse']['iSCSIService']\
            [0]['physrecordlength']
    logging.debug('physrecordlength: %s', physrecordlength)
    queuedepth = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]\
            ['queuedepth']
    logging.debug('queuedepth: %s', queuedepth)
    workerthreads = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]\
            ['workerthreads']
    logging.debug('workerthreads %s', workerthreads)
    querycommand = 'command=listiSCSIInitiator&accountid=%s' %(account_id)
    resp_api = str(stdurl) + str(querycommand)
    logging.debug('RESP API for listiSCSIInitiator...%s', resp_api)
    resp_listiSCSIInitiator = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listiSCSIInitiator.text)
    logging.debug('listiSCSIInitiator response...%s', data)
    if 'errorcode' in str(data):
        errormsg = str(data['listInitiatorsResponse']\
                ['initiator'].get('errortext'))
        logging.error('Failed to listiSCSIInitiator due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result
    initiators = data['listInitiatorsResponse']['initiator']
    initiator_id = None
    logging.info('getting initiator id...')
    for initiator in initiators:
        if initiator['name'] != iniator_gp_name:
            continue
        initiator_id = initiator['id']
        break
    if initiator_id is None:
        logging.error('Failed to take initiator id. Its None Please check '\
                'iniator group is correct')
        result = ['FAILED', 'Iniator group id is None, Please check iniator '\
                'group is correct']
        return result
    querycommand = 'command=updateVolumeiSCSIService&status=true&authmethod='\
            'None&authgroupid=%s&igid=%s&initialdigest=Auto&queuedepth=%s&'\
            'workerthreads=%s&unmap=%s&physrecordlength=%s&id=%s' \
            %(ag_id, initiator_id, queuedepth, workerthreads, unmap, \
            physrecordlength, iscsi_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for updateVolumeiSCSIService...%s', rest_api)
    resp_updateVolumeiSCSIService = sendrequest(stdurl, querycommand)
    data = json.loads(resp_updateVolumeiSCSIService.text)
    logging.debug('updateVolumeiSCSIService response...%s', data)
    if 'errorcode' in str(data):
        errormsg = str(data['updatingvolumeiscsidetails'].get('errortext'))
        logging.error('Failed to update updateVolumeiSCSIService due to: %s', \
                errormsg)
        result = ['FAILED', errormsg]
    else:
        logging.debug('iniator group <%s> added successfully to volume', \
                iniator_gp_name)
        result = ['PASSED', 'iniator group <%s> added successfully to volume' \
                %(iniator_gp_name)]
    return result

def discover_iscsi_lun(tsm_ip, vol_iqn):
    cmd = 'iscsiadm -m discovery -t st -p %s | grep %s | awk '\
            '{\'print $2\'}' %(tsm_ip, vol_iqn)
    logging.debug('executing command for discover iSCSI LUN: %s', cmd)
    iqn_name = getoutput_with_error(cmd)
    if iqn_name == []:
        result = ['FAILED', 'Not able to discover iSCSI LUN']
        logging.error('Not able to discover iSCSI LUN with iqn: %s, Error: '\
                '%s', vol_iqn, str(iqn_name))
        return result
    iqn = iqn_name[0].strip()
    result = ['PASSED', iqn]
    return result

def iscsi_login_logout(vol_iqn, vsm_ip, action):
    #action can be login and logout
    logging.info('inside the iscsi_login_logout method...')
    cmd = 'iscsiadm -m node --targetname %s --portal %s:3260 --%s' \
            %(vol_iqn, vsm_ip, action)
    logging.debug('executing command: %s', cmd)
    result = executeCmd(cmd)
    logging.debug('iscsi %s result: %s', action, result)
    return result
    
def get_iscsi_device():
    cmd = 'iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk '\
            '{\'print $4\'}'
    logging.info('getting iSCSI loggedin device name...')
    logging.debug('executing command... %s', cmd)
    time.sleep(1)
    result = getoutput(cmd)
    if result != 'null':
        #logging.debug('logged iscsi device: %s', (result[0].split('\n'))[0])
        result = ['PASSED', (result[-1].split('\n'))[0]]
        return result
    logging.error('Not getting iSCSI loggedin device')
    result = ['FAILED', '']
    return result

def execute_mkfs(device, version):
    #device where you want to write filesystem e.g sda, sdb, sdc
    #version means here for filesystem e.g. ext3, ext4 etc
    #for using this method make sure fdisk_response_file should be there
    logging.debug('creating the partion on device %s', device)
    cmd = 'fdisk /dev/%s < fdisk_response_file' %(device)
    logging.debug('command: %s', cmd)
    result = executeCmd(cmd)
    logging.debug('result for making partion: %s', result)
    logging.debug('writing %s on device %s', version, device)
    time.sleep(2)
    result = executeCmd('echo y | mkfs.%s /dev/%s1' %(version, device))
    if result[0] == 'PASSED':
        logging.debug('filesystem has been written successfully')
        result = ['PASSED', '']
    else:
        logging.error('Not able to write filesystem Error: %s', result)
        result = ['FAILED', result]
    return result


def mount_iscsi(device, vol_name):
    #this method will work only when you create a partion to your iscsi LUN
    executeCmd('mkdir -p mount/%s' %(vol_name))
    mount_result = executeCmd('mount /dev/%s1 mount/%s' %(device, vol_name))
    if mount_result[0] == 'PASSED':
        logging.debug('mounted %s at mount/%s successfully', vol_name, vol_name)
        return ['PASSED', '']
    logging.error('Not able to mount iscsi LUN: %s', mount_result)
    return ['FAILED', mount_result]



def copy_file(file_to_copy, dstntn_dir): #dstntn_dir is destination_directory
    logging.debug('inside copy_file method...')
    logging.debug('taking md5sum of %s...', file_to_copy)
    out =  getoutput('md5sum %s' %(file_to_copy))[0]
    md5_of_src_file = out.split(' ')[0]
    logging.debug('md5sum at source of %s:  %s', file_to_copy, md5_of_src_file)
    copy_result = executeCmd('cp %s %s/' %(file_to_copy, dstntn_dir))
    if copy_result[0] == 'FAILED':
        logging.error('Not able to copy file at directory %s', dstntn_dir)
        return ['FAILED', '']
    logging.debug('copied file to mounted directory successfully')
    out =  (getoutput('md5sum %s/%s' %(dstntn_dir, file_to_copy)))[0]
    md5_of_dstns_file = out.split(' ')[0]
    logging.debug('md5sum at destination of %s:  %s', file_to_copy, md5_of_dstns_file)
    if str(md5_of_src_file) == str(md5_of_dstns_file):
        logging.debug('md5sum check is passed')
        result = ['PASSED', md5_of_src_file]
    else:
        result = ['FAILED', 'md5sum is not same at source and destination']
        logging.error('Integrity check is failed: %s', result)
    return result

def get_node_ip(stdurl, controllerid):
    node_ip = None
    querycommand = 'command=listController&id=%s' %(controllerid)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listController... %s', rest_api)
    logging.debug('getting controllers IP...')
    resp_listController = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listController.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listControllerResponse']['errortext'])
        logging.error('Not able to get list controllers... %s', errormsg)
        return ['FAILED', '']
    node_ip = (data['listControllerResponse']['controller'][0]).get('ipAddress')
    if node_ip is not None:
        return ['PASSED', node_ip]
    logging.debug('Not able to get Node IP... %s')
    return ['FAILED', '']

def check_mendatory_arguments(argvs, numbers, syntax, footer_msg, blocked_msg, \
        startTime):
    #numbers means total parameters
    try:
        if len(argvs) < int(numbers):
            print 'Arguments are not correct, Please provide as follows...'
            print '%s' %(syntax)
            logging.error('Arguments are not correct, provide as follows...')
            logging.debug('%s', syntax)
            get_logger_footer('%s' %(footer_msg))
            exit()
    except ValueError:
        endTime = ctime()
        print 'Value for numbers is not integer'
        logging.error('Value for number of arguments is not integer ...')
        get_logger_footer('%s' %(footer_msg))
        resultCollection('%s' %blocked_msg, ['BLOCKED', ''], startTime, endTime)
        exit()
    return

def is_blocked(startTime, footer_msg, blocked_msg):
    endTime = ctime()
    get_logger_footer('%s' %(footer_msg))
    resultCollection('%s' %(blocked_msg), ['BLOCKED', ''], startTime, endTime)
    exit()

###testcase:'name of testcase'
###failed:'blocked/failed', parameter can be return value of fn or any thing
###parameter: result[1]
def logAndresult(testcase, failed, parameter, startTime, endTime):
    logging.debug('"%s" testcase is %s due to: "%s"', testcase, failed, parameter)
    logging.debug('----Ending script because this testcase is %s----\n', failed)
    resultCollection('"%s" testcase is ' %testcase, ['%s' %failed, ' '], \
            startTime, endTime)
    exit()

def deleteiscsiInitiatorGrp(stdurl, acc_id, grpName):
    querycommand = 'command=listiSCSIInitiator&accountid=%s'\
            %(acc_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listiSCSIInitiator...%s', rest_api)
    logging.debug('executing sendrequest command...')
    resp_listiSCSIInitiator = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listiSCSIInitiator.text)
    if 'initiator' in str(data):
        init = data['listInitiatorsResponse']['initiator']
        for initiator in init:
            if initiator['name'] == grpName:
                initID = initiator['id']
                querycommand = 'command=deleteiSCSIInitiator&accountid=%s&id=%s'\
                        %(acc_id, initID)
                rest_api = str(stdurl) + str(querycommand)
                logging.debug('REST API for deleteIscsiInitiator... %s', rest_api)
                resp_deliSCSIInitiator = sendrequest(stdurl, querycommand)
                data = json.loads(resp_deliSCSIInitiator.text)
                if 'errorcode' in str(data):
                    errormsg = data['deleteiscsiinitiatorResponse']['errortext']
                    print errormsg
                    logging.debug('%s' , errormsg)
                    result = ['FAILED', errormsg]
                    return result
                else:
                    print 'Deleted iscsiInitator Group %s' %grpName
                    logging.debug('Deleted iscsiInitator Group "%s"', grpName)
                    result = ['PASSED', 'Deleted iscsiInitator Group']
                    return result
        else:
            print 'Initiator group "%s" not present' %grpName
            logging.debug('iscsiInitator Group "%s" not present', grpName)
            result = ['FAILED', 'iscsiInitator Group not present']
            return result
    else:
        errormsg = data['listInitiatorsResponse']['errortext']
        logging.debug('%s' , errormsg)
        print errormsg
        result = ['FAILED', errormsg]
        return result

def check_alerts(stdurl, severity, search_string, category):
    #severity should be integer value, importance of alert
    #search_string should contain a sub-string of Description string of alerts
    #category: e.g. 'volume capacity', 'Messaging Service' etc
    logging.debug('Inside the check_alert method...')
    querycommand = 'command=listAlerts'
    resp_listAlerts = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listAlerts.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listalertsresponse'].get('errortext'))
        logging.debug('Not able to list alerts, Error: %s', errormsg)
        return ['FAILED', errormsg]
    alerts = data['listalertsresponse'].get('alert')
    isAlert = False
    isSeverity = False
    for alert in alerts:
        #this will change once we get the correct response as key value pair
        if '%s' %search_string in alert['subject'] and alert['description'] \
                == '%s' %category:
                    logging.debug('Got the alert for %s as: %s', category, \
                            alert['subject'])
                    isAlert = True
                    if alert['severity'] == int(severity):
                        logging.debug('Getting severity as: %s', \
                                alert['severity'])
                        isSeverity = True
                    else:
                        print 'Getting wrong severity alert for %s' %(category)
                        logging.error('Getting wrong severity for %s alert', \
                                category)
                        logging.info('Getting severity as: %s', \
                                alert['severity'])
    if isAlert and isSeverity:
        result = ['PASSED', 'Getting alert with expected severity for <%s>' \
                %(category)]
    elif isAlert and not isSeverity:
        result = ['FAILED', 'Getting alert with wrong severity for <%s>' \
                %(category)]
    else:
        result = ['FAILED', 'Not getting alert for <%s>' %(category)]
    return result

def add_auth_group(stdurl, account_id, goup_name, chapusername, chappassword, \
        mchapusername, mchappassword):
    logging.debug('Inside the add_auth_group method...')
    querycommand = 'command=addiSCSIAuthGroup&comment=AuthGoup&accountid=%s&'\
            'name=%s&chapusername=%s&chappassword=%s&mutualchapusername=%s&'\
            'mutualchappassword=%s' %(account_id, goup_name, chapusername, \
            chappassword, mchapusername, mchappassword)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for addiSCSIAuthGroup...%s', rest_api)
    logging.debug('executing sendrequest command...')
    resp_addiSCSIAuthGroup = sendrequest(stdurl, querycommand)
    data = json.loads(resp_addiSCSIAuthGroup.text)
    if 'errorcode' in str(data):
        errormsg = str(data['tsmiSCSIAuthGroupResponse'].get('errortext'))
        print errormsg
        logging.error('Error while adding Auth Group: %s', errormsg)
        result = ['FAILED', errormsg]
    else:
        logging.debug('iSCSI authentication group %s added successfully', 
                goup_name)
        result = ['PASSED', '']
    return result

def update_iscsi_services(stdurl, vol_id, account_id, services):
    #vol_id is volume id and services is a distionary that may contains...
    #Authentication Method, Discovery Authentication Group, Initiator Group
    #sample services dictionary will look like as follows...
    #{'auth_mathod': 'CHAP', 'auth_group': 'None/xyz', 'init_group': 'ALL/xyz'}
    auth_method = services.get('auth_method')
    auth_group = services.get('auth_group')
    init_group = services.get('init_group')

    querycommand = 'command=listVolumeiSCSIService&storageid=%s' %(vol_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listVolumeiSCSIService...%s', rest_api)
    logging.debug('executing sendrequest command...')
    resp_listVolumeiSCSIService = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listVolumeiSCSIService.text)
    logging.debug('listVolumeiSCSIService response...%s', data)
    if 'errorcode' in str(data):
        errormsg = str(data['listVolumeiSCSIServiceResponse'].get('errortext'))
        logging.error('Failed to list listiSCSIService due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result

    #getting old properties for iSCSI LUN-----------------------------------
    #iscsi_id as iscsi_service_id
    iscsi_id = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]['id']
    logging.debug('iscsi service id: %s', iscsi_id)
    
    unmap = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]['unmap']
    if unmap == True:
        unmap = 'true'
    else:
        unmap = 'false'
    logging.debug('unmap status: %s', unmap)
    physrecordlength = data['listVolumeiSCSIServiceResponse']['iSCSIService']\
            [0]['physrecordlength']
    logging.debug('physrecordlength: %s', physrecordlength)
    queuedepth = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]\
            ['queuedepth']
    logging.debug('queuedepth: %s', queuedepth)
    workerthreads = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]\
            ['workerthreads']
    logging.debug('workerthreads %s', workerthreads)
    #getting old properties for iSCSI LUN done-----------------------------
    

    #Authentication method part---------------------------------------------
    if auth_method is not None:
        pass
    else:
        auth_method = data['listVolumeiSCSIServiceResponse']['iSCSIService']\
                [0]['authmethod']
    #Authentication method part done----------------------------------------

    
    #Authentication group part----------------------------------------------
    if auth_group is None:
        ag_id = data['listVolumeiSCSIServiceResponse']['iSCSIService'][0]\
                ['ag_id']
        logging.debug('authgroup_id: %s', ag_id)
    else:
        querycommand = 'command=listiSCSIAuthGroup&accountid=%s' %(account_id)
        resp_api = str(stdurl) + str(querycommand)
        logging.debug('RESP API for listiSCSIAuthGroup...%s', resp_api)
        resp_listiSCSIAuthGroup = sendrequest(stdurl, querycommand)
        data2 = json.loads(resp_listiSCSIAuthGroup.text)
        logging.debug('listiSCSIAuthGroup response...%s', data2)
        if 'errorcode' in str(data2):
            errormsg = str(data2['listiSCSIAuthGroupResponse']\
                    ['authgroup'].get('errortext'))
            logging.error('Failed to listiSCSIAuthGroup due to: %s', errormsg)
            result = ['FAILED', errormsg]
            return result
        authgroups = data2['listiSCSIAuthGroupResponse']['authgroup']
        ag_id = None
        logging.info('getting authgroup id...')
        for authgroup in authgroups:
            if authgroup['name'] != auth_group:
                continue
            ag_id = authgroup['id']
            break
        if ag_id is None:
            logging.error('Failed to take authgroup id. Its None Please check '\
                    'authgroup is correct')
            result = ['FAILED', 'Authgroup id is None, Please check '\
                    'authgroup is correct']
            return result
        logging.debug('authgroup_id: %s', ag_id)
    #Authentication group part done-----------------------------------------


    #iniator group part-----------------------------------------------------
    if init_group is None:
        initiator_id = data['listVolumeiSCSIServiceResponse']['iSCSIService']\
                [0]['ig_id']
        logging.debug('initiator_group_id: %s', initiator_id)
    else:
        querycommand = 'command=listiSCSIInitiator&accountid=%s' %(account_id)
        resp_api = str(stdurl) + str(querycommand)
        logging.debug('RESP API for listiSCSIInitiator...%s', resp_api)
        resp_listiSCSIInitiator = sendrequest(stdurl, querycommand)
        data3 = json.loads(resp_listiSCSIInitiator.text)
        logging.debug('listiSCSIInitiator response...%s', data3)
        if 'errorcode' in str(data3):
            errormsg = str(data['listInitiatorsResponse']\
                    ['initiator'].get('errortext'))
            logging.error('Failed to listiSCSIInitiator due to: %s', errormsg)
            result = ['FAILED', errormsg]
            return result
        initiators = data3['listInitiatorsResponse']['initiator']
        initiator_id = None
        logging.info('getting initiator id...')
        for initiator in initiators:
            if initiator['name'] != init_group:
                continue
            initiator_id = initiator['id']
            break
        if initiator_id is None:
            logging.error('Failed to take initiator id. Its None Please check '\
                    'iniator group is correct')
            result = ['FAILED', 'Iniator group id is None, Please check '\
                    'iniator group is correct']
            return result
        logging.debug('initiator_group_id: %s', initiator_id)
        #iniator group part done---------------------------------------------

    querycommand = 'command=updateVolumeiSCSIService&status=true&authmethod='\
            '%s&authgroupid=%s&igid=%s&initialdigest=Auto&queuedepth=%s&'\
            'workerthreads=%s&unmap=%s&physrecordlength=%s&id=%s' \
            %(auth_method, ag_id, initiator_id, queuedepth, workerthreads, \
            unmap, physrecordlength, iscsi_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for updateVolumeiSCSIService...%s', rest_api)
    resp_updateVolumeiSCSIService = sendrequest(stdurl, querycommand)
    data = json.loads(resp_updateVolumeiSCSIService.text)
    logging.debug('updateVolumeiSCSIService response...%s', data)
    if 'errorcode' in str(data):
        errormsg = str(data['updatingvolumeiscsidetails'].get('errortext'))
        logging.error('Failed to update updateVolumeiSCSIService due to: %s', \
                errormsg)
        result = ['FAILED', errormsg]
    else:
        logging.debug('iSCSI services updated successfully to volume')
        result = ['PASSED', 'iSCSI services updated successfully to volume']
    return result

def add_initator_group(account_id, initGrpName, InitIqn, ntw, stdurl):
    logging.debug('Inside the add_initiator_group method...')
    querycommand = 'command=addiSCSIInitiator&accountid=%s&name=%s&'\
        'initiatorgroup=%s&netmask=%s' \
        %(account_id, initGrpName, InitIqn, ntw)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for addiSCSI_initatorGroup...%s', rest_api)
    resp_addiSCSIAuthGroup = sendrequest(stdurl, querycommand)
    data = json.loads(resp_addiSCSIAuthGroup.text)
    logging.debug('Response for addiSCSI_initatorGroup : %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['tsmiSCSIInitiatorResponse'].get('errortext'))
        print errormsg
        result = ["FAILED", errormsg]
        return result
    else:
        result = ['PASSED', 'Added initiator group "%s" successfully' \
                                %initGrpName]
        return result

def iscsi_mount_flow(volname, tsm_ip, vol_iqn, vol_mntPoint, fs_type):
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
    fs = execute_mkfs(device, fs_type)
    if fs[0] == 'FAILED':
        return ['FAILED', fs[1]]
    logging.debug('file system "%s" has been written successfully on the lun')
    mnt_lun = mount_iscsi(device, volname)
    if mnt_lun[0] == 'FAILED':
        return ['FAILED', mnt_lun[1]]
    return ['PASSED', 'Successfully mounted iscsi volume "%s"' %volname, \
            discover_lun[1], device]

#used for remount, if quota is changed...
def iscsi_remount_flow(volname, tsm_ip, vol_iqn, vol_mntPoint, fs_type):
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
    fs = executeCmd('fdisk /dev/%s < fdisk_response_file2' %(device))
    time.sleep(5)
    quota=getoutput('fdisk -l | grep /dev/%s: |  awk {\'print $5\'}' %(device))
    quota1= int(quota[0])/(1024*1024*1024)
    
    mkfs_result = executeCmd('echo y | mkfs.%s /dev/%s2' %(fs_type, device))
    if mkfs_result[0] == 'FAILED':
        return ['FAILED', mkfs_result[1]]
    logging.debug('file system "%s" has been written successfully on the lun')
    executeCmd('mkdir -p mount/%s' %vol_mntPoint)
    executeCmd('mkdir -p expand/')
    mount_result1 = executeCmd('mount /dev/%s1 mount/%s' %(device, volname))
    mount_result2 = executeCmd('mount /dev/%s2  expand/' %device)
    if mount_result1[0] == 'FAILED' and mount_result2[0] == 'FAILED':
        return ['FAILED',mount_result[1], mount_result2[1]]
    return ['PASSED', 'Successfully mounted iscsi volume "%s"' %volname, \
            discover_lun[1], device, quota1]


from time import ctime
import time
import sys
import os
import json
import logging
from cbrequest import sendrequest, queryAsyncJobResult
from poolUtils import listPool, get_pool_info
from accountUtils import create_account, get_account_info, listAccount_new


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

def get_tsm_default_params():
    tsm_def_params = {'name': '', 'accountid': '', 'poolid': '', \
            'ipaddress': '', 'quotasize': '1T', 'blocksize': '4k', \
            'latency': 15, 'totaliops': 5000, 'totalthroughput': 20000, \
            'graceallowed': 'true', 'subnet': 8, 'tntinterface': '', \
            'dnsname': 'cloudbyte.com', 'dnsserver': '8.8.8.8', \
            'gracecontrol': 'false', 'iopscontrol': 'true', \
            'tpcontrol': 'true', 'backuptpcontrol': 'false', \
            'totalbackupthroughput': 0}
    return tsm_def_params

def form_querycommand(command, final_tsmParams):
    querycommand = '%s' %(command)
    for key, value in final_tsmParams.iteritems():
        querycommand = querycommand + '&%s=%s' %(key, value)
    return querycommand

def modify_params(tsm_def_params, user_tsm_params):
    for key in user_tsm_params:
        if key in tsm_def_params:
            tsm_def_params[key] = user_tsm_params[key]
            if key == 'totaliops':
                throughput = int(user_tsm_params[key]) * 4
                tsm_def_params['totalthroughput'] = throughput
    return tsm_def_params

def listTSM_new(stdurl):
    querycommand = 'command=listTsm'
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for Listing Tsm: %s', str(rest_api))
    resp_listTsm = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listTsm.text)
    logging.debug('response for Listing Tsm: %s', str(data))
    if not 'errorcode' in str(data['listTsmResponse']):
        if 'listTsm' in data['listTsmResponse']:
            tsms = data['listTsmResponse']['listTsm']
            result = ['PASSED', tsms]
            return result
        else:
            result = ['BLOCKED', 'There is no VSMs']
            return result
    else:
        errormsg = str(data['listTsmResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('Not able to List Tsm due to: %s', errormsg)
        return result

def listTSMWithIP_new(stdurl, tsm_ip):
    querycommand = 'command=listTsm&ipaddress=%s' %(tsm_ip)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for Listing Tsm with IP: %s', str(rest_api))
    resp_listTsm = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listTsm.text)
    logging.debug('response for Listing Tsm with IP: %s', str(data))
    if not 'errorcode' in data['listTsmResponse']:
        if 'listTsm' in data['listTsmResponse']:
            tsms = data['listTsmResponse']['listTsm']
            result = ['PASSED', tsms]
            return result
        else:
            result = ['BLOCKED', 'There is no VSMs with IP: %s' %(tsm_ip)]
            return result
    else:
        errormsg = str(data['listTsmResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('Not able to List Tsm for given IP due to: %s', errormsg)
        return result

###list_tsm will be o/p of listTSMWithIP_new(stdurl, tsm_ip)
def get_tsm_info(list_tsm):
    for listTsm in list_tsm:
        tsm_id = listTsm.get('id')
        tsm_name = listTsm.get('name')
        dataset_id = listTsm.get('datasetid')
        tsm_iops = listTsm.get('iops')
        tsm_quota = listTsm['storageBuckets'][0].get('quota')
        result = [tsm_id, tsm_name, dataset_id, tsm_iops, tsm_quota]
        return result

###mandatory paramrs for user_params [name, accID, poolID, IP, interface] 
def create_tsm(user_params, stdurl):
    logging.info('inside create_tsm method...')
    logging.debug('getting default parameters for creating tsm')
    tsm_def_params = get_tsm_default_params()
    logging.debug('default parameters for creating tsm: %s', str(tsm_def_params))
    logging.debug('getting final parametrs for creating tsm')
    final_tsm_params = modify_params(tsm_def_params, user_params)
    logging.debug('final parameters for creating tsm: %s', str(final_tsm_params))
    command = 'command=createTsm'
    querycommand = form_querycommand(command, final_tsm_params)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for creating tsm: %s', (rest_api))
    logging.info('Executing command sendrequest...')
    resp_addTsm = sendrequest(stdurl, querycommand)
    data = json.loads(resp_addTsm.text)
    logging.debug('response for creating TSM: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['addTsmResponse']['errortext'])
        logging.error('Not able to create Tsm due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result
    job_id = data['addTsmResponse']['jobid']
    logging.debug('create Tsm job id: %s', job_id)
    logging.info('calling queryAsyncJobResult method...')
    create_tsm_status = queryAsyncJobResult(stdurl, job_id)
    if create_tsm_status[0] == 'PASSED':
        result = ['PASSED', 'TSM created successfuly']
        return result
    else:
        result = ['FAILED', create_tsm_status]
        logging.debug('result of create_tsm: %s', str(result))
        return result

def delete_tsm(tsm_id, stdurl):
    logging.info('Inside  delete tsm method...')
    querycommand = 'command=deleteTsm&id=%s' %(tsm_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for deleting TSM: %s', str(rest_api))
    resp_deleteTsm = sendrequest(stdurl, querycommand)
    data = json.loads(resp_deleteTsm.text)
    logging.debug('response for deleting tsm: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['deleteTsmResponse']['errortext'])
        print errormsg
        result = ['FAILED', 'Not able to delete tsm due to: %s', errormsg]
        logging.error('Not able to delete tsm due to: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully deleted Tsm']
        return result

def editTsmQuota(dataset_id, quota, stdurl):
    logging.info('Editing tsm quota method..')
    querycommand = 'command=updateStorage&id=%s&quotasize=%s' %(dataset_id, quota)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for editing tsm quota: %s', str(rest_api))
    edit_tsmQuota = sendrequest(stdurl, querycommand)
    data = json.loads(edit_tsmQuota.text)
    logging.debug('response for editing tsm quota: %s', str(data))
    if 'errorcode' in data['updatedatasetresponse']:
        errormsg = str(data['updatedatasetresponse']['errortext'])
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully updated TSM quota size']
        return result

def editTsmIOPS(tsm_id, iops, stdurl):
    logging.info('Editing tsm iops method..')
    throughput = iops * 4
    querycommand = 'command=updateTsm&id=%s&iops=%s&throughput=%s' \
            %(tsm_id, iops, throughput)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for editing tsm IOPS: %s', str(rest_api))
    edit_tsmIops = sendrequest(stdurl, querycommand)
    data = json.loads(edit_tsmIops.text)
    logging.debug('response for editing tsm IOPS: %s', str(data))
    if 'errorcode' in data['updateTsmResponse']:
        errormsg = str(data['updateTsmResponse']['errortext'])
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully updated TSM IOPS value']
        return result

def editNFSthreads(tsm_id, threads, stdurl):
    logging.info('Editing NFS thread value method...')
    querycommand = 'command=updateTsmNfsOptions&tsmid=%s&nfsworkerthreads=%s' \
                    %(tsm_id, threads)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for editing tsm IOPS: %s', str(rest_api))
    resp_threadUpdate = sendrequest(stdurl, querycommand)
    data = json.loads(resp_threadUpdate.text)
    logging.debug('response for editing NFS threads: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['updateTsmNfsOptionsResponse']['errortext'])
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully updated thread value']
        return result

def updateTsmIP(tsm_id, tsm_new_IP, stdurl):
    logging.info('Inside Tsm IP update method...')
    querycommand='command=updateTsmSettings&tsmid=%s&primaryipaddress=%s'\
                    '&defaultrouter=0'  %(tsm_id, tsm_new_IP)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for editing tsm IOPS: %s', str(rest_api))
    resp_IPUpdate = sendrequest(stdurl, querycommand)
    
    # Workaround for the bug where fake_fs sysctl for jails is set at 1
    #time.sleep(60)

    data = json.loads(resp_IPUpdate.text)
    logging.debug('response for updating Tsm IP: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['updateTsmDnsSettingsResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully Updated Tsm IP']
        return result

#tsm_params dict must have : name, tsm ip, interface
#other params are optional
#from this method passing pool_id & acct_id to dict
def tsm_creation_flow(stdurl, poolName, acctName, tsm_params):
    #pool details
    list_pool = listPool(stdurl)
    if list_pool[0] == 'FAILED':
        return ['FAILED', list_pool[1]]
    pool_info = get_pool_info(list_pool[1], poolName)
    if pool_info[0] == 'FAILED':
        return ['FAILED', pool_info[1]]
    pool_id = pool_info[1]
    logging.debug('Pool id of pool "%s" is: %s', poolName, pool_id)
    #account details
    account_creation = create_account(acctName, stdurl)
    if account_creation[0] == 'FAILED' and 'already exists' in str(account_creation[1]):
        logging.debug('Account already exist, taking its details..')
    elif account_creation[0] == 'FAILED':
        return ['FAILED', account_creation[1]]
    logging.debug('"%s" Account created successfully', acctName)
    list_acct = listAccount_new(stdurl)
    if list_acct[0] == 'FAILED':
        return ['FAILED', list_acct[1]]
    get_accInfo =  get_account_info(list_acct[1], acctName)
    if get_accInfo[0] == 'FAILED':
        return ['FAILED', get_accInfo[1]]
    acct_id = get_accInfo[1]
    logging.debug('Account Id of account "%s" is: %s', acctName, acct_id)
    #tsm details
    req_ids = {'poolid': pool_id, 'accountid': acct_id}
    final_tsm_params = dict(tsm_params.items() + req_ids.items())
    logging.debug('final_tsm_params : %s', final_tsm_params)
    tsm_creation =  create_tsm(final_tsm_params, stdurl)
    if tsm_creation[0] == 'FAILED':
        return ['FAILED', tsm_creation[1]]
    return ['PASSED', 'Tsm "%s" created successfully' %(tsm_params['name'])]


#verify tsmIP whether used or not given in config file
def verify_tsmIP_from_configFile(config, stdurl):
    for x in range(1,6):
        tsmIP = config["ipVSM%s" %x]
        tsmInterface = config["interfaceVSM%x" %x]
        tsmList = listTSMWithIP_new(stdurl, tsmIP)
        if 'There is no VSMs' in tsmList[1]:
            logging.info('Taking "%s" as tsm IP, to create tsm', tsmIP)
            return ['PASSED', tsmIP, tsmInterface]
        else:
             logging.debug('"%s" IP is already used, hence getting another IP', tsmIP)
    else:
        logging.info('Checking extra IP if given in config file')
        msg = 'All the given tsm IP in config file are used, '\
                'Please specify unused IP'
        return ['FAILED', msg]


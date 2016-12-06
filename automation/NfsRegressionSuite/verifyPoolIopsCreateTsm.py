import os
import sys
import time
import json
import logging
import subprocess
from cbrequest import *
from tsmUtils import *
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

logging.info('-----Verify pool IOPS and creting TSM------')
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])
accName = config['AccountName']
print accName

###Create Account
querycommand = 'command=createAccount&name=%s&description=None' %(accName)
logging.info('Creating Account "%s"', accName)
resp_createAccount = sendrequest(stdurl, querycommand)
data = json.loads(resp_createAccount.text)
if 'errorcode' in str(data):
    errormsg = data['createaccountresponse']['errortext']
    print errormsg
    logging.debug('%s', errormsg)
else:
    print '%s created successfully' %accName

querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
data = json.loads(resp_listAccount.text)
accounts = data["listAccountResponse"]["account"]
for account in accounts:
    if account['name'] == accName:
        logging.info('Getting account id of "%s"', accName)
        account_id = account['id']
        logging.debug('Account_id : %s', account_id)
        break

querycommand = 'command=listHAPool'
logging.info('listing pool')
resp_listHAPool = sendrequest(stdurl,querycommand)
data = json.loads(resp_listHAPool.text)
hapools = data["listHAPoolResponse"]["hapool"]

logging.info('getting pool name, availableIOPS, totalIOPS and its ID')
availIOPS = hapools[0]['availIOPS']
poolName = hapools[0]['name']
poolID = hapools[0]['id']
poolIOPS = hapools[0]['totaliops']
logging.debug('Pool_name:%s ,pool_Id:%s, pool_totalIOps:%s, pool_availableIOPS:%s',\
        poolName, poolID, poolIOPS, availIOPS)

for avail in hapools:
    if availIOPS >= avail['availIOPS']:
        #logging.info('pool available iops is enough to create tsm')
        pass
    else:
        availIOPS = avail['availIOPS']
        poolName = avail['name']
        poolID = avail['id']
        poolIOPS = avail['totaliops']

if availIOPS <= 5000:
    iops = poolIOPS + 5000
    logging.info('Increasing iops of pool %s', poolName)
    logging.debug('Now totalIOPS will be : %s', iops)
    throughput = iops * 128
    print throughput, iops
    querycommand = 'command=updateHAPool&id=%s&ispooltakeoveronpartialfailure=true'\
        '&totaliops=%s&totalthroughput=%s&graceallowed=true&deduplication=off&'\
        'readmultiplicationfactor=4&penaltyenforcementfactor=no&avgblocksize=4&'\
        'revisionnumber=1&response=json' %(poolID, iops, throughput)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('Pool IOPS upadate rest api : %s', rest_api)
    edit_poolIops = sendrequest(stdurl, querycommand)
    data = json.loads(edit_poolIops.text)
    if 'errorcode' in str(data):
        errormsg = str(data['updateHAPoolResponse']['errortext'])
        print errormsg
        logging.debug('%s', errormsg)
        logging.debug('---------Ending script pool update failed----')
        exit()
    else:
        print 'Pool IOPS updated Successfully'
        logging.info('Pool updated successfully')

for x in range(1, 6):
    tsm = {'name' : 'pTSM%d' %x, 'ipaddress': config["ipVSM%d" %x] , \
        'accountid': account_id, 'poolid': poolID, \
        'tntinterface': config["interfaceVSM%d" %x]}
    createTsm = create_tsm(tsm, stdurl)
    if 'FAILED' in createTsm:
        print createTsm[1]
        #exit()
    else:
        print "%s created successully" %tsm['name']
        logging.debug("%s created successully", tsm['name'])
logging.info('--------successfully update pool and created tsm, ending script-------')

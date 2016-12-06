import sys
import os
import json
import logging
import subprocess
from time import ctime
import time
from cbrequest import sendrequest

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
    filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

def listAccount_new(stdurl):
    querycommand = 'command=listAccount' 
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for Listing account: %s', str(rest_api))
    resp_listAccount = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listAccount.text)
    logging.debug('response for Listing Account: %s', str(data))
    if 'account' in str(data["listAccountResponse"]):
        accounts = data["listAccountResponse"]["account"]
        result = ['PASSED', accounts]
        return result
    elif not 'errorcode' in str(data["listAccountResponse"]):
        print 'There is no account'
        result = ['BLOCKED', 'There is no account to list']
        return result
    else:
        errormsg = str(data["listAccountResponse"].get("errortext"))
        result = ['FAILED', errormsg]
        return result

###list_acct = listAccount_new(stdurl)
def get_account_info(list_acct, acct_name):
    for account in list_acct:
        if acct_name == account.get('name'):
            acct_id = account.get('id')
            return ['PASSED', acct_id]
    else:
        return ['FAILED', 'Not able to find account']

def create_account(account_name, stdurl):
    logging.info('inside create_ccount method...')
    querycommand = 'command=createAccount&name=%s&description=None' %(account_name)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for creating tsm: %s', (rest_api))
    resp_createAccount = sendrequest(stdurl, querycommand)
    data = json.loads(resp_createAccount.text)
    logging.debug('response for creating Account: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['createaccountresponse'].get('errortext'))
        print errormsg
        return ['FAILED', errormsg]
    else:
        return ['PASSED', 'Successfully created account']

def delete_account(acct_id, stdurl):
    logging.info('Inside the delete account method...')
    querycommand = 'command=deleteAccount&id=%s' %(acct_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for deleting Account: %s', str(rest_api))
    resp_deleteAccount = sendrequest(stdurl, querycommand)
    data = json.loads(resp_deleteAccount.text)
    logging.debug('response for deleting Account: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['deleteAccountResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', 'Not able to delete Account due to: %s', errormsg]
        logging.error('Not able to delete Account due to: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully deleted Account']
        return result
    localClientIP = getoutput("ifconfig %s | grep 'inet ' | awk '{print $2}' "\
                         "| sed -e s/.*://" %interface)
    localClientIP = localClientIP[0].rstrip('\n')
    return ['PASSED', localClientIP]

def get_account_id(stdurl, account_name):
    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listAccount.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listAccountResponse'].get('errortext'))
        print 'Not able to get accounts, Error: %s' %(errormsg)
        logging.error('Not able to get accounts, Error: %s', errormsg)
        return ['FAILED', errormsg]
    accounts = data['listAccountResponse'].get('account')
    if accounts is None:
        print 'There is no Accounts to list...'
        logging.debug('There is no Accounts to list, please create account '\
                'and procede...')
        return ['BLOCKED', 'There is no Accounts...']
    isAccount = False
    for account in accounts:
        if account_name is None:
            account_id = account['id']
            return ['PASSED', account_id]
        elif account['name'] == account_name:
            account_id = account['id']
            return ['PASSED', account_id]
        else:
            continue
    if not isAccount:
        return ['BLOCKED', 'There is no account with given name']
#### Function(s) Declartion Ends

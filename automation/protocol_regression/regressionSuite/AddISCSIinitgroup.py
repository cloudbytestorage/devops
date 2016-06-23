import json
import sys
import time
from time import ctime
from cbrequest import *
from volumeUtils import *
from utils import *
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
        filename='logs/automation_execution.log',filemode='a',level=logging.DEBUG)

logging.info('---Start of script "AddISCSIinitgroup.py"---')
if len(sys.argv)<2:
    print "Argument are not correct, Please provide as follows"
    print "python AddISCSIinitgroup.py conf.txt "
    logging.debug('--------Ending script because of parameter mismatch--------')
    exit()

logging.info("Establish connection to EC ")
conf = configFile(sys.argv);
apikey = get_apikey(conf)
stdurl = get_url(conf, apikey[1])
tsmIP = conf['ipVSM1']
logging.info("fetching apikey and stdurl was successful") 
name = 'InitGroup'
iqn  = getoutput('cat /etc/iscsi/initiatorname.iscsi '\
             '| grep iqn | cut -d  "=" -f 2')
iqn = iqn[0].rstrip('\n')
logging.info('Getting local client IP')
localClientIP = get_ntwInterfaceAndIP(tsmIP)
if 'FAILED' in localClientIP:
    endTime = ctime()
    print localClientIP[1]
    logAndresult(testcase, 'BLOCKED', localClientIP[1], startTime, endTime)
else:
    localClientIP = localClientIP[1]
    logging.debug('local client IP : "%s"', localClientIP)

network = "%s/8" %localClientIP

startTime = ctime()
############Fetch Account ID.
logging.info("Listing Account ID")
def getAccountID(accounts):
    accountId = None
    for account in accounts:
        accountId = account['id']
        break
    return accountId
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
data = json.loads(resp_listAccount.text)
accounts = data['listAccountResponse']['account']
accountId = getAccountID(accounts)
if accountId is not None:
    print accountId
    logging.info('Accounts present with accountId %s', accountId)
     
    
######## Add Iscsi Auth group.
querycommand = 'command=addiSCSIInitiator&accountid=%s&name=%s&initiatorgroup=%s&netmask=%s' \
            %(accountId, name, iqn, network) 
logging.debug("Addition of ISCSIAuthgroup is on progress : %s", querycommand)
resp_addiSCSIInitiator = sendrequest(stdurl, querycommand)
data = json.loads(resp_addiSCSIInitiator.text)
if 'errorcode' in str(data):
    errormsg = str(data["tsmiSCSIInitiatorResponse"]["errortext"])
    logging.error("Failed to add ISCSI initiator group : %s", errormsg)
    endTime = ctime()
    resultCollection('Failed to add Iscsi initiator group', \
            ['FAILED', errormsg], startTime, endTime)
    exit()
else:
    logging.info('Sucessfully Added AuthGroup %s', name)
    endTime = ctime()
    resultCollection('Adding iscsi initiator group was sucessful', \
                                     ['PASSED', ''], startTime, endTime)
logging.info('---END of script "AddISCSIinitgroup.py"---')





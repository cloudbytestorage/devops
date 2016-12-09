import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, executeCmd, getoutput, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print " python createISCSIInitiatorGroup.py config.txt  clientip"
    exit()

ip = sys.argv[2]
initname = "iqn"

#iqn = sys.argv[2]
#ip = sys.argv[3]
###initiator name

###get clients iqn
#if iqn == "system_iqn":
iqn = getoutput('cat /etc/iscsi/initiatorname.iscsi | grep iqn | cut -d "=" -f 2')
iqn = iqn[0].strip()
print iqn

###get clients ip
#if ip == "system_ip":
#ip = getoutput('ifconfig eth0 | grep "inet addr:" | cut -d ":" -f 2 | awk \'{ print $1}\'')
#ip = ip[0].strip()
print ip

### list of accounts
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/ListAccount.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)
#print data
accounts = data['listAccountResponse']['account']


for x in range(1, int(config['Number_of_Accounts'])+1):
    startTime = ctime()
    for account in accounts:
        if account['name']  == "%s" %(config['accountName%d' %(x)]):
            acc_id = account['id']
            initname = initname + "%d" %(x)
            ### creating iscsi initiator group 
            querycommand = 'command=addiSCSIInitiator&accountid=%s&name=%s&initiatorgroup=%s&netmask=%s' %(acc_id, initname, iqn, ip+"%2F8")
            resp_tsmiSCSIInitiatorResponse = sendrequest(stdurl, querycommand)
            filesave("logs/tsmiSCSIInitiatorResponse.txt", "w", resp_tsmiSCSIInitiatorResponse)
            data = json.loads(resp_tsmiSCSIInitiatorResponse.text)
            endTime = ctime()
            if not "errortext" in str(data):
                resultCollection("sucessfully created iscsi initiator group \'%s\' in %s" %(initname,account['name']), ["PASSED"," "], startTime, endTime)
            else:
                errorstatus= str(data['tsmiSCSIInitiatorResponse']['errortext'])
                resultCollection("failed to created iscsi initiator group \'%s\' in %s" %(initname,account['name']), ["FAILED",errorstatus], startTime, endTime)        


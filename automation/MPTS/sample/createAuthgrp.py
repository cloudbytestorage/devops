import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, executeCmd, getoutput, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

if len(sys.argv) < 2:
    print "Argument is not correct.. Correct way as below"
    print " python createAuthgrp.py config.txt" 
    exit()

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
            authgrp_name = "AuthGrp" + "%d" %(x)
            comment = "Auth%20Group%20Info."
            querycommand = 'command=addiSCSIAuthGroup&accountid=%s&name=%s&comment=%s&chapusername=ChapUser&chappassword=ChapPassword&mutualchapusername=MutualUser&mutualchappassword=MutualPassword' %(acc_id, authgrp_name, comment)
            resp_tsmiSCSIAuthGroupResponse = sendrequest(stdurl, querycommand)
            filesave("logs/tsmiSCSIAuthGroupResponse.txt", "w", resp_tsmiSCSIAuthGroupResponse)
            data = json.loads(resp_tsmiSCSIAuthGroupResponse.text)
            endTime = ctime()
            if not "errortext" in str(data):
                resultCollection("sucessfully created iscsi authentication group in %s" %account['name'], ["PASSED"," "], startTime, endTime)
            else:
                errorstatus= str(data['tsmiSCSIAuthGroupResponse']['errortext'])
                resultCollection("failed to created iscsi authentication group in %s" %account['name'], ["FAILED",errorstatus], startTime, endTime)


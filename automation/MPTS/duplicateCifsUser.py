import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/listAccount.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)
accountName = "%s" %(config['accountName1'])
account_id = None
flag = 0
#error_cause = ''
if not 'errorcode' in data['listAccountResponse']:
    startTime = ctime()
    accounts = data['listAccountResponse']['account']
    for account in accounts:
        if account['name'] == accountName:
            account_id = account['id']
            break
    if account_id is not None:
        AuthName = 'testAuthGroup'
        user = 'testuser1'
        password = user
        time.sleep(1)
        querycommand = 'command=addCIFSAuthGroup&accountid=%s&name=%s&comment=%s&username=%s&password=%s&fullname=%s' %(account_id, AuthName,"Comment",user,password,"fullname")
        resp_tsmcifsauthgroupresponse = sendrequest(stdurl,querycommand)
        filesave("logs/AccountDuplicateUserCreation.txt","w",resp_tsmcifsauthgroupresponse)
        data = json.loads(resp_tsmcifsauthgroupresponse.text)
        if not "errortext" in data["tsmcifsauthgroupresponse"]:
            endTime = ctime()
            print "AuthGroup %s is created" %(AuthName)
            authGroupId = data['tsmcifsauthgroupresponse']['cifsauthgroup']['id']
            querycommand = 'command=addCIFSAuthUser&accountid=%s&authgroupid=%s&username=%s&password=%s' %(account_id, authGroupId, user, password)
            resp_addDuplicateCIFSAuthUser = sendrequest(stdurl, querycommand)
            filesave("logs/addDuplicateCifsUser.txt", "w", resp_addDuplicateCIFSAuthUser)
            data = json.loads(resp_addDuplicateCIFSAuthUser.text)
            if "errorcode" in data['addcifsauthuserresponse']:
                message = data['addcifsauthuserresponse']['errortext']
                if 'unique name' in message:
                    endTime = ctime()
                    resultCollection("Duplicate cifs user TC is", ['PASSED', message], startTime, endTime)
                else:
                    endTime = ctime()
                    resultCollection("Duplicate cifs user TC is", ['FAILED', message], startTime, endTime)
            else:
                endTime = ctime()
                resultCollection("Able to create Duplicate cifs user, So TC is", ['FAILED', ''], startTime, endTime)
        else:
            flag = 1
            error_cause = 'Not able to create AuthGroup'
    else:
        flag = 1
        error_cause = 'Account name is not matching with config file'
else:
    flag = 1
    error_cause = 'Not able to run listAccount'
if flag:
    endTime = ctime()
    resultCollection("Duplicate cifs user TC is blocked reason is %s" %(error_cause), ['BLOCKED', ''], startTime, endTime)

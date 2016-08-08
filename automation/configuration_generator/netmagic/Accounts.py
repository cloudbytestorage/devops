import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

######## To Add an Account for TSM -- Begins


print "Account Creation Begins"
timetrack("Account Creation Begins")
for x in range(1, int(config['Number_of_Accounts'])+1):
    startTime = ctime()
    querycommand = 'command=createAccount&name=%s&description=%s' %(config['accountName%d' %(x)], config['accountDescription%d' %(x)])
    resp_createAccount=sendrequest(stdurl,querycommand)
    filesave("logs/AccountCreation.txt","w",resp_createAccount)
    data = json.loads(resp_createAccount.text)
    if not 'errorcode' in data['createaccountresponse']:
        print "Account %s is created" %(config['accountName%d' %(x)])
        endTime = ctime()
        resultCollection("Account %s creation is" %(config['accountName%d' %(x)]), ['PASSED', ''], startTime, endTime)
        ###
        account_id = data["createaccountresponse"]["account2"]["id"]  
        #creating Account User
        userName = "%suser" %(config['accountName%d' %(x)])
        password = userName
        time.sleep(2);
        querycommand = 'command=createAccountUser&description=test&fullname=test&password=%s&username=%s&accountid=%s' %(password, userName, account_id)
        resp_createAccountUser = sendrequest(stdurl, querycommand)
        filesave('logs/resp_createAccountUser', 'w', resp_createAccountUser)
        data2 = json.loads(resp_createAccountUser.text)
        if not 'errorcode' in data2['createUserResponse']:
            endTime = ctime()
            print 'usr %s is created' %(userName)
            resultCollection('cifs user created successfully', ['PASSED', ''], startTime, endTime)
        else:
            endTime = ctime()
            print 'usr %s creation is failed' %(userName)
            resultCollection('cifs user created failed', ['FAILED', ''], startTime, endTime)

    else:
        endTime = ctime()
        print "Error in creating %s : %s " %(config['accountName%d' %(x)],str(data['createaccountresponse']['errortext']))
        resultCollection("Account %s creation is" %(config['accountName%d' %(x)]), ['FAILED', ''], startTime, endTime)


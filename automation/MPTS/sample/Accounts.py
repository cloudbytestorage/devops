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
        #creating Account User Authentication
        AuthName = "%sAUTH" %(config['accountName%d' %(x)])
        user = "%suser" %(config['accountName%d' %(x)])
        password = user
        time.sleep(2);
        querycommand = 'command=addCIFSAuthGroup&accountid=%s&name=%s&comment=%s&username=%s&password=%s&fullname=%s' %(account_id, AuthName,"Comment",user,password,"fullname")
        resp_tsmcifsauthgroupresponse = sendrequest(stdurl,querycommand)
        filesave("logs/AccountUserCreation.txt","w",resp_tsmcifsauthgroupresponse)
        data = json.loads(resp_tsmcifsauthgroupresponse.text)
        if not "errortext" in data["tsmcifsauthgroupresponse"]:
            endTime = ctime()
            print "AuthGroup %s is created" %(AuthName)
            resultCollection("AuthGroup %s creation is" %(AuthName), ['PASSED', ''], startTime, endTime)
            ###
            if x == 1:
                authGroupId = data['tsmcifsauthgroupresponse']['cifsauthgroup']['id']
                print 'authGroupId = %s' %(authGroupId)
                for i in range(1, 3):
                    user = "%suser%d" %(config['accountName%d' %(x)], i)
                    password = user
                    querycommand = 'command=addCIFSAuthUser&accountid=%s&authgroupid=%s&username=%s&password=%s' %(account_id, authGroupId, user, password)
                    resp_addCIFSAuthUser = sendrequest(stdurl, querycommand)
                    filesave("logs/AccountUserCreation.txt", "w", resp_addCIFSAuthUser)
                    data = json.loads(resp_addCIFSAuthUser.text)
                    if not "errorcode" in data['cifsauthuserresponse']:
                        endTime = ctime()
                        print 'Cifs user %s is created' %(user)
                        resultCollection("Cifs User %s creation is" %(user), ['PASSED', ''], startTime, endTime)
                    else:
                        endTime = ctime()
                        print 'Error in creating cifs user %s' %(user)
                        resultCollection("Cifs User %s creation is" %(user), ['FAILED', ''], startTime, endTime)

        else:
            endTime = ctime()
            print "Error in creating %s : %s" %(AuthName,data["tsmcifsauthgroupresponse"]["errortext"])
            resultCollection("AuthGroup %s creation is" %(AuthName), ['FAILED', ''], startTime, endTime)

        time.sleep(2);

    else:
        endTime = ctime()
        print "Error in creating %s : %s " %(config['accountName%d' %(x)],str(data['createaccountresponse']['errortext']))
        resultCollection("Account %s creation is" %(config['accountName%d' %(x)]), ['FAILED', ''], startTime, endTime)


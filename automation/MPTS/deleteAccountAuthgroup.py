import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

if len(sys.argv)<2:
    print "Argument is not correct.. Correct way as below"
    print "python deleteAccountAuthgroup.py snapshot.txt"
    exit()

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

### CIFS Auth group should be deleted when an account is deleted
### Expected result
### When the account and auth group is deleted, the deletion should be done cleanly from UI and db
### After deletion when the new account and new auth group is created with same name it should be successful
### Dependenties: Nothing

startTime = ctime()
accountName = 'accountNametest101'
### creating account
querycommand = 'command=createAccount&name=%s&description=%s' %(accountName, "Account description")
resp_createAccount2 = sendrequest(stdurl,querycommand)
filesave("logs/AccountsCreation2.txt", "w", resp_createAccount2)
data = json.loads(resp_createAccount2.text)
flag = 1;
errormsg = ''
if not 'errorcode' in data['createaccountresponse']:
    print "Account %s is created" %(accountName)
    account_id = data["createaccountresponse"]["account2"]["id"]
    AuthName = "%sAUTH" %(accountName)
    user = "%suser" %(accountName)
    password = user
    time.sleep(2);
    #creating cifs authentication group and cifs user
    querycommand = 'command=addCIFSAuthGroup&accountid=%s&name=%s&comment=%s&username=%s&password=%s&fullname=%s' %(account_id, AuthName, "Comment", user, password, "fullname")
    resp_tsmcifsauthgroupresponse2 = sendrequest(stdurl,querycommand)
    filesave("logs/AccountUserCreation2.txt", "w", resp_tsmcifsauthgroupresponse2)
    data2 = json.loads(resp_tsmcifsauthgroupresponse2.text)
    if not "errotext" in data2["tsmcifsauthgroupresponse"]:
        print 'Authgroup %s is created' %(AuthName)
    else:
        flag = 0
        errormsg = str(data2['tsmcifsauthgroupresponse']['errortext'])
else:
    flag = 0
    errormsg = str(data['createaccountresponse']['errortext'])

if flag:
    time.sleep(2)
    ### deleting above created account
    querycommand = 'command=deleteAccount&id=%s' %(account_id)
    resp_deleteAccount2 = sendrequest(stdurl, querycommand)
    filesave("logs/DeleteCreation2.txt", "w", resp_deleteAccount2)
    data3 = json.loads(resp_deleteAccount2.text)
    if not 'errorcode' in data3['deleteAccountResponse']:
        print 'Account %s is deleted successfully' %(accountName)
        time.sleep(2)
        ### create account with same name as account, but that account has been deleted
        querycommand = 'command=createAccount&name=%s&description=%s' %(accountName, "Account description")
        resp_createAccount2 = sendrequest(stdurl, querycommand)
        filesave("logs/AccountsCreation2.txt", "w", resp_createAccount2)
        data4 = json.loads(resp_createAccount2.text)
        ### Creating cifs authgroup with same name as previous authgroup name that has been deleted
        if not 'errorcode' in data4['createaccountresponse']:
            print 'Account %s is created' %(accountName)
            account_id = data4["createaccountresponse"]["account2"]["id"]
            querycommand = 'command=addCIFSAuthGroup&accountid=%s&name=%s&comment=%s&username=%s&password=%s&fullname=%s' %(account_id, AuthName, "Comment", user, password, "fullname")
            myurl = stdurl + querycommand
            resp_tsmcifsauthgroupresponse2 = sendrequest(stdurl, querycommand)
            filesave("logs/AccountUserCreation2.txt", "w", resp_tsmcifsauthgroupresponse2)
            data5 = json.loads(resp_tsmcifsauthgroupresponse2.text)
            if not 'errorcode' in data5["tsmcifsauthgroupresponse"]:
                print 'Authgroup %s is created' %(AuthName)
                endTime = ctime()
                resultCollection("CIFS Auth group should be deleted when an account is deleted is", ["PASSED", ''], startTime, endTime)
            else:
                endTime = ctime()
                errormsg = str(data5['tsmcifsauthgroupresponse']['errortext'])
                resultCollection("CIFS Auth group should be deleted when an account is deleted is", ["FAILED", errormsg], startTime, endTime)
        else:
            endTime = ctime()
            errormsg = str(data4['createaccountresponse']['errortext'])
            resultCollection("Not able to create Account with name that account has been deleted", ["FAILED", errormsg], startTime, endTime)
    else:
        endTime = ctime()
        errormsg = str(data3['deleteAccountResponse']['errortext'])
        resultCollection("Error in deleting Account, Skipping for creating Account/Authgroup with same name", ['FAILED', errormsg], startTime, endTime)
else:
    endTime = ctime()
    resultCollection("Error in creating Account/Authgroup, Skipping for deleting/creating Account/Authgroup with same name", ['FAILED', errormsg], startTime, endTime)


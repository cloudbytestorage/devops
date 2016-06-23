import json
import requests

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    #print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;
 
#### Function(s) Declartion Ends


config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

####### To Add an Account for TSM -- Begins

print "Account Creation Begins"
for x in range(1, int(config['Number_of_Accounts'])+1):
#for x in range (1, NoofAccounts+1): 
    #Creating Account
    querycommand = 'command=createAccount&name=%s&description=%s' %(config['accountName%d' %(x)], config['accountDescription%d' %(x)])
    resp_createAccount=sendrequest(stdurl,querycommand)
    filesave("logs/AccountCreation.txt","w",resp_createAccount)
    data = json.loads(resp_createAccount.text)
    account_id=data["createaccountresponse"]["account2"]["id"]

    #Creating 1 Account User (Currently its AccountnameUser)
    querycommand = 'command=createAccountUser&accountid=%s&username=%suser&password=%suser&fullname=%suser&description=%suser' %(account_id, config['accountName%d' %(x)], config['accountName%d' %(x)], config['accountName%d' %(x)], config['accountName%d' %(x)])
    resp_createAccountUser=sendrequest(stdurl,querycommand)
    filesave("logs/AcccountUserCreation.txt","w",resp_createAccountUser)
    print "Account %d Creation Done" %(x)
print "Account Creation Done"

######## To Add an Account for TSM -- Done



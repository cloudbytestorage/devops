import json
import sys
import time
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

######## To Add an Account for TSM -- Begins


print "Account Creation Begins"
timetrack("Account Creation Begins")
for x in range(1, int(config['Number_of_Accounts'])+1):
    querycommand = 'command=createAccount&name=%s&description=%s' %(config['accountName%d' %(x)], config['accountDescription%d' %(x)])
    resp_createAccount=sendrequest(stdurl,querycommand)
    filesave("logs/AccountCreation.txt","w",resp_createAccount)
    data = json.loads(resp_createAccount.text)
    if not 'errorcode' in data['createaccountresponse']:
      print "%s is created" %(config['accountName%d' %(x)])
      account_id=data["createaccountresponse"]["account2"]["id"]  
      #creating Account User Authentication
      name = "%sAUTH" %(config['accountName%d' %(x)])
      user = "%suser" %(config['accountName%d' %(x)])
      password = user
      time.sleep(2);
      querycommand ='command=addCIFSAuthGroup&accountid=%s&name=%s&comment=%s&username=%s&password=%s&fullname=%s' %(account_id, name,"Comment",user,password,"fullname")
      resp_tsmcifsauthgroupresponse=sendrequest(stdurl,querycommand)
      filesave("logs/AccountUserCreation.txt","w",resp_tsmcifsauthgroupresponse)
      data = json.loads(resp_tsmcifsauthgroupresponse.text)
      if not "errortext" in data["tsmcifsauthgroupresponse"]:
          print "%s created" %(name)
      else:
          print "Error in creating %s : %s" %(name,data["tsmcifsauthgroupresponse"]["errortext"])
      time.sleep(2);

    else:
        print "Error in creating %s : %s " %(config['accountName%d' %(x)],str(data['createaccountresponse']['errortext']))


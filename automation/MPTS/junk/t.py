import json
import requests

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    print url+querystring
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
######## To Make A NFS Volume Begins here

print "NFS Volume Creation Begins"
###Stage 1 to 7 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
#for x in range (1, NoofNFSVolumes+1):

    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    print resp_listAccount
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volAccountName%d' %(x)]):
            account_id = account['id']
            break
    #print "Accountid =", account_id

    print "NFS Volume %d Created" %(x)
 
print "NFS Volume Creation Done"
######## To Make A NFS Volume Ends here



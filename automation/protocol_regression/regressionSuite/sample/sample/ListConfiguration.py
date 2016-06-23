import json
import requests
import time
import datetime

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofCIFSVolumes=_MyValue_
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

x =   datetime.datetime.now()
total = x - x # To set 0

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

print "Start date and time is = " , datetime.datetime.now()
x =   datetime.datetime.now()
### To list number of  Sites
querycommand = 'command=listSite'
resp_listSite = sendrequest(stdurl,querycommand)
filesave("logs/CurrentSite.txt","w",resp_listSite) 
data = json.loads(resp_listSite.text)
sites = data["listSiteResponse"]["count"]
print "No of Sites    = ", sites
y = datetime.datetime.now()
z = y - x
print "Time taken for List Sites is = ", z
total = total + z

### To list number of  Clusters
x =   datetime.datetime.now()
querycommand = 'command=listHACluster'
resp_listHACluster = sendrequest(stdurl,querycommand)
filesave("logs/CurrentClusters.txt","w",resp_listHACluster) 
data = json.loads(resp_listHACluster.text)
clusters = data["listHAClusterResponse"]["count"]
print "No of Clusters = ", clusters
y = datetime.datetime.now()
z = y - x
print "Time taken for List Clusters is = ", z
total = total + z


### To list number of  Nodes
x =   datetime.datetime.now()
querycommand = 'command=listController'
resp_listController= sendrequest(stdurl,querycommand)
filesave("logs/CurrentNodes.txt","w",resp_listController) 
data = json.loads(resp_listController.text)
nodes = data["listControllerResponse"]["count"]
print "No of Nodes    = ", nodes
y = datetime.datetime.now()
z = y - x
print "Time taken for List Nodes is = ", z
total = total + z

### To list number of  Pools
x =   datetime.datetime.now()
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl,querycommand)
filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
data = json.loads(resp_listHAPool.text)
hapools = data["listHAPoolResponse"]["count"]
print "No of Pools    = ", hapools
y = datetime.datetime.now()
z = y - x
print "Time taken for List Pools is = ", z
total = total + z



### To list number of  List Account
x =   datetime.datetime.now()
querycommand = 'command=listAccount2'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)
accounts = data["listAccountResponse"]["count"]
print "No of Accounts = ", accounts
y = datetime.datetime.now()
z = y - x
print "Time taken for List Accounts is = ", z
total = total + z


### To list the number of TSM
x =   datetime.datetime.now()
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data["listTsmResponse"]["count"]
print "No of TSMs     = ", tsms
y = datetime.datetime.now()
z = y - x
print "Time taken for List TSMs is = ", z
total = total + z

### To list the number of FileSystem
x =   datetime.datetime.now()
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/CurrentFileSystemList.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
volumes = data["listFilesystemResponse"]["count"]
print "No of Volumes  = ", volumes
y = datetime.datetime.now()
z = y - x
print "Time taken for List File Systems is = ", z
total = total + z

print "Time take for all list commands is =", total
print "End date and time is = " , datetime.datetime.now()


import json
import requests
import md5
import fileinput
import subprocess
import time
import datetime

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

def timetrack(event):
    f=open("results/config_creation_result.csv","a")
    f.write(event)
    f.write("--")
    time = datetime.datetime.now()
    f.write(str(time))
    f.write("\n")
    f.close()
    return;

#### Function(s) Declartion Ends

config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

######## To Make A iSCSI Volume Begins here

print "ISCSI Volume Creation Begins"
timetrack("ISCSI Volume Creation Begins")
###Stage 1 to 6 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
#for x in range (1, NoofISCSIVolumes+1):
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['voliSCSIPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
    #print "Poolid =" ,pool_id


    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['voliSCSIAccountName%d' %(x)]):
            account_id = account['id']
            break
    #print "Accountid =", account_id


    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"]["listTsm"]
    for listTsm in tsms:
        if listTsm['name'] == "%s" %(config['voliSCSITSMName%d' %(x)]):
            tsm_id = listTsm['id']
	    dataset_id = listTsm['datasetid']
            break
    #print "Tsmid =", tsm_id
    #print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&mountpoint=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['voliSCSIName%d' %(x)], config['voliSCSILatency%d' %(x)], config['voliSCSIBlocksize%d' %(x)], config['voliSCSITpcontrol%d' %(x)], config['voliSCSIThroughput%d' %(x)], config['voliSCSIIopscontrol%d' %(x)], config['voliSCSIIops%d' %(x)], config['voliSCSIGraceallowed%d' %(x)], config['voliSCSIMemlimit%d' %(x)], config['voliSCSINetworkspeed%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIDatasetname%d' %(x)], config['voliSCSIProtocoltype%d' %(x)], config['voliSCSIQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
    #print "QosGroup id=",qosgroup_id

    ###Stage2 add Volume
    querycommand = 'command=addVolume2&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&recordsize=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&blocklength=%s&iscsienabled=%s&fcenabled=%s' %(config['voliSCSIType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['voliSCSIDatasetname%d' %(x)], config['voliSCSIQuotasize%d' %(x)], dataset_id, config['voliSCSIBlocksize%d' %(x)], config['voliSCSIDeduplication%d' %(x)], config['voliSCSICompression%d' %(x)],config['voliSCSISync%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSINoofCopies%d' %(x)], config['voliSCSICasesensitivity%d' %(x)], config['voliSCSIReadonly%d' %(x)], config['voliSCSIUnicode%d' %(x)], config['voliSCSIBlocklength%d' %(x)], config['voliSCSIISCSIEnabled%d' %(x)], config['voliSCSIFCEnabled%d' %(x)])
    resp_addVolume2 = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolume.txt", "w", resp_addVolume2)
    data = json.loads(resp_addVolume2.text)
    storage_id=data["addvolumeresponse"]["storage"]["id"]
    #print "Storage id =",storage_id

    ###Stage3 Add isCSI Serveice
    querycommand = 'command=addVolumeiSCSIService&volumeid=%s&status=%s' %(storage_id, config['voliSCSIManagedState%d' %(x)])
    resp_addvVolumeiSCSIService = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolumeISCSIService.txt", "w", resp_addvVolumeiSCSIService)
    data = json.loads(resp_addvVolumeiSCSIService.text)
    iscsi_id = data["volumeiSCSIserviceresponse"]["viscsioptions"]["id"]
    #print "ISCSI id =", iscsi_id 

	
    ###Stage4 Update Controller
    querycommand = 'command=updateController&type=qosgroup&qosid=%s&tsmid=%s' %(qosgroup_id, tsm_id)
    resp_updateControllerqosgroup = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerqosgroup)

    ###Stage5 Update Controller
    querycommand = 'command=updateController&storageid=%s&type=storage&tsmid=%s' %(storage_id, tsm_id)
    resp_updateControllerstorage = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerstorage)

    ###Stage6 Update Controller
    querycommand ='command=updateController&viscsiid=%s&type=configurevolumeiscsi' %(iscsi_id)
    resp_updateControlleriscsi = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControlleriscsi.txt", "w", resp_updateControlleriscsi)

	
    print "ISCSI Volume %d Created" %(x)
    
timetrack("ISCSI Volume Creation Done")
print "ISCSI Volume Creation Done" 
######## To Make A iSCSI Volume Ends here

######## To Make A CIFS Volume Begins here
print "CIFS Volume Creation Begins"
timetrack("CIFS Volume Creation Begins")
###Stage 1 to 7 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
#for x in range (1, NoofCIFSVolumes+1):
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['volCifsPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
    

    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volCifsAccountName%d' %(x)]):
            account_id = account['id']
            break


    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"]["listTsm"]
    for listTsm in tsms:
        if listTsm['name'] == "%s" %(config['volCifsTSMName%d'%(x)]):
            tsm_id = listTsm['id']
	    dataset_id = listTsm['datasetid']
            break

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&mountpoint=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['volCifsName%d' %(x)], config['volCifsLatency%d' %(x)], config['volCifsBlocksize%d' %(x)], config['volCifsTpcontrol%d' %(x)], config['volCifsThroughput%d' %(x)], config['volCifsIopscontrol%d' %(x)], config['volCifsIops%d' %(x)], config['volCifsGraceallowed%d' %(x)], config['volCifsMemlimit%d' %(x)], config['volCifsNetworkspeed%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsDatasetname%d' %(x)], config['volCifsProtocoltype%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]



    ###Stage2 add Filesystem
    querycommand = 'command=addFileSystem&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&recordsize=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&cifsenabled=%s&cifsenabled=%s' %(config['volCifsType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['volCifsDatasetname%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id, config['volCifsRecordSize%d' %(x)], config['volCifsDeduplication%d' %(x)], config['volCifsCompression%d' %(x)],config['volCifsSync%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsNoofCopies%d' %(x)], config['volCifsCasesensitivity%d' %(x)], config['volCifsReadonly%d' %(x)], config['volCifsUnicode%d' %(x)], config['volCifsCIFSEnabled%d' %(x)], config['volCifsCIFSEnabled%d' %(x)])
    resp_addFileSystem = sendrequest(stdurl, querycommand)
    filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
    data = json.loads(resp_addFileSystem.text)
    storage_id=data["adddatasetresponse"]["filesystem"]["id"]
	

    ###Stage3 Update Controller
    querycommand = 'command=updateController&type=qosgroup&qosid=%s&tsmid=%s' %(qosgroup_id, tsm_id)
    resp_updateControllerqosgroup = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerqosgroup)

    ###Stage4 Update Controller
    querycommand = 'command=updateController&storageid=%s&type=storage&tsmid=%s' %(storage_id, tsm_id)
    resp_updateControllerstorage = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerstorage)

    ###Stage5 Add CIFS Serveice
    querycommand ='command=addFsCifsService&datasetid=%s&name=%s&description=default&status=true&readonly=false&browseable=true&inheritpermissions=true&recyclebin=true&hidedotfiles=true&name=null&name=null' %(storage_id, config['volCifsTSMName%d' %(x)])
    resp_cifsService = sendrequest(stdurl, querycommand)
    filesave("logs/AddCIFSService.txt", "w", resp_cifsService)
    data = json.loads(resp_cifsService.text)
    cifs_id = data["fsCifsserviceResponse"]["cifsService"]["id"]

	
    ###Stage6 Update Controller
    querycommand ='command=updateController&fcifsid=%s&type=configurecifs' %(cifs_id)
    resp_updateControllercifs = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControllercifs.txt", "w", resp_updateControllercifs)

	
    ###Stage7 addFsCifsService
    querycommand = 'command=addnfsService&datasetid=%s&managedstate=%s&authnetwork=%s&alldirs=%s&mapuserstoroot=%s&readonly=%s' %(storage_id, config['volCifsManagedState%d' %(x)], config['volCifsAuthNetwork%d' %(x)], config['volCifsAllDir%d' %(x)], config['volCifsMapUsersToRoot%d' %(x)], config['volCifsReadOnly%d' %(x)])
    resp_nfsService = sendrequest(stdurl, querycommand)
    filesave("logs/addFsCifsService.txt", "w", resp_nfsService)

    print "CIFS Volume %d Created" %(x)
 
timetrack("CIFS Volume Creation Done")
print "CIFS Volume Creation Done"
######## To Make A CIFS Volume Ends here

#####To List the number of Objects Created
timetrack("Dashboard List Operation Begins")
x =   datetime.datetime.now()
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

x =   datetime.datetime.now()
### To list number of  Sites
querycommand = 'command=listSite'
resp_listSite = sendrequest(stdurl,querycommand)
filesave("logs/CurrentSite.txt","w",resp_listSite) 
data = json.loads(resp_listSite.text)
sites = data["listSiteResponse"]["count"]
print "No of Sites    = ", sites

### To list number of  Clusters
querycommand = 'command=listHACluster'
resp_listHACluster = sendrequest(stdurl,querycommand)
filesave("logs/CurrentClusters.txt","w",resp_listHACluster) 
data = json.loads(resp_listHACluster.text)
clusters = data["listHAClusterResponse"]["count"]
print "No of Clusters = ", clusters


### To list number of  Nodes
querycommand = 'command=listController'
resp_listController= sendrequest(stdurl,querycommand)
filesave("logs/CurrentNodes.txt","w",resp_listController) 
data = json.loads(resp_listController.text)
nodes = data["listControllerResponse"]["count"]
print "No of Nodes    = ", nodes

### To list number of  Pools
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl,querycommand)
filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
data = json.loads(resp_listHAPool.text)
hapools = data["listHAPoolResponse"]["count"]
print "No of Pools    = ", hapools

### To list number of  List Account
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)
accounts = data["listAccountResponse"]["count"]
print "No of Accounts = ", accounts

### To list the number of TSM
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data["listTsmResponse"]["count"]
print "No of TSMs     = ", tsms

### To list the number of FileSystem
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/CurrentFileSystemList.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
volumes = data["listFilesystemResponse"]["count"]
print "No of Volumes  = ", volumes
y = datetime.datetime.now()
z = y - x
print "Time taken for List Operation is = ", z

timetrack("Dashboard List Operation Done")

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

#######Generate Apikeys
m = md5.new()
m.update("%s" %(config['admin_org_password']))
md5_org_pwd =  m.hexdigest()
m = md5.new()
m.update("%s" %(config['admin_set_password']))
md5_set_pwd =  m.hexdigest()
stdurl_noapikey = 'https://%s/client/api?response=%s&' %(config['host'], config['response'])

s = requests.session()
payload = {'command': 'login', 'username': 'admin', 'password': md5_org_pwd, 'domain': '/', 'response': 'json'}

### First time login
r = s.post(stdurl_noapikey, verify=False, data=payload)


### List userid
querystring = 'command=listUsers'
r = s.get(stdurl_noapikey+querystring, verify=False)
data = json.loads(r.text)
users = data["listusersresponse"]["user"]
for user in users:
    if user['username'] == "admin":
        user_id = user['id']

### Update User ID
querystring = 'command=updateUser&id=%s&password=%s&firstname=%s&lastname=%s&email=%s&mobileno=%s' %(user_id, md5_set_pwd, config['firstname'], config['lastname'], config['email'], config['mobile'])
r = s.get(stdurl_noapikey+querystring, verify=False)

### Update Email ID
querystring = 'command=updateConfiguration&name=alert.email.addresses&value=%s' %(config['email'])
r = s.get(stdurl_noapikey+querystring, verify=False)

### Generate ApiKey
querystring = 'command=registerUserKeys&id=%s' %(user_id)
r = s.get(stdurl_noapikey+querystring, verify=False)
data = json.loads(r.text)
apikey = data["registeruserkeysresponse"]["userkeys"]["apikey"]
print apikey
for line in fileinput.FileInput("config.txt",inplace=1):
    line = line.replace("MyApiKey",apikey)
    print line,

cfg.close()
#############Apikey Generated
config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
#########To Add the Sites
print "Site Creation Begins"
timetrack("Site Creation Begins")
for x in range(1, int(config['Number_of_Sites'])+1):
    querycommand = 'command=createSite&location=%s&name=%s&description=%s' %(config['siteLocation%d' %(x)], config['siteName%d'%(x)], config['siteDescription%d' %(x)])
    resp_createSite = sendrequest(stdurl, querycommand)
    filesave("logs/AddSiteList.txt", "w", resp_createSite)
    print "Site %d Creation Begins" %(x)
timetrack("Site Creation Done")
print "Site Creation Done" 

#########To Add Cluster
#########To List the Current Number of Sites 
print "HA Cluster Creation Begins"
timetrack("HA Cluster Creation Begins")
for x in range(1, int(config['Number_of_Clusters'])+1):
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentSitesList.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    sites = data["listSiteResponse"]["site"]
    site = [y for y in sites if y["name"] == "%s" %(config['clusterSiteName%d'%(x)])].pop(0)
    site_id = site["id"] #if site else None

###CreateHACluster Stage1 and Stage2
    ###Stage1 createHACluster
    querycommand = 'command=createHACluster&clustername=%s&description=%s&siteid=%s' %(config['clusterName%d' %(x)], config['clusterDescription%d' %(x)], site_id) 
    resp_createHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/ClusterCreation.txt", "w", resp_createHACluster) 
    data = json.loads(resp_createHACluster.text)
    hacluster_id=data["createHAClusterResponse"]["hacluster"]["id"]

    ###Stage2 createHAClusterNetwork
    querycommand = 'command=createHAClusterNetworkRule&type=healthcheck&network=&subnet=&startip=%s&endip=%s&ipaddress=&clusterid=%s' %(config['clusterStartIP%d' %(x)], config['clusterEndIP%d' %(x)],hacluster_id)
    resp_createHAClusterNetworks = sendrequest(stdurl, querycommand)
    filesave("logs/ClusterCreationComplete.txt", "w", resp_createHAClusterNetworks) 
    print "HA Cluster %d Created" %(x)
timetrack("HA Cluster Creation Done")
print "HA Cluster Creation Done"
###Ends Here Cluster Creation

########To Add Node
#########To List the Current Number of Sites 
print "Node Creation Begins"
timetrack("Node Creation Begins")
for x in range(1, int(config['Number_of_Nodes'])+1):
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentSitesList.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    sites = data["listSiteResponse"]["site"]
    site = [y for y in sites if y["name"] == "%s" %(config['nodeSiteName%d'%(x)])].pop(0)
    site_id = site["id"] #if site else None


    ###To List the Current Number of HA
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand) 
    filesave("logs/CurrentHAClustersList.txt", "w", resp_listHACluster) 
    data = json.loads(resp_listHACluster.text)
    haclusters = data["listHAClusterResponse"]["hacluster"]
    hacluster = [y for y in haclusters if y["name"] == "%s" %(config['nodeClusterName%d'%(x)]) ].pop(0)
    hacluster_id = hacluster["id"] #if site else None

    #Actual Node Addtion happens here
    querycommand = 'command=addController&name=%s&siteid=%s&ipaddress=%s&clusterid=%s' %(config['nodeName%d' %(x)], site_id, config['nodeIP%d' %(x)], hacluster_id) 
    resp_addController = sendrequest(stdurl, querycommand)
    filesave("logs/NodeCreation.txt", "w", resp_addController) 
    print "Node %d Created" %(x)
timetrack("Node Creation Done")
print "Node Creation Done"

########### Node Addtion Complete 

###Add a disk Enclosure
print "JBOD Creation Begins"
timetrack("JBOD Creation Begins")

### 3 Stage process, first 1 to listController and get site_id, cluster_id, controller_id, target and bus

querycommand = 'command=listController'
resp_listController = sendrequest(stdurl, querycommand)
filesave("logs/CurrentControllerList.txt", "w", resp_listController) 
data = json.loads(resp_listController.text)
controllers = data["listControllerResponse"]["controller"]

for controller in controllers:
    if controller['name'] == "%s" %(config['nodeName1']): #Still Can be parameterised for Node loop 
        disks = controller['disks']
        controller_id = controller['id']
        site_id = controller['siteid']
        cluster_id = controller['clusterid']
        break

target, bus = "", ""
lunnumber = []
for disk in disks:
    target += disk['target']
    target += ","
    bus += disk['bus']
    bus += ","
    lunnumber.append('0')

lunnumber=','.join(lunnumber)

### Stage 1 Create JBOD
querycommand = 'command=createJBOD&clusterid=%s&name=%s&type=%s&rows=%s&cols=%s' %(cluster_id, config['jbodName1'], config['type'],config['rows'],config['cols'])
resp_createJBOD = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODList.txt", "w", resp_createJBOD) 
data = json.loads(resp_createJBOD.text)
jbod_id=data["createJbodResponse"]["jbod"]["id"]

### Stage 2 UpdatediskLabels
querycommand = 'command=updateDiskLabels&jbodid=%s&controllerid=%s&bus=%s&targetnumber=%s&baynumber=%s&lunnumber=%s' %(jbod_id, controller_id, bus, target, config['baynumber1'],lunnumber)
resp_updateDiskLabels = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updateDiskLabels) 

### Stage 3 UpdateHAconfiglabels
querycommand = 'command=updatehaconfiglabel&clusterid=%s' %(cluster_id)

resp_updatehaconfiglabel = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updatehaconfiglabel) 

timetrack("JBOD Creation Done")
print "JBOD Creation Done"
############ Disk Enclosure Done

######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
print "Pool Creation Begins"
timetrack("Pool Creation Begins")

###To List the Current Number of Sites 
for x in range(1, int(config['Number_of_Pools'])+1):
    ### To ListController  and get Diskids
    querycommand = 'command=listController'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/ListController.txt", "w", resp_listController)
    data = json.loads(resp_listController.text)
    controllers = data["listControllerResponse"]["controller"]
    for controller in controllers:
        if controller['name'] == "%s" %(config['poolNodeName%d' %(x)]): 
	    disks = controller['disks']
	    controller_id = controller['id']
	    site_id = controller['siteid']
	    cluster_id = controller['clusterid']
	    break
    disk_list_id = ""
    for disk in disks:
        for y in range (1, int(config['poolDisksAllocated%d' %(x)])+1):
            if "%s" %(config['poolDiskLabel%d%d' %(y,x)]) in disk['label']:
                disk_list_id += disk['id']
                disk_list_id += ","

    ####### Clear the Pools
    querycommand = 'command=clearPool&&name=%s&id=%s' %(config['poolName%d' %(x)], controller_id)
    resp_clearPool= sendrequest(stdurl, querycommand)
    filesave("logs/clearPool.txt", "w", resp_clearPool)

    ### Stage1 addHAPool
    querycommand = 'command=addHAPool&controllerid=%s&siteid=%s&clusterid=%s&diskslist=%s&name=%s&graceallowed=%s&iops=%s&throughput=%s&latency=%s&sectorsize=%s&grouptype=%s&scsireserved=true' %(controller_id,site_id, cluster_id, disk_list_id, config['poolName%d' %(x)], config['poolGraceAllowed%d' %(x)], config['poolIops%d' %(x)], config['poolThroughput%d' %(x)],  config['poolLatency%d' %(x)], config['poolSectorsize%d' %(x)], config['poolGroupType%d' %(x)])
    resp_addHAPool = sendrequest(stdurl, querycommand)
    filesave("logs/AddHAPool.txt", "w", resp_addHAPool)
    print "Pool %d Created" %(x)
    time.sleep(60)#Now its an async call.

timetrack("Pool Creation Done")
print "Pool Creation Done"
######## To Make A Pool Done

######## To Add an Account for TSM -- Begins


print "Account Creation Begins"
timetrack("Account Creation Begins")
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
timetrack("Account Creation Done")
print "Account Creation Done"

######## To Add an Account for TSM -- Done

######## To Make A TSM Begins here

print "TSM Creation Begins"
timetrack("TSM Creation Begins")
for x in range(1, int(config['Number_of_TSMs'])+1):
#for x in range (1, NoofTSMs+1): 
    ###Stage 1 to 8 ... Prior to that 2 commands are for listing.

    #querycommand = 'command=createAccount&name=%s&description=%s' %(config['tsmName%d' %(x)], config['tsmDescription%d' %(x)])
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['tsmPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
        #print "Poolid =" ,pool_id


    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['tsmAccountName%d' %(x)]):
            account_id = account['id']
            break
            #print "Accountid =", account_id


    ###Stage1 Command addTSM
    querycommand = 'command=addTsm&accountid=%s&poolid=%s&name=%s&ipaddress=%s&subnet=%s&router=%s&dnsname=%s&dnsserver=%s&tntinterface=%s&gracecontrol=%s&graceallowed=%s&blocksize=%s&latency=%s&iopscontrol=%s&totaliops=%s&tpcontrol=%s&totalthroughput=%s&backuptpcontrol=%s&totalbackupthroughput=%s&iqnname=%s&quotasize=%s' %(account_id, pool_id, config['tsmName%d' %(x)], config['tsmIPAddress%d' %(x)], config['tsmSubnet%d' %(x)], config['tsmRouter%d' %(x)], config['tsmDNSName%d' %(x)], config['tsmDNSServer%d' %(x)], config['tsmTntInterface%d' %(x)], config['tsmGraceControl%d' %(x)], config['tsmGraceAllowed%d' %(x)], config['tsmBlocksize%d' %(x)], config['tsmLatency%d' %(x)], config['tsmIopsControl%d' %(x)], config['tsmTotalIops%d' %(x)], config['tsmTpControl%d' %(x)], config['tsmTotalThroughput%d' %(x)], config['tsmBackupTpcontrol%d' %(x)], config['tsmTotalBackupThroughput%d' %(x)], config['tsmIqnName%d' %(x)], config['tsmQuotasize%d' %(x)])
    resp_addTsm = sendrequest(stdurl, querycommand)
    filesave("logs/AddTsm.txt", "w", resp_addTsm)
    data = json.loads(resp_addTsm.text)
    tsm_id=data["addTsmResponse"]["tsm"]["id"]
    controller_id=data["addTsmResponse"]["tsm"]["controllerid"]
    #print "TSM ID=", tsm_id
    #print "Controller_id", controller_id

    ####Stage2 Command addStorage
    querycommand = 'command=addStorage&tsmid=%s&poolid=%s&deduplication=off&compression=off&sync=standard&noofcopies=1&recordsize=4K&quotasize=%s' %(tsm_id, pool_id, config['tsmQuotasize%d' %(x)])
    resp_addStorage = sendrequest(stdurl, querycommand)
    filesave("logs/AddStorage.txt", "w", resp_addStorage)
    data = json.loads(resp_addStorage.text)
    storage_id=data["addStorageResponse"]["storage"]["id"]
    #print "Storage id", storage_id

    ####Stage3 updateControllerCommand tsmid
    querycommand = 'command=updateController&tsmid=%s&type=tsm&id=%s' %(tsm_id, controller_id)
    resp_updateController1 = sendrequest(stdurl, querycommand)
    filesave("logs/updateController1.txt", "w", resp_updateController1)

    ####Stage4 updateControllerCommand Storageid
    querycommand = 'command=updateController&storageid=%s&type=storage&id=%s' %(storage_id, controller_id)
    resp_updateController2 = sendrequest(stdurl, querycommand)
    filesave("logs/updateController2.txt", "w", resp_updateController2)

    ####Stage5 addTsmiSCSIService
    querycommand = 'command=addTsmiSCSIService&tsmid=%s' %(tsm_id)
    resp_addTsmiSCSIService = sendrequest(stdurl, querycommand)
    filesave("logs/resp_addTsmiSCSIService.txt", "w", resp_addTsmiSCSIService)
    data = json.loads(resp_addTsmiSCSIService.text)
    iscsi_id = data["tsmiSCSIserviceresponse"]["tiscsioptions"]["id"]
    #print "iSCSIID=",iscsi_id

    ####Stage6 updateController
    querycommand = 'command=updateController&iscsiid=%s&type=configuretsmiscsi&id=%s' %(iscsi_id, controller_id)
    resp_updateControlleriSCSI = sendrequest(stdurl, querycommand)
    filesave("logs/resp_updateControlleriSCSI.txt", "w", resp_updateControlleriSCSI)

    ####Stage7 addTSMCIFSService
    querycommand = 'command=addTsmCifsService&tsmid=%s&netbiosname=%s&authentication=user&workgroup=workgroup&doscharset=CP437&unixcharset=UTF-8&loglevel=Minimum&timeserver=false' %(tsm_id, config['tsmName%d' %(x)])
    resp_addTSMCIFSService = sendrequest(stdurl, querycommand)
    filesave("logs/resp_addTsmiSCSIService.txt", "w", resp_addTSMCIFSService)
    data = json.loads(resp_addTSMCIFSService.text)
    cifs_id = data["tsmCifsserviceResponse"]["cifsService"]["id"]
    #print "Cifs id", cifs_id

    ####Stage8 updateController
    querycommand = 'command=updateController&tcifsid=%s&type=configuretsmcifs&id=%s' %(cifs_id, controller_id)
    resp_updateControllerCIFS = sendrequest(stdurl, querycommand)
    filesave("logs/resp_updateControllerCIFS", "w", resp_updateControllerCIFS)
    print "TSM %d created" %(x)

timetrack("TSM Creation Done")
print "TSM Creation Done"
##### TSM Creation ends here

######## To Make A NFS Volume Begins here

print "NFS Volume Creation Begins"
timetrack("NFS Volume Creation Begins")
###Stage 1 to 7 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
#for x in range (1, NoofNFSVolumes+1):
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['volPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
    #print "Poolid =" ,pool_id
    

    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volAccountName%d' %(x)]):
            account_id = account['id']
            break
    #print "Accountid =", account_id


    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"]["listTsm"]
    for listTsm in tsms:
        if listTsm['name'] == "%s" %(config['volTSMName%d'%(x)]):
            tsm_id = listTsm['id']
	    dataset_id = listTsm['datasetid']
            break
    #print "Tsmid =", tsm_id
    #print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&mountpoint=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['volName%d' %(x)], config['volLatency%d' %(x)], config['volBlocksize%d' %(x)], config['volTpcontrol%d' %(x)], config['volThroughput%d' %(x)], config['volIopscontrol%d' %(x)], config['volIops%d' %(x)], config['volGraceallowed%d' %(x)], config['volMemlimit%d' %(x)], config['volNetworkspeed%d' %(x)], config['volMountpoint%d' %(x)], config['volDatasetname%d' %(x)], config['volProtocoltype%d' %(x)], config['volQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
    #print "QosGroup id=",qosgroup_id

    ###Stage2 add Filesystem
    querycommand = 'command=addFileSystem&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&recordsize=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&nfsenabled=%s&cifsenabled=%s' %(config['volType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['volDatasetname%d' %(x)], config['volQuotasize%d' %(x)], dataset_id, config['volRecordSize%d' %(x)], config['volDeduplication%d' %(x)], config['volCompression%d' %(x)],config['volSync%d' %(x)], config['volMountpoint%d' %(x)], config['volNoofCopies%d' %(x)], config['volCasesensitivity%d' %(x)], config['volReadonly%d' %(x)], config['volUnicode%d' %(x)], config['volNFSEnabled%d' %(x)], config['volCIFSEnabled%d' %(x)])
    resp_addFileSystem = sendrequest(stdurl, querycommand)
    filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
    data = json.loads(resp_addFileSystem.text)
    storage_id=data["adddatasetresponse"]["filesystem"]["id"]
    #print "Storage id =",storage_id
	
    ###Stage3 Add NFS Serveice
    querycommand = 'command=nfsService&datasetid=%s&managedstate=%s&authnetwork=%s&alldirs=%s&mapuserstoroot=%s&readonly=%s' %(storage_id, config['volManagedState%d' %(x)], config['volAuthNetwork%d' %(x)], config['volAllDir%d' %(x)], config['volMapUsersToRoot%d' %(x)], config['volReadOnly%d' %(x)])
    resp_nfsService = sendrequest(stdurl, querycommand)
    filesave("logs/AddNFSService.txt", "w", resp_nfsService)
    data = json.loads(resp_nfsService.text)
    nfs_id = data["nfsserviceprotocolresponse"]["nfs"]["id"]
    #print "NFS id =", nfs_id 

	
    ###Stage4 Update Controller
    querycommand = 'command=updateController&type=qosgroup&qosid=%s&tsmid=%s' %(qosgroup_id, tsm_id)
    resp_updateControllerqosgroup = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerqosgroup)

    ###Stage5 Update Controller
    querycommand = 'command=updateController&storageid=%s&type=storage&tsmid=%s' %(storage_id, tsm_id)
    resp_updateControllerstorage = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerstorage)
	
    ###Stage6 Update Controller
    querycommand ='command=updateController&nfsid=%s&type=configurenfs' %(nfs_id)
    resp_updateControllernfs = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControllernfs.txt", "w", resp_updateControllernfs)

	
    ###Stage7 addFsCifsService
    querycommand ='command=addFsCifsService&datasetid=d0b0db0d-89e9-39e2-9b80-ea69b0c9259f&name=Storage1&description=default&status=false&readonly=false&browseable=true&inheritpermissions=true&recyclebin=true&hidedotfiles=true&name=null&name=null'
    resp_addFsCifsService = sendrequest(stdurl, querycommand)
    filesave("logs/addFsCifsService.txt", "w", resp_addFsCifsService)

    print "NFS Volume %d Created" %(x)
 
timetrack("NFS Volume Creation Done")
print "NFS Volume Creation Done"
######## To Make A NFS Volume Ends here

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

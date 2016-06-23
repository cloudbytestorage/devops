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

###Add a disk Enclosure
print "JBOD Creation Begins"

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
for disk in disks:
    target += disk['target']
    target += ","
    bus += disk['bus']
    bus += ","

### Stage 1 Create JBOD
querycommand = 'command=createJBOD&clusterid=%s&name=%s&type=%s&rows=%s&cols=%s' %(cluster_id, config['jbodName1'], config['type'],config['rows'],config['cols'])
resp_createJBOD = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODList.txt", "w", resp_createJBOD) 
data = json.loads(resp_createJBOD.text)
jbod_id=data["createJbodResponse"]["jbod"]["id"]

### Stage 2 UpdatediskLabels
querycommand = 'command=updateDiskLabels&jbodid=%s&controllerid=%s&bus=%s&targetnumber=%s&baynumber=%s' %(jbod_id, controller_id, bus, target, config['baynumber1'])
resp_updateDiskLabels = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updateDiskLabels) 

### Stage 3 UpdateHAconfiglabels
querycommand = 'command=updatehaconfiglabel&clusterid=%s' %(cluster_id)

resp_updatehaconfiglabel = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updatehaconfiglabel) 

print "JBOD Creation Done"
############ Disk Enclosure Done

######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
print "Pool Creation Begins"

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
    ### Stage1 addHAPool
    querycommand = 'command=addHAPool&controllerid=%s&siteid=%s&clusterid=%s&diskslist=%s&name=%s&graceallowed=%s&iops=%s&throughput=%s&latency=%s&sectorsize=%s' %(controller_id,site_id, cluster_id, disk_list_id, config['poolName%d' %(x)], config['poolGraceAllowed%d' %(x)], config['poolIops%d' %(x)], config['poolThroughput%d' %(x)],  config['poolLatency%d' %(x)], config['poolSectorsize%d' %(x)])
    resp_addHAPool = sendrequest(stdurl, querycommand)
    filesave("logs/AddHAPool.txt", "w", resp_addHAPool)
    data = json.loads(resp_addHAPool.text)
    pool_id = data["addHAPoolResponse"]["hapool"]["id"] 
    ### Stage2  addDiskGroup
    querycommand = 'command=addDiskGroup&clusterid=%s&poolid=%s&diskslist=%s&totaliops=%s&totalthroughput=%s&name=%s&grouptype=%s&sectorsize=%s' %(cluster_id, pool_id, disk_list_id, config['poolIops%d' %(x)], config['poolThroughput%d' %(x)], config['poolGroupName%d' %(x)], config['poolGroupType%d' %(x)], config['poolSectorsize%d' %(x)])
    resp_addDiskGroup= sendrequest(stdurl, querycommand)
    filesave("logs/AddDiskGroup.txt", "w", resp_addDiskGroup)
    
    ### Stage3 UpdateController
    querycommand = 'command=updateController&id=%s&poolid=%s&type=pool' %(controller_id, pool_id)
    resp_updateController = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateController)
    print "Pool %d Created" %(x)

print "Pool Creation Done"
######## To Make A Pool Done



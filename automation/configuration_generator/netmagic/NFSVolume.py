import json
import sys
import time
from time import ctime
import requests
from cbrequest import sendrequest, filesave, configFile

config = configFile(sys.argv)
print "%s" %(config['host'])

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
######## To Make A NFS Volume Begins here

print "NFS Volume Creation Begins"
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
    querycommand ='command=addFsCifsService&datasetid=%s&name=%s&description=default&status=false&readonly=false&browseable=true&inheritpermissions=true&recyclebin=true&hidedotfiles=true&name=null&name=null' %(storage_id, config['volDatasetname%d' %(x)])
    resp_addFsCifsService = sendrequest(stdurl, querycommand)
    filesave("logs/addFsCifsService.txt", "w", resp_addFsCifsService)

    print "NFS Volume %d Created" %(x)
 
print "NFS Volume Creation Done"
######## To Make A NFS Volume Ends here



import json
import requests

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

def msg():
    msg = 'Press y to Continue or Any other key to exit? \n'
    if (raw_input("%s (y/N) " % msg).lower() == 'y'):
        print "Proceed"
    else:
        print "Still Proceeding :)"
    return;
 
#### Function(s) Declartion Ends


config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
######## To Make A CIFS Volume Begins here

print "CIFS Volume Creation Begins"
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
    print "Poolid =" ,pool_id
    

    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volCifsAccountName%d' %(x)]):
            account_id = account['id']
            break
    print "Accountid =", account_id


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
    print "Tsmid =", tsm_id
    print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&mountpoint=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['volCifsName%d' %(x)], config['volCifsLatency%d' %(x)], config['volCifsBlocksize%d' %(x)], config['volCifsTpcontrol%d' %(x)], config['volCifsThroughput%d' %(x)], config['volCifsIopscontrol%d' %(x)], config['volCifsIops%d' %(x)], config['volCifsGraceallowed%d' %(x)], config['volCifsMemlimit%d' %(x)], config['volCifsNetworkspeed%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsDatasetname%d' %(x)], config['volCifsProtocoltype%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
    print "QosGroup id=",qosgroup_id



    ###Stage2 add Filesystem
    querycommand = 'command=addFileSystem&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&recordsize=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&nfsenabled=%s&cifsenabled=%s' %(config['volCifsType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['volCifsDatasetname%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id, config['volCifsRecordSize%d' %(x)], config['volCifsDeduplication%d' %(x)], config['volCifsCompression%d' %(x)],config['volCifsSync%d' %(x)], config['volCifsMountpoint%d' %(x)], config['volCifsNoofCopies%d' %(x)], config['volCifsCasesensitivity%d' %(x)], config['volCifsReadonly%d' %(x)], config['volCifsUnicode%d' %(x)], config['volCifsNFSEnabled%d' %(x)], config['volCifsCIFSEnabled%d' %(x)])
    resp_addFileSystem = sendrequest(stdurl, querycommand)
    filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
    data = json.loads(resp_addFileSystem.text)
    storage_id=data["adddatasetresponse"]["filesystem"]["id"]
    print "Storage id =",storage_id
	

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
    print "CIFS id =", cifs_id 

	
    ###Stage6 Update Controller
    querycommand ='command=updateController&fcifsid=%s&type=configurecifs' %(cifs_id)
    resp_updateControllercifs = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControllercifs.txt", "w", resp_updateControllercifs)

	
    ###Stage7 addFsCifsService
    querycommand = 'command=manageNfs&id=%s&managedstate=%s' %(storage_id, config['volNfsManagedState%d' %(x)])
    resp_nfsService = sendrequest(stdurl, querycommand)
    filesave("logs/addFsCifsService.txt", "w", resp_nfsService)

    print "CIFS Volume %d Created" %(x)
 
print "CIFS Volume Creation Done"
######## To Make A CIFS Volume Ends here



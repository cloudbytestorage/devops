import sys
import time
from time import ctime
import json
import requests
from cbrequest import sendrequest, filesave, configFile

config = configFile(sys.argv)

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

######## To Make A iSCSI Volume Begins here

print "ISCSI Volume Creation Begins"
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
        print listTsm['name'] + '\n'
        print "%s" %(config['voliSCSITSMName%d' %(x)])
        if listTsm['name'] == "%s" %(config['voliSCSITSMName%d' %(x)]):
            tsm_id = listTsm['id']
            print tsm_id
            dataset_id = listTsm['datasetid']
            break
        else:
            continue

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&mountpoint=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['voliSCSIName%d' %(x)], config['voliSCSILatency%d' %(x)], config['voliSCSIBlocksize%d' %(x)], config['voliSCSITpcontrol%d' %(x)], config['voliSCSIThroughput%d' %(x)], config['voliSCSIIopscontrol%d' %(x)], config['voliSCSIIops%d' %(x)], config['voliSCSIGraceallowed%d' %(x)], config['voliSCSIMemlimit%d' %(x)], config['voliSCSINetworkspeed%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIDatasetname%d' %(x)], config['voliSCSIProtocoltype%d' %(x)], config['voliSCSIQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    print data
    print stdurl+querycommand
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
    #print "QosGroup id=",qosgroup_id
    print stdurl+querycommand     
    ###Stage2 add Volume
    querycommand = 'command=addVolume2&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&blocklength=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&iscsienabled=%s&fcenabled=%s&recordsize=%s' %(config['voliSCSIType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['voliSCSIDatasetname%d' %(x)], config['voliSCSIQuotasize%d' %(x)], dataset_id, config['voliSCSIBlocklength%d' %(x)], config['voliSCSIDeduplication%d' %(x)], config['voliSCSICompression%d' %(x)],config['voliSCSISync%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSINoofCopies%d' %(x)], config['voliSCSICasesensitivity%d' %(x)], config['voliSCSIReadonly%d' %(x)], config['voliSCSIUnicode%d' %(x)], config['voliSCSIISCSIEnabled%d' %(x)], config['voliSCSIFCEnabled%d' %(x)], config['voliSCSIRecordSize%d' %(x)])
    resp_addVolume2 = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolume.txt", "w", resp_addVolume2)
    data = json.loads(resp_addVolume2.text)
    storage_id=data["addvolumeresponse"]["storage"]["id"]
    #print "Storage id =",storage_id
    print stdurl+querycommand
     	
    ###Stage3 Add isCSI Serveice
    querycommand = 'command=addVolumeiSCSIService&volumeid=%s&status=%s' %(storage_id, config['voliSCSIManagedState%d' %(x)])
    resp_addvVolumeiSCSIService = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolumeISCSIService.txt", "w", resp_addvVolumeiSCSIService)
    data = json.loads(resp_addvVolumeiSCSIService.text)
    iscsi_id = data["volumeiSCSIserviceresponse"]["viscsioptions"]["id"]
    #print "ISCSI id =", iscsi_id 
    print stdurl+querycommand
	
    ###Stage4 Update Controller
    querycommand = 'command=updateController&type=qosgroup&qosid=%s&tsmid=%s' %(qosgroup_id, tsm_id)
    resp_updateControllerqosgroup = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerqosgroup)
    print stdurl+querycommand
    ###Stage5 Update Controller
    querycommand = 'command=updateController&storageid=%s&type=storage&tsmid=%s' %(storage_id, tsm_id)
    resp_updateControllerstorage = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController.txt", "w", resp_updateControllerstorage)
    print stdurl+querycommand
    ###Stage6 Update Controller
    querycommand ='command=updateController&viscsiid=%s&type=configurevolumeiscsi' %(iscsi_id)
    resp_updateControlleriscsi = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControlleriscsi.txt", "w", resp_updateControlleriscsi)
    print stdurl+querycommand
	
    ####List Filesystem
#    querycommand ='command=listFileSystem'
#    resp_listFilesystem= sendrequest(stdurl, querycommand)
    print "ISCSI Volume %d Created" %(x)
    
print "ISCSI Volume Creation Done" 

######## To Make A iSCSI Volume Ends here






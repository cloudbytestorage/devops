import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, queryAsyncJobResultNegative

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
negativeFlag = 0

if len(sys.argv)== 3:
    if sys.argv[2].lower()== "negative":
        negativeFlag = 1;
    else:
        print "Argument is not correct.. Correct way as below"
        print " python NFSVolume.py config.txt"
        print " python NFSVolume.py config.txt negative"
        exit()
######## To Make A NFS Volume Begins here

print "NFS Volume Creation Begins"
###Stage 1 to 7 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    startTime = ctime()
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
    print "Accountid =", account_id


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
    print "Tsmid =", tsm_id
    print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s' %(tsm_id, config['volName%d' %(x)], config['volLatency%d' %(x)], config['volBlocksize%d' %(x)], config['volTpcontrol%d' %(x)], config['volThroughput%d' %(x)], config['volIopscontrol%d' %(x)], config['volIops%d' %(x)], config['volGraceallowed%d' %(x)], config['volMemlimit%d' %(x)], config['volNetworkspeed%d' %(x)]) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    print data

    # for negative testcase
    if negativeFlag == 1:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s&' %(qosgroup_id, tsm_id, config['volDatasetname%d' %(x)], config['volQuotasize%d' %(x)], dataset_id,config['volDeduplication%d' %(x)], config['volCompression%d' %(x)],config['volSync%d' %(x)],config['volRecordSize%d' %(x)],config['volBlocksize%d' %(x)],config['volMountpoint%d' %(x)],config['volProtocoltype%d' %(x)])
            resp_addFileSystem = sendrequest(stdurl, querycommand)
            filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
            data = json.loads(resp_addFileSystem.text)
            job_id=data["createvolumeresponse"]["jobid"]
            rstatus=queryAsyncJobResultNegative(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("NFSVolume %s Creation- negative testcase" %(config['volDatasetname%d' %(x)]), rstatus,startTime,endTime)  
        else:
            print "%s volume creation failed"  %(config['volDatasetname%d' %(x)])
            errorstatus= str(data['addqosgroupresponse']['errortext'])
            endTime = ctime()
            resultCollection("%s volume creation - negative testcase" %(config['volDatasetname%d' %(x)]), ["PASSED", errorstatus],startTime,endTime)

    # for positive testcase
    else:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s&' %(qosgroup_id, tsm_id, config['volDatasetname%d' %(x)], config['volQuotasize%d' %(x)], dataset_id,config['volDeduplication%d' %(x)], config['volCompression%d' %(x)],config['volSync%d' %(x)],config['volRecordSize%d' %(x)],config['volBlocksize%d' %(x)],config['volMountpoint%d' %(x)],config['volProtocoltype%d' %(x)])
            resp_addFileSystem = sendrequest(stdurl, querycommand)
            filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
            data = json.loads(resp_addFileSystem.text)
            job_id=data["createvolumeresponse"]["jobid"]
            rstatus=queryAsyncJobResult(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("NFSVolume %s Creation" %(config['volDatasetname%d' %(x)]), rstatus,startTime,endTime)
            print "%s created" %(config['volDatasetname%d' %(x)] )
        else:
             print "%s volume creation failed"  %(config['volDatasetname%d' %(x)])
             errorstatus= str(data['addqosgroupresponse']['errortext'])
             endTime = ctime()
             resultCollection("%s volume creation " %(config['volDatasetname%d' %(x)]), ["FAILED", errorstatus],startTime,endTime)
	
 
print "NFS Volume Creation Process Done"
######## To Make A NFS Volume Ends here


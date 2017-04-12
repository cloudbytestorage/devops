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
        print " python CIFSVolume.py config.txt"
        print " python CIFSVolume.py config.txt negative"
        exit()
######## To Make A CIFS Volume Begins here

print "CIFS Volume Creation Begins"
###Stage 1 to 7 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    startTime = ctime()
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
    #print "Poolid =" ,pool_id
    

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
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s' %(tsm_id, config['volCifsName%d' %(x)], config['volCifsLatency%d' %(x)], config['volCifsBlocksize%d' %(x)], config['volCifsTpcontrol%d' %(x)], config['volCifsThroughput%d' %(x)], config['volCifsIopscontrol%d' %(x)], config['volCifsIops%d' %(x)], config['volCifsGraceallowed%d' %(x)], config['volCifsMemlimit%d' %(x)], config['volCifsNetworkspeed%d' %(x)]) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)

    # for negative testcase
    if negativeFlag == 1:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s&' %(qosgroup_id, tsm_id, config['volCifsDatasetname%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id,config['volCifsDeduplication%d' %(x)], config['volCifsCompression%d' %(x)],config['volCifsSync%d' %(x)],config['volCifsRecordSize%d' %(x)],config['volCifsBlocklength%d' %(x)],config['volCifsMountpoint%d' %(x)],config['volCifsProtocoltype%d' %(x)])
            resp_addFileSystem = sendrequest(stdurl, querycommand)
            filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
            data = json.loads(resp_addFileSystem.text)
            job_id=data["createvolumeresponse"]["jobid"]
            rstatus=queryAsyncJobResultNegative(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("CIFSVolume %s Creation- negative testcase" %(config['volCifsDatasetname%d' %(x)]), rstatus,startTime,endTime) 
        else:
            print "%s volume creation failed"  %(config['volCifsDatasetname%d' %(x)])
            errorstatus= str(data['addqosgroupresponse']['errortext'])
            endTime = ctime()
            resultCollection("%s volume creation - negative testcase" %(config['volCifsDatasetname%d' %(x)]), ["PASSED", errorstatus],startTime,endTime)

    # for positive testcase
    else:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s&' %(qosgroup_id, tsm_id, config['volCifsDatasetname%d' %(x)], config['volCifsQuotasize%d' %(x)], dataset_id,config['volCifsDeduplication%d' %(x)], config['volCifsCompression%d' %(x)],config['volCifsSync%d' %(x)],config['volCifsRecordSize%d' %(x)],config['volCifsBlocklength%d' %(x)],config['volCifsMountpoint%d' %(x)],config['volCifsProtocoltype%d' %(x)])
            resp_addFileSystem = sendrequest(stdurl, querycommand)
            filesave("logs/AddFileSystem.txt", "w", resp_addFileSystem)
            data = json.loads(resp_addFileSystem.text)
            job_id=data["createvolumeresponse"]["jobid"]
            rstatus=queryAsyncJobResult(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("CIFSVolume %s Creation" %(config['volCifsDatasetname%d' %(x)]), rstatus,startTime,endTime)
            print "%s created" %(config['volCifsDatasetname%d' %(x)])
        else:
            print "%s volume creation failed"  %(config['volCifsDatasetname%d' %(x)])
            errorstatus= str(data['addqosgroupresponse']['errortext'])
            endTime = ctime()
            resultCollection("%s volume creation " %(config['volCifsDatasetname%d' %(x)]), ["FAILED", errorstatus],startTime,endTime)

 
print "CIFS Volume Creation process Done"
######## To Make A CIFS Volume Ends here



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
        print " python ISCSIVolume.py config.txt"
        print " python ISCSIVolume.py config.txt negative"


######## To Make A iSCSI Volume Begins here

print "ISCSI Volume Creation Begins"
###Stage 1 to 6 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    startTime = ctime()
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

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s' %(tsm_id, config['voliSCSIName%d' %(x)], config['voliSCSILatency%d' %(x)], config['voliSCSIBlocksize%d' %(x)], config['voliSCSITpcontrol%d' %(x)], config['voliSCSIThroughput%d' %(x)], config['voliSCSIIopscontrol%d' %(x)], config['voliSCSIIops%d' %(x)], config['voliSCSIGraceallowed%d' %(x)], config['voliSCSIMemlimit%d' %(x)], config['voliSCSINetworkspeed%d' %(x)]) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    print data    

    # for negative testcase
    if negativeFlag == 1:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s' %(qosgroup_id,tsm_id, config['voliSCSIDatasetname%d' %(x)],config['voliSCSIQuotasize%d' %(x)],dataset_id,config['voliSCSIDeduplication%d' %(x)],config['voliSCSICompression%d' %(x)],config['voliSCSISync%d' %(x)],config['voliSCSIBlocksize%d' %(x)],config['voliSCSIBlocklength%d' %(x)],config['voliSCSIMountpoint%d' %(x)],config['voliSCSIProtocoltype%d' %(x)])
            resp_create_volume = sendrequest(stdurl, querycommand)
            filesave("logs/AddVolume.txt", "w", resp_create_volume)
            data = json.loads(resp_create_volume.text)
            job_id=data["createvolumeresponse"]["jobid"];
            rstatus=queryAsyncJobResultNegative(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("ISCSIVolume %s Creation - Negative testcase" %(config['voliSCSIDatasetname%d' %(x)]), rstatus,startTime,endTime) 
        else:
            print "%s volume creation failed"  %(config['voliSCSIDatasetname%d' %(x)])
            errorstatus= str(data['addqosgroupresponse']['errortext'])
            endTime = ctime()
            resultCollection("%s volume creation - Negative testcase" %(config['voliSCSIDatasetname%d' %(x)]), ["PASSED", errorstatus],startTime,endTime)
    
    # for positive testcase
    else:
        ###Stage2 add Volume
        if not "errortext" in str(data):
            qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
            querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s' %(qosgroup_id,tsm_id, config['voliSCSIDatasetname%d' %(x)],config['voliSCSIQuotasize%d' %(x)],dataset_id,config['voliSCSIDeduplication%d' %(x)],config['voliSCSICompression%d' %(x)],config['voliSCSISync%d' %(x)],config['voliSCSIBlocksize%d' %(x)],config['voliSCSIBlocklength%d' %(x)],config['voliSCSIMountpoint%d' %(x)],config['voliSCSIProtocoltype%d' %(x)])
            resp_create_volume = sendrequest(stdurl, querycommand)
            filesave("logs/AddVolume.txt", "w", resp_create_volume)
            data = json.loads(resp_create_volume.text)
            job_id=data["createvolumeresponse"]["jobid"];
            rstatus=queryAsyncJobResult(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection("ISCSIVolume %s Creation" %(config['voliSCSIDatasetname%d' %(x)]), rstatus,startTime,endTime)
            print "\n%s created\n" %(config['voliSCSIDatasetname%d' %(x)])
        else:
            print "%s volume creation failed"  %(config['voliSCSIDatasetname%d' %(x)])
            errorstatus= str(data['addqosgroupresponse']['errortext'])
            endTime = ctime()
            resultCollection("%s volume creation" %(config['voliSCSIDatasetname%d' %(x)]), ["FAILED", errorstatus],startTime,endTime)

print "ISCSI Volume Creation process Done" 

######## To Make A iSCSI Volume Ends here


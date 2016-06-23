import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

######## To Make A FC Volume Begins here

print "FC Volume Creation Begins\n"
###Stage 1 to 6 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_fcVolumes'])+1):
    startTime = ctime()
#for x in range (1, NooffcVolumes+1):
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['volfcPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
 #  print "Poolid = %d" ,pool_id


    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volfcAccountName%d' %(x)]):
            account_id = account['id']
            break
 #  print "Accountid =", account_id


    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"]["listTsm"]
    for listTsm in tsms:
        if listTsm['name'] == "%s" %(config['volfcTSMName%d' %(x)]):
            tsm_id = listTsm['id']
	    dataset_id = listTsm['datasetid']
            break
  # print "Tsmid =", tsm_id
  # print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s' %(tsm_id, config['volfcName%d' %(x)], config['volfcLatency%d' %(x)], config['volfcBlocksize%d' %(x)], config['volfcTpcontrol%d' %(x)], config['volfcThroughput%d' %(x)], config['volfcIopscontrol%d' %(x)], config['volfcIops%d' %(x)], config['volfcGraceallowed%d' %(x)], config['volfcMemlimit%d' %(x)], config['volfcNetworkspeed%d' %(x)]) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    qosgroup_id=data["addqosgroupresponse"]["qosgroup"]["id"]
  # print "QosGroup id=",qosgroup_id

    ###Stage2 add Volume
    querycommand = 'command=createVolume&qosgroupid=%s&tsmid=%s&name=%s&quotasize=%s&datasetid=%s&deduplication=%s&compression=%s&sync=%s&recordsize=%s&blocklength=%s&mountpoint=%s&protocoltype=%s' %(qosgroup_id,tsm_id, config['volfcDatasetname%d' %(x)],config['volfcQuotasize%d' %(x)],dataset_id,config['volfcDeduplication%d' %(x)],config['volfcCompression%d' %(x)],config['volfcSync%d' %(x)],config['volfcBlocksize%d' %(x)],config['volfcBlocklength%d' %(x)],config['volfcMountpoint%d' %(x)],config['volfcProtocoltype%d' %(x)])
    resp_addVolume2 = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolume.txt", "w", resp_addVolume2)
    data = json.loads(resp_addVolume2.text)
    job_id=data["createvolumeresponse"]["jobid"]
    #queryAsyncJobResult(stdurl, job_id);
    rstatus=queryAsyncJobResult(stdurl, job_id);
    print rstatus
    endTime = ctime()
    resultCollection("FCVolume %s Creation" %(config['volfcDatasetname%d' %(x)]), rstatus,startTime,endTime) 
    print "\n%s created\n" %(config['volfcDatasetname%d' %(x)])
    

print "FC Volume Creation Done" 

######## To Make A fc Volume Ends here






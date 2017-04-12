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
        print " python Pool.py config.txt"
        print " python Pool.py config.txt negative"
        exit()
######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
print "Pool Creation Begins"
timetrack("Pool Creation Begins")

###To List the Current Number of Sites 
for x in range(1, int(config['Number_of_Pools'])+1):
    startTime = ctime()
    ### To ListController  and get Diskids
    querycommand = 'command=listController'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/ListController.txt", "w", resp_listController)
    data = json.loads(resp_listController.text)
    controllers = data["listControllerResponse"]["controller"]
    print controllers
    disks=""
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
                disk_list_id += "%3B"

    ####### Clear the Pools
    querycommand = 'command=clearPool&name=%s&id=%s' %(config['poolName%d' %(x)], controller_id)
    resp_clearPool= sendrequest(stdurl, querycommand)
    filesave("logs/clearPool.txt", "w", resp_clearPool)

    ### Stage1 addHAPool
    querycommand = 'command=addHAPool&controllerid=%s&siteid=%s&clusterid=%s&diskslist=%s&name=%s&graceallowed=%s&iops=%s&latency=%s&sectorsize=%s&grouptype=%s&scsireserved=true' %(controller_id,site_id, cluster_id, disk_list_id, config['poolName%d' %(x)], config['poolGraceAllowed%d' %(x)], config['poolIops%d' %(x)], config['poolLatency%d' %(x)], config['poolSectorsize%d' %(x)], config['poolGroupType%d' %(x)])
    resp_addHAPool = sendrequest(stdurl, querycommand)
    filesave("logs/AddHAPool.txt", "w", resp_addHAPool)
    data = json.loads(resp_addHAPool.text)
    #print data
    job_id = data["addHAPoolResponse"]["jobid"]
    #queryAsyncJobResult(stdurl, job_id)

    # for negative testcase
    if negativeFlag == 1:

        rstatus=queryAsyncJobResultNegative(stdurl, job_id);
        print rstatus
        endTime = ctime()
        resultCollection("Pool %s Creation- negative testcase" %(config['poolName%d' %(x)]), rstatus,startTime,endTime) 
    
    # for positive testcase
    else :
        
        rstatus=queryAsyncJobResult(stdurl, job_id);
        print rstatus
        endTime = ctime()
        resultCollection("Pool %s Creation " %(config['poolName%d' %(x)]), rstatus,startTime,endTime)
        print "Pool %d Created" %(x)
    
print "Pool Creation Process " + rstatus[0] 
######## To Make A Pool Done


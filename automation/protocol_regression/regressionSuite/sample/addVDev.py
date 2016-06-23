import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
print "VDev Creation Begins"
timetrack("VDev Creation Begins")

###To List the Current Number of Sites 
for x in range(1, int(config['Number_of_VDevs'])+1):
    ### To ListController  and get Diskids
    querycommand = 'command=listHAPool'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/listPool.txt", "w", resp_listController)
    data = json.loads(resp_listController.text)
    pools = data["listHAPoolResponse"]["hapool"]
    for pool in pools:
        if pool['name'] == "%s" %(config['DiskPoolName%d' %(x)]): 
	    pool_id = pool['id']
	    site_id = pool['siteid']
	    cluster_id = pool['haclusterid']
            nodeName = pool['controllerName']
	    break

for x in range(1, int(config['Number_of_VDevs'])+1):
    startTime = ctime()
    ### To ListController  and get Diskids
    querycommand = 'command=listController'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/ListController.txt", "w", resp_listController)
    data = json.loads(resp_listController.text)
    controllers = data["listControllerResponse"]["controller"]
    for controller in controllers:
        if controller['name'] == "%s" %(nodeName):
            disks = controller['disks']
            break
    disk_list_id = ""
    for disk in disks:
        for y in range (1, int(config['NumOfDisksAllocated%d' %(x)])+1):
            if "%s" %(config['DiskLabel%d%d' %(y,x)]) in disk['label']:
                disk_list_id += disk['id']
                disk_list_id += "%3B"
    querycommand = 'command=addDiskGroup&clusterid=%s&poolid=%s&grouptype=%s&sectorsize=%s&diskslist=%s&totaliops=%s&totalthroughput=%s&latency=%s' %(cluster_id,pool_id,config['DiskGroupType%d' %(x)],config['DiskSectorsize%d' %(x)],disk_list_id,config['DiskTotalIops%d' %(x)],config['DiskTotalThroughput%d' %(x)],config['DiskLatency%d' %(x)])
    resp_addHAPool = sendrequest(stdurl, querycommand)
    filesave("logs/AddHAPool.txt", "w", resp_addHAPool)
    data = json.loads(resp_addHAPool.text)
    job_id = data["addDiskgroupResponse"]["jobid"]
    #queryAsyncJobResult(stdurl, job_id)
    rstatus=queryAsyncJobResult(stdurl, job_id);
    print rstatus
    endTime = ctime()
    resultCollection("VDev with DiskGroupType %s Creation" %(config['DiskGroupType%d' %(x)]), rstatus,startTime,endTime) 
   
    print "VDev %d Created" %(x)
    
timetrack("VDev Creation Done")
print "VDev Creation Done"


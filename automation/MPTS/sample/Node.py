import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

########To Add Node
#########To List the Current Number of Sites 
print "Node Creation Begins"
timetrack("Node Creation Begins")
for x in range(1, int(config['Number_of_Nodes'])+1):
    startTime = ctime()
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentSitesList.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    sites = data["listSiteResponse"]["site"]
    site = [y for y in sites if y["name"] == "%s" %(config['nodeSiteName%d'%(x)])].pop(0)
    site_id = site["id"] #if site else None

    ###To List the Current Number of HA
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand) 
    filesave("logs/CurrentHAClustersList.txt", "w", resp_listHACluster) 
    data = json.loads(resp_listHACluster.text)
    haclusters = data["listHAClusterResponse"]["hacluster"]
    hacluster = [y for y in haclusters if y["name"] == "%s" %(config['nodeClusterName%d'%(x)]) ].pop(0)
    hacluster_id = hacluster["id"] #if site else None

    #Actual Node Addtion happens here
    querycommand = 'command=addController&name=%s&siteid=%s&ipaddress=%s&clusterid=%s' %(config['nodeName%d' %(x)], site_id, config['nodeIP%d' %(x)], hacluster_id) 
    resp_addController = sendrequest(stdurl, querycommand)
    filesave("logs/NodeCreation.txt", "w", resp_addController) 
    data = json.loads(resp_addController.text)
    job_id = data["addControllerResponse"]["jobid"]
    #queryAsyncJobResult(stdurl, job_id);
    rstatus=queryAsyncJobResult(stdurl, job_id);
    print rstatus
    endTime = ctime()
    resultCollection("Node %s Import" %(config['nodeName%d' %(x)]), rstatus,startTime,endTime) 
    print "Node %d Created" %(x)
timetrack("Node Creation Done")
print "Node Creation Done"

########### Node Addtion Complete 

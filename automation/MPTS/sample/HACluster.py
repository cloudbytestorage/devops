import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

#########To Add Cluster
#########To List the Current Number of Sites 
print "HA Cluster Creation Begins"
timetrack("HA Cluster Creation Begins")
createFlag = True
startTime = ctime()
for x in range(1, int(config['Number_of_Clusters'])+1):
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentSitesList.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    sites = data["listSiteResponse"]["site"]
    site = [y for y in sites if y["name"] == "%s" %(config['clusterSiteName%d'%(x)])].pop(0)
    site_id = site["id"] #if site else None

###CreateHACluster Stage1 and Stage2
    ###Stage1 createHACluster
    #querycommand = 'command=createHACluster&clustername=%s&description=%s&siteid=%s' %(config['clusterName%d' %(x)], config['clusterDescription%d' %(x)], site_id) 
    #resp_createHACluster = sendrequest(stdurl, querycommand)
    #filesave("logs/ClusterCreation.txt", "w", resp_createHACluster) 
    #data = json.loads(resp_createHACluster.text)
    #print data
    #exit()
    #hacluster_id=data["createHAClusterResponse"]["hacluster"]["id"]

    ###createHACluster
    startTime = ctime()
    querycommand = 'command=createHACluster&type=healthcheck&siteid=%s&startip=%s&endip=%s&clustername=%s&sdescription=%s' %(site_id, config['clusterStartIP%d' %(x)], config['clusterEndIP%d' %(x)], config['clusterName%d' %(x)], config['clusterDescription%d' %(x)])
    resp_createHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/ClusterCreationComplete.txt", "w", resp_createHACluster)
    data = json.loads(resp_createHACluster.text)
    endTime = ctime()
    if 'errorcode' in str(data['createHAClusterResponse']):
        createFlag = False
        errormsg = str(data['createHAClusterResponse']['errortext'])
        resultCollection('Not able to create HACluster', ['FAILED', errormsg], startTime, endTime)

if createFlag:
    endTime = ctime()
    resultCollection('HACluster created successfully', ['PASSED', ''], startTime, endTime)
###Ends Here Cluster Creation

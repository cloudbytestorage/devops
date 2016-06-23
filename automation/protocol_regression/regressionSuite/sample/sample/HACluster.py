import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

#########To Add Cluster
#########To List the Current Number of Sites 
print "HA Cluster Creation Begins"
timetrack("HA Cluster Creation Begins")
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
    querycommand = 'command=createHACluster&clustername=%s&description=%s&siteid=%s' %(config['clusterName%d' %(x)], config['clusterDescription%d' %(x)], site_id) 
    resp_createHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/ClusterCreation.txt", "w", resp_createHACluster) 
    data = json.loads(resp_createHACluster.text)
    hacluster_id=data["createHAClusterResponse"]["hacluster"]["id"]

    ###Stage2 createHAClusterNetwork
    querycommand = 'command=createHAClusterNetworkRule&type=healthcheck&network=&subnet=&startip=%s&endip=%s&ipaddress=&clusterid=%s' %(config['clusterStartIP%d' %(x)], config['clusterEndIP%d' %(x)],hacluster_id)
    resp_createHAClusterNetworks = sendrequest(stdurl, querycommand)
    filesave("logs/ClusterCreationComplete.txt", "w", resp_createHAClusterNetworks) 
    print "HA Cluster %d Created" %(x)
timetrack("HA Cluster Creation Done")
print "HA Cluster Creation Done"
###Ends Here Cluster Creation



import json
import requests

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    #print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;
 
#### Function(s) Declartion Ends


config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
#########To Add the Sites
print "Site Creation Begins"
for x in range(1, int(config['Number_of_Sites'])+1):
    querycommand = 'command=createSite&location=%s&name=%s&description=%s' %(config['siteLocation%d' %(x)], config['siteName%d'%(x)], config['siteDescription%d' %(x)])
    resp_createSite = sendrequest(stdurl, querycommand)
    filesave("logs/AddSiteList.txt", "w", resp_createSite)
    print "Site %d Creation Begins" %(x)
print "Site Creation Done" 

#########To Add Cluster
#########To List the Current Number of Sites 
print "HA Cluster Creation Begins"
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
print "HA Cluster Creation Done"

###Ends Here Cluster Creation

########To Add Node
#########To List the Current Number of Sites 
print "Node Creation Begins"
for x in range(1, int(config['Number_of_Nodes'])+1):
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
    print "Node %d Created" %(x)
print "Node Creation Begins"

########### Node Addtion Complete 



import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
    

###TO list the clusters

print "%s" %(config['Number_of_Clusters'])
for x in range(1, int(config['Number_of_Laggs'])+1):
    cluster_id = ""
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/listHACluster.txt", "w",resp_listHACluster)
    data = json.loads(resp_listHACluster.text)
    clusters = data['listHAClusterResponse']['count']
    cluster_list = data['listHAClusterResponse']['hacluster']
    for listHACluster in cluster_list:
        if listHACluster['name'] == config['laggClusterName%d' % x]:
            cluster_id = data['listHAClusterResponse']['hacluster'][0]['id']
            print "ClusterID = %s" %(cluster_id)
            break   
  
    querycommand = 'command=listSharedNICs&clusterid=%s' %(cluster_id)
    resp_listSharedNICs = sendrequest(stdurl, querycommand)
    data=json.loads(resp_listSharedNICs.text)
    sharedNICid = data['listSharedNICsResponse']['nic']
    filesave("logs/listSharedNICs.txt","w", resp_listSharedNICs)
    nic_id = "";
    for listSharedNICs in sharedNICid:
        for y in range(1, int(config['Number_of_Interfaces%d' % x ])+1):
            if listSharedNICs['name'] == config['laggInterface%d%d' %(y,x)]:
               nic_id += listSharedNICs['id']
               nic_id += ","


    ###TO Add Lagg Interface
    querycommand = 'command=addLagg&name=lagg%s&clusterid=%s&protocoltype=%s&portslist=%s' %(config['laggTag%d' %(x)],cluster_id,config['laggType%d'%(x)],nic_id)
    resp_addLagg = sendrequest(stdurl, querycommand)
    filesave("logs/addLagg.txt", "w", resp_addLagg)
    data = json.loads(resp_addLagg.text)
    if not "errortext" in str(data):
        print "Lagg added successfully"
        resultCollection("Lagg Addition %s Verification from Devman" %(config['laggTag%d' %(x)]), ["PASSED", ""]) 
    else:
        print "Lagg addition Failed "
        errorstatus= str(data['addLaggResponse']['errortext'])
        resultCollection("Lagg Addition %s Verification from Devman" %(config['LaggTag%d' %(x)]), ["FAILED", errorstatus]) 

    routput = getControllerInfo("20.10.59.51", "test", "ifconfig lagg%s| grep status | awk '{print $2}'" %(config['laggTag%d' %(x)]), "logs/test" );
   
    if "active" in routput:
        resultCollection("Lagg Addition lagg%s Verification from Node" %(config['laggTag%d' %(x)]), ["PASSED", ""]) 
    else:
        resultCollection("Lagg Addition lagg%s Verification from Node" %(config['laggTag%d' %(x)]), ["FAILED", str(routput)]) 



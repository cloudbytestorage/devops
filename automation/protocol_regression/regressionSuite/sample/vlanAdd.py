import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
    

###TO list the clusters

print "%s" %(config['Number_of_Clusters'])
for x in range(1, int(config['Number_of_Vlans'])+1):
    startTime = ctime()
    cluster_id = ""
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/listHACluster.txt", "w",resp_listHACluster)
    data = json.loads(resp_listHACluster.text)
    clusters = data['listHAClusterResponse']['count']
    cluster_list = data['listHAClusterResponse']['hacluster']
    for listHACluster in cluster_list:
        if listHACluster['name'] == config['vlanClusterName%d' % x]:
            cluster_id = data['listHAClusterResponse']['hacluster'][0]['id']
            print "ClusterID = %s" %(cluster_id)
            break   
  
    querycommand = 'command=listSharedNICs&clusterid=%s' % cluster_id
    resp_listSharedNICs = sendrequest(stdurl, querycommand)
    data=json.loads(resp_listSharedNICs.text)
    sharedNICid = data['listSharedNICsResponse']['nic']
    filesave("logs/listSharedNICs.txt","w", resp_listSharedNICs)
    for listSharedNICs in sharedNICid:
        if listSharedNICs['name'] == config['vlanInterface%d' %x]:
            nic_id = listSharedNICs['id']
            break

    ###TO Add VLAN Interface
    querycommand = 'command=addVLAN&clusterid=%s&tag=%s&parentnicid=%s' % (cluster_id,config['vlanTag%d' %(x)],nic_id)
    resp_addVLAN = sendrequest(stdurl, querycommand)
    filesave("logs/addVLAN.txt", "w", resp_addVLAN)
    data = json.loads(resp_addVLAN.text)
    if not "errortext" in str(data):
        print "VLAN added successfullyi"
        endTime = ctime()
        resultCollection("VLAN Addition %s Verification from Devman" %(config['vlanTag%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "VLAN addition Failed "
        errorstatus= str(data['vlanResponse']['errortext'])
        endTime = ctime()
        resultCollection("VLAN Addition %s Verification from Devman" %(config['vlanTag%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 

    routput = getControllerInfo("20.10.57.103", "test", "ifconfig vlan%s | grep parent" %(config['vlanTag%d' %(x)]), "logs/test");

    if (("%s" %(config['vlanTag%d' %(x)]) in str(routput)) and ("%s" %(config['vlanInterface%d' %(x)]) in str(routput))):
        endTime = ctime()
        resultCollection("VLAN Addition %s Verification from Node" %(config['vlanTag%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        endTime = ctime()
        resultCollection("VLAN Addition %s Verification from Node" %(config['vlanTag%d' %(x)]), ["FAILED", str(routput)],startTime,endTime) 








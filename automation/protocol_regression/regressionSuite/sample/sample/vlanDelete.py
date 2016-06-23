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

    vlan_id = ""
    for listSharedNICs in sharedNICid:
        vlans = data['listSharedNICsResponse']['nic']
        for vlan in vlans:
            if vlan['name'] == "vlan%s" %(config['vlanTag%d' %x]):
                #vlan_id = data['listSharedNICsResponse']['nic'][0]['id']
                vlan_id = vlan['id']
                break
    
    ###TO Delete VLAN Interface
    querycommand = 'command=deleteVLAN&id=%s' % (vlan_id)
    resp_deleteVLAN = sendrequest(stdurl, querycommand)
    filesave("logs/deleteVLAN.txt", "w", resp_deleteVLAN)
    data = json.loads(resp_deleteVLAN.text)
    if not "errortext" in str(data):
        endTime = ctime()
        print "VLAN deleteed successfully"
        resultCollection("VLAN deletion %s Verification from Devman" %(config['vlanTag%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "VLAN deleteition Failed "
        errorstatus= str(data['deleteVLANResponse']['errortext'])
        endTime = ctime()
        resultCollection("VLAN deletion %s Verification from Devman" %(config['vlanTag%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 

    routput = getControllerInfo("20.10.57.103", "test", "ifconfig vlan%s | grep parent" %(config['vlanTag%d' %(x)]), "logs/test");

    if (("%s" %(config['vlanTag%d' %(x)]) in str(routput)) and ("%s" %(config['vlanInterface%d' %(x)]) in str(routput))):
        endTime = ctime()
        resultCollection("VLAN deletion %s Verification from Node" %(config['vlanTag%d' %(x)]), ["FAILED", str(routput)],startTime,endTime) 
    else:
        endTime = ctime()
        resultCollection("VLAN deletion %s Verification from Node" %(config['vlanTag%d' %(x)]), ["PASSED", ""],startTime,endTime) 








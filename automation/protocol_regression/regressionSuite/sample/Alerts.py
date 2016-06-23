import json
import md5
import requests
import time

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    print url+querystring
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
#########List All Alerts
querycommand = 'command=listAlerts'
resp_listAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAlerts.txt", "w", resp_listAlerts)

#########List All Acknowledged Alerts
querycommand = 'command=listAlerts&show=acked'
resp_listAckedAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAckedAlerts.txt", "w", resp_listAckedAlerts)


#########Acknowlege Bulk Alerts
querycommand = 'command=acknowledgeAlerts&type=all&acknowledgedesc=AckAll'
resp_listAckAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAckAlerts.txt", "w", resp_listAckAlerts)

#########List All Events
querycommand = 'command=listEvents'
resp_listEvents = sendrequest(stdurl, querycommand)
filesave("logs/ListEvents.txt", "w", resp_listEvents)


#########Refresh Hardware from Node
querycommand = 'command=listController'
resp_listController = sendrequest(stdurl, querycommand)
filesave("logs/listController.txt", "w", resp_listController)
data = json.loads(resp_listController.text)
controllers = data["listControllerResponse"]["controller"]
for controller in controllers:
    controller_id = controller['id']
    controller_name = controller['name']
    ### Refresh Hardware All
    querycommand = 'command=discoverController&id=%s&type=all' %(controller_id)
    resp_refreshHardwareAll= sendrequest(stdurl, querycommand)
    filesave("logs/RefreshHardwareAll.txt", "w", resp_refreshHardwareAll)
    ### Refresh Storage (Only Disks)
    querycommand = 'command=discoverController&id=%s&type=disks' %(controller_id)
    resp_refreshHardwareDisks= sendrequest(stdurl, querycommand)
    filesave("logs/RefreshHardwareDisks.txt", "w", resp_refreshHardwareDisks)
    ### Refresh Network (Only Nics)
    querycommand = 'command=discoverController&id=%s&type=nics' %(controller_id)
    resp_refreshHardwareNics= sendrequest(stdurl, querycommand)
    filesave("logs/RefreshHardwareNics.txt", "w", resp_refreshHardwareNics)
    print "Refresh Hardware of the controller", controller_name

##########Refresh Hardware HACluster
querycommand = 'command=listHACluster'
resp_listHACluster = sendrequest(stdurl, querycommand)
filesave("logs/listHACluster.txt", "w", resp_listHACluster)
data = json.loads(resp_listHACluster.text)
haclusters = data["listHAClusterResponse"]["hacluster"]
for hacluster in haclusters:
    hacluster_id = hacluster['id']
    hacluster_name = hacluster['name']
    ### Refresh Storage (Only Disks)
    querycommand = 'command=discoverClusterNodes&id=%s&type=disks' %(hacluster_id)
    resp_refreshHwDisks_hacluster = sendrequest(stdurl, querycommand)
    filesave("logs/RefreshHACluster", "w", resp_refreshHwDisks_hacluster)
    print "RefreshHardware disks in HACluster", hacluster_name


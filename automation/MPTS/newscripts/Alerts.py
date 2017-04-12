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

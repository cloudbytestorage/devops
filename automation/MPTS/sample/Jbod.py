import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

###Add a disk Enclosure
print "JBOD Creation Begins"
timetrack("JBOD Creation Begins")

### 3 Stage process, first 1 to listController and get site_id, cluster_id, controller_id, target and bus

querycommand = 'command=listController'
resp_listController = sendrequest(stdurl, querycommand)
filesave("logs/CurrentControllerList.txt", "w", resp_listController) 
data = json.loads(resp_listController.text)
controllers = data["listControllerResponse"]["controller"]

for controller in controllers:
    if controller['name'] == "%s" %(config['nodeName1']): #Still Can be parameterised for Node loop 
        disks = controller['disks']
        controller_id = controller['id']
        site_id = controller['siteid']
        cluster_id = controller['clusterid']
        break

target, bus = "", ""
lunnumber=[]
for disk in disks:
    target += disk['target']
    target += ","
    bus += disk['bus']
    bus += ","
    lunnumber.append("0")

lunnumber=','.join(lunnumber)

### Stage 1 Create JBOD
querycommand = 'command=createJBOD&clusterid=%s&name=%s&type=%s&rows=%s&cols=%s' %(cluster_id, config['jbodName1'], config['type'],config['rows'],config['cols'])
resp_createJBOD = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODList.txt", "w", resp_createJBOD) 
data = json.loads(resp_createJBOD.text)
jbod_id=data["createJbodResponse"]["jbod"]["id"]

### Stage 2 UpdatediskLabels
querycommand = 'command=updateDiskLabels&jbodid=%s&controllerid=%s&bus=%s&targetnumber=%s&baynumber=%s&lunnumber=%s' %(jbod_id, controller_id, bus, target, config['baynumber1'],lunnumber)
resp_updateDiskLabels = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updateDiskLabels) 

### Stage 3 UpdateHAconfiglabels
querycommand = 'command=updatehaconfiglabel&clusterid=%s' %(cluster_id)

resp_updatehaconfiglabel = sendrequest(stdurl, querycommand)
filesave("logs/CurrentJBODUpdate.txt", "w", resp_updatehaconfiglabel) 

timetrack("JBOD Creation Done")
print "JBOD Creation Done"
############ Disk Enclosure Done



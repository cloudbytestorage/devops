import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, getoutput, executeCmd

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

def all_same(items):
    return all(x == "ONLINE\n" for x in items)

if len(sys.argv)<6:
    print "Argument is not correct.. Correct way as below"
    print "python rebootNode.py config.txt reboot node1IP node1passwd node2IP node2passwd"
    exit()

mode = sys.argv[2]
IP1 = sys.argv[3]
passwd1 = sys.argv[4]
IP2 = sys.argv[5]
passwd2 = sys.argv[6]

getControllerInfo(IP1,passwd1,"reboot","r.txt")
pingvalue = executeCmd('ping -c 1 %s'%IP1)

while pingvalue[0] == "PASSED": 
    pingvalue = executeCmd('ping -c 1 %s'%IP1)
    time.sleep(1)
print pingvalue[0]
startTime = ctime()
time.sleep(120)
endTime = ctime()

querycommand = 'command=listController'
resp_listcontroller = sendrequest(stdurl, querycommand)
filesave("logs/ListController.txt", "w", resp_listcontroller)
data = json.loads(resp_listcontroller.text)
#print data
if "controller" in data["listControllerResponse"]:
    controllerlist = data["listControllerResponse"]["controller"]
else:
    print "There are no Nodes"
    controllerlist = {}

for controller in controllerlist:
    startTime = ctime()
    status = controller['managedstate']
    ctrl_name = controller['name']
    ctrl_id = controller['id']
    ctrl_ip = controller['hamanageripaddress']
    if IP1 == "%s" %(ctrl_ip):
        zpoolList1 = list();
        for y in range(1, int(config['Number_of_Pools'])+1):
            if ctrl_name == "%s" %(config['poolNodeName%d' %(y)]):
                pool = "%s" %(config['poolName%d' %(y)])
                zpoolList1.append(pool)
        health = list();
        for x in range(0,len(zpoolList1)):
            value = getControllerInfo(IP2, passwd2, "zpool list | grep %s | awk '{print $7}' " %zpoolList1[x],"zpoolList.txt")
            print zpoolList1[x]+" "+value
            health.append(value)
            
            flag = all_same(health)
            print flag
            if flag:
                resultCollection(" %s rebooted and take over process " %(ctrl_name),["PASSED",""], startTime, endTime)
            else:
                resultCollection(" %s rebooted and take over process " %(ctrl_name),["FAILED",""], startTime, endTime)


import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo, executeCmd

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

def all_same(items):
    return all(x == "ONLINE\n" for x in items)

if len(sys.argv)<6:
    print "Argument is not correct.. Correct way as below"
    print "python nodeToMode.py config.txt maintenance/available node1IP node1passwd node2IP node2passwd"
    exit()

mode = sys.argv[2]
IP1 = sys.argv[3]
passwd1 = sys.argv[4]
IP2 = sys.argv[5]
passwd2 = sys.argv[6]

if mode.lower()== "maintenance":
    mode = "Maintenance";
elif  mode.lower()== "available":
    mode = "Available";
else:
    print " third argument has to be maintenance or available "
    print "Argument is not correct.. Correct way as below"
    print "python nodeToMode.py config.txt maintenance/available node1IP node1passwd node2IP node2passwd"
    exit()

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

pingvalue = executeCmd('ping -c 1 %s'%IP1)
count = 1
while pingvalue[0] == "FAILED":
    if count == 300:
        print "%s is unreachable"%IP1
        resultCollection("%s is unreachable " %(IP1),["FAILED",""], startTime, endTime)
        exit()
    pingvalue = executeCmd('ping -c 1 %s'%IP1)
    count+=1
    time.sleep(2)
print pingvalue[0]
print count

time.sleep(20)

for controller in controllerlist:
    startTime = ctime()
    status = controller['managedstate']
    #print status
    #print mode
    ctrl_name = controller['name']
    ctrl_id = controller['id']
    ctrl_ip = controller['hamanageripaddress']
    if IP1 == "%s" %(ctrl_ip): 
        if status != mode:
            # Maintenance/Available mode
            startTime = ctime()
            print "%s is in %s Mode so moving to %s Mode" %(controller['name'],controller['managedstate'],mode )
            querycommand = 'command=changeControllerState&id=%s&state=%s'%(controller['id'],mode)
            resp_stateofnode= sendrequest(stdurl, querycommand)
            filesave("logs/nodemaintenance.txt", "w", resp_stateofnode)
            data1 = json.loads(resp_stateofnode.text)
            print data1
            hajob_id = data1["changeControllerStateResponse"]["controller"]["hajobid"]
            querycommand = 'command=listHAJobActivities&hajobid=%s' %(hajob_id)
            hajob=sendrequest(stdurl, querycommand)
            filesave("logs/hajob.txt", "w", hajob)
            data2= json.loads(hajob.text)
            job_id = data2["listHAJobActivitiesResponse"]["jobid"]
            rstatus=queryAsyncJobResult(stdurl, job_id);
            print rstatus
            endTime = ctime()
            resultCollection(" %s changing state to %s mode from UI" %(ctrl_name,mode),rstatus, startTime, endTime)

            zpoolList1 = list();
            for y in range(1, int(config['Number_of_Pools'])+1):
                if ctrl_name == "%s" %(config['poolNodeName%d' %(y)]):
                    pool = "%s" %(config['poolName%d' %(y)])
                    zpoolList1.append(pool)
            #l = len(zpoolList1) - 1
            health = list();
            if mode == "Maintenance":
                for x in range(0,len(zpoolList1)):
                    value = getControllerInfo(IP2, passwd2, "zpool list | grep %s | awk '{print $7}' " %zpoolList1[x],"zpoolList.txt")
                    print zpoolList1[x]+" "+value
                    health.append(value)
                #print health
                flag = all_same(health)
                print flag
                if flag:
                    resultCollection(" %s changing state to %s mode from controller" %(ctrl_name,mode),["PASSED",""], startTime, endTime)
                else:
                    resultCollection(" %s changing state to %s mode from controller" %(ctrl_name,mode),["FAILED",""], startTime, endTime)
            else:
                for x in range(0,len(zpoolList1)):
                    value = getControllerInfo(IP1, passwd1, "zpool list | grep %s | awk '{print $7}' " %zpoolList1[x],"zpoolList.txt")
                    print zpoolList1[x]+" "+value
                    health.append(value)
                #print health
                flag = all_same(health)
                print flag
                if flag:
                    resultCollection(" %s changing state to %s mode from controller" %(ctrl_name,mode),["PASSED",""], startTime, endTime)
                else:
                    resultCollection(" %s changing state to %s mode from controller" %(ctrl_name,mode),["FAILED",""], startTime, endTime)

        else:
            startTime = ctime()
            print "%s is in already in %s Mode " %(controller['name'],mode)
            endTime = ctime()
            resultCollection("%s is in already in %s Mode " %(controller['name'],mode),["FAILED",""], startTime, endTime)





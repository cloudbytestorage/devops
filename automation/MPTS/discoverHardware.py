import sys
import json
import time
from time import ctime
from cbrequest import sendrequest, filesave, getControllerInfo, resultCollection, queryAsyncJobResult, configFile, executeCmd

### discover hardware 
if len(sys.argv)<5:
    print "Argument is not correct.. Correct way as below"
    print "python refreshHardware.py snapshot.txt type_of_cmd(all/disks) NODE_IP NODE_PASSWD"
    exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

type = sys.argv[2]
ip = sys.argv[3]
passwd = sys.argv[4]
startTime = ctime()
if type == 'all':
    component = 'hardware'
elif type == 'disks':
    component = 'storage'
else:
    print 'Second argument should be all/disks'
    exit()
querycommand = 'command=listController'
resp_listcontroller = sendrequest(stdurl, querycommand)
filesave("logs/ListController.txt", "w", resp_listcontroller)
data = json.loads(resp_listcontroller.text)
if 'controller' in data["listControllerResponse"]:
    controllers = data["listControllerResponse"]["controller"]
elif 'errorcode' in data["listControllerResponse"]:
    endTime = ctime()
    errormsg = data["listControllerResponse"]['errortext']
    resultCollection('Not able to list Controllers', ['BLOCKED', errormsg], startTime, endTime)
    exit()
else:
    endTime = ctime()
    print "There are no Nodes"
    resultCollection('There is no controller available, further %s refress test case skipped' %(component), ['BLOCKED', ''], startTime, endTime)
    exit()
flag = 1
for controller in controllers:
    ctrl_name = controller['name']
    ctrl_id = controller['id']
    ctrl_ip = controller['hamanageripaddress']
    if ctrl_ip == ip:
        flag = 0
        break
if flag:
    endTime = ctime()
    resultCollection('There is no controller with ip %s, So test case for refresh %s is:' %(ip, component), ['BLOCKED', ''], startTime, endTime)
else:
    querycommand = 'command=discoverController&id=%s&type=%s' %(ctrl_id, type)
    print querycommand
    resp_discoverController = sendrequest(stdurl, querycommand)
    filesave("logs/disciverhardware.txt", "w", resp_discoverController)
    data2 = json.loads(resp_discoverController.text)
    if 'errorcode' in data2['discoverControllerResponse']:
        endTime = ctime()
        errormsg = data2['discoverControllerResponse']['errortext']
        resultCollection('Not able to refresh %s' %(component), ['FAILED', errormsg], startTime, endTime)
    else:
        endTime = ctime()
        resultCollection('refresh %s successfully' %(component), ['PASSED', ''], startTime, endTime)

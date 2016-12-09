import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, getControllerInfo

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

if len(sys.argv)< 4:
    print "Argument is not correct.. Correct way as below"
    print "python staticIPAdd.py config.txt NodeIP NodePassword"
    exit()
IP=sys.argv[2]
Password=sys.argv[3]
   


for x in range(1, int(config['Number_of_StaticIPs'])+1):
    startTime = ctime()
    ###TO list the ControllerID
    controller_id = ""
    querycommand = 'command=listController'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/listController.txt", "w",resp_listController)
    data = json.loads(resp_listController.text)
    controllers = data['listControllerResponse']['controller']
    #controller_list = data['listControllerResponse']['controller']
    #print controllers
    for controller in controllers:
        if controller['name'] == "%s" %(config['staticIPControllerName%d' %(x)]):
            #controller_id = data['listControllerResponse']['controller'][0]['id']
            controller_id = controller['id']
            #print "ControllerID = %s" %(controller_id)
            nics = controller['nics']
            #print nics
            for nic in nics:
                if nic['name'] == config['staticIPInterface%d' %x]:
                    nic_id = nic['nicid']
                    #print "Nic id %s" %(nic_id)
                    break


    querycommand = 'command=clearStaticIP&controllerid=%s&nicid=%s' %(controller_id, nic_id)
    resp_clearStaticIP = sendrequest(stdurl, querycommand)
    data=json.loads(resp_clearStaticIP.text)
    #staticIPResponse = data['nicResponse']
    #print data

    filesave("logs/clearStaticIP.txt","w", resp_clearStaticIP)

    if not "errortext" in str(data):
        endTime = ctime()
        print "Static IP Clear successfully"
        resultCollection("Static IP Clear %s Verification from Devman" %(config['staticIPInterface%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "Static IP Clear Failed "
        errorstatus= str(data['nicResponse']['errortext'])
        endTime = ctime()
        resultCollection("Static IP Clear %s Verification from Devman" %(config['staticIPInterface%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 

    routput = getControllerInfo(IP, Password, "ifconfig %s | grep inet" %(config['staticIPInterface%d' %(x)]), "logs/test");
    #print routput 

    if (("%s" %(config['staticIP%d' %(x)]) not in str(routput)) and ("%s" %(config['staticIPGateway%d' %(x)]) not in str(routput))):
        endTime = ctime()
        resultCollection("Static IP Addition %s Verification from Node" %(config['staticIPInterface%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        endTime = ctime()
        resultCollection("Static IP Addition %s Verification from Node" %(config['staticIPInterface%d' %(x)]), ["FAILED", str(routput)],startTime,endTime) 








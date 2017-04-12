import json
import sys
import md5
import fileinput
import requests
import time
from time import ctime
from cbrequest import sendrequest, filesave, configFile, resultCollection

config = configFile(sys.argv);

poolFlag = volumeFlag = 0
### python tpAlert.py config.txt type x, where type is volume/pool and x is the severity of TP alert 2 for critical and 3 for warning 

if len(sys.argv)< 4:
    print "Argument is not correct.. Correct way as below"
    print "python tpAlert.py config.txt type x"
    print "where type is volume/pool and x is the severity of TP alert 2 for critical and 3 for warning"
    exit()

if  sys.argv[2].lower()==  "%s" %("pool"):
    poolFlag == 1;
elif sys.argv[2].lower() == "%s" %("volume"):
    volumeFlag = 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python tpAlert.py config.txt type x"
    print "where type is volume/pool and x is the severity of TP alert 1 for error 2 for critical and 3 for warning and 4 for info"
    exit()

x = sys.argv[3]
print x

startTime = ctime()

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#########List All Alerts
querycommand = 'command=listAlerts'
resp_listAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAlerts.txt", "w", resp_listAlerts)
data = json.loads(resp_listAlerts.text)


#### Finding TP Alert for volume
if volumeFlag == 1:
    alerts=data["listalertsresponse"]["alert"]
    print alerts
    for alert in alerts:
        if "space" in alert['subject'] and alert['description']=="Volume Capacity":
            if alert['severity']== int(x):
                print "Thin provisioning alert for volume, severity is %s" %x
                endTime = ctime()
                resultCollection(alert['subject'],["PASSED",""],startTime,endTime)

                ### Acknowledge that TP alert for volume
                querycommand='command=acknowledgeAlerts&id=%s' % (alert['id'])
                resp_acknowledgeAlerts=sendrequest(stdurl, querycommand)
                exit()
            else:
                print "Thin provisioning alert severity for volume is not same,severity is %s" %alert['severity']
                exit()

    print "No Thin provisioning alert for volume received "
    endTime = ctime()
    resultCollection("No Thin provisioning alert for volume received",["FAILED",""],startTime,endTime)


#### Finding TP Alert for pool
if  poolFlag == 1:
    alerts=data["listalertsresponse"]["alert"]
    print alerts
    for alert in alerts:
        if "space" in alert['subject'] and alert['description']=="Pool Capacity":
            if alert['severity']== int(x):
                print "Thin provisioning alert for pool, severity is %s" %x
                endTime = ctime()
                resultCollection(alert['subject'],["PASSED",""],startTime,endTime)

                ### Acknowledge that TP alert for pool
                querycommand='command=acknowledgeAlerts&id=%s' % (alert['id'])
                resp_acknowledgeAlerts=sendrequest(stdurl, querycommand)
                exit()
            else:
                print "Thin provisioning alert severity for pool is not same,severity is %s" %alert['severity']
                exit()
    print "No Thin provisioning alert for pool received"
    endTime = ctime()
    resultCollection("No Thin provisioning alert for pool received",["FAILED",""],startTime,endTime)




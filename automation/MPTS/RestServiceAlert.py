import json
import requests
import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd, getoutput, getControllerInfo
if len(sys.argv) < 2:
       print "Argument is not correct.. Correct way as below"
       print "python AckAllAlert.py dedup.txt"
       exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
startTime=ctime()
querycommand = 'command=listAlerts&listAll=true'
resp_listAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAlerts.txt", "w", resp_listAlerts)
data = json.loads(resp_listAlerts.text)
data1 = data['listalertsresponse']
#print data1
if data1=={}:
     print "No Alerts are there"
     endTime=ctime()
     resultCollection("No alerts are displyed in UI may be no alerts generated or all are acknowledged",["FAILED", ' '],startTime, endTime)
     exit()
else:
     print "alerts are present"
     alerts=data['listalertsresponse']['alert']
     success=0
     for alert in alerts:
         type = alert['type']
         time = alert['created']
         if type == 11300114:
             print type
             endTime=ctime()
             print "REST Service up alert is generated at '%s' and visible in UI"%(time)
             success=1
             resultCollection("REST Service UP alert is generated at '\%s'\ and displyed in UI"%(time),["PASSED", ' '],startTime, endTime)
         elif type == 11300113:
             print type
             endTime=ctime()
             print "REST Service down alert is generated at '%s',check the devman" %(time)
             success=1
             resultCollection("REST Service down alert is generated at '\%s'\ and displyed in UI check the devman"%(time),["PASSED", ' '],startTime, endTime)
if success == 0:
    endTime=ctime()
    print"REST service alert is not visible in UI"
    resultCollection("REST Service alert is not generated",["FAILED", ' '],startTime, endTime)

    

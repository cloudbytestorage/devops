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
   print "python AckAllAlert.py dedup.txt "
   exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listAlerts&listAll=true'
resp_listAlerts = sendrequest(stdurl, querycommand)
filesave("logs/ListAlerts.txt", "w", resp_listAlerts)
data = json.loads(resp_listAlerts.text)
#print data

startTime=ctime()
querycommand='command=acknowledgeAlerts&type=all&acknowledgedesc=bulkack'
resp_ackall = sendrequest(stdurl, querycommand)
filesave("logs/ackall.txt", "w",resp_ackall)
response = json.loads(resp_ackall.text)
if 'errortext' in str(response):
   errorstatus = str(response['acknowledgeresponse']['errortext'])
   print errorstatus
   endTime=ctime()
   resultCollection("Alert's BulkAcknoledge  failed'",["FAILED", ' '],startTime, endTime)
   exit()
if 'errortext' not in str(response):
   #time.sleep(5)
   querycommand = 'command=listAlerts&listAll=true'
   resp_listAlerts1 = sendrequest(stdurl, querycommand)
   filesave("logs/ListAlerts1.text", "w", resp_listAlerts1)
   data1 = json.loads(resp_listAlerts1.text)
   data2 = str(data1['listalertsresponse'])
   print data2
   if data2=="{}":
      print "All Alerts are Acknowledged"
      endTime=ctime()
      resultCollection("Alert's BulkAcknoledge done no alerts displyed in UI",["PASSED", ' '],startTime, endTime)
   else: 
       print "After Bulk-Ack still Alerts are there"
       endTime=ctime()
       resultCollection("After BulkAcknoledge of alerts still alerts displyed in UI",["FAILED", ' '],startTime, endTime)


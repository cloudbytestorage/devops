import json
import requests
from hashlib import md5
import fileinput
import subprocess
import sys
import time
from time import ctime
from cbrequest import sendrequest,filesave, filesave1, timetrack, queryAsyncJobResult, resultCollection, configFile, executeCmd, createSFTPConnection, getControllerInfo 
if len(sys.argv) < 3:
 print "Enter in following Format:python PoolDedup.py configfile on/off"
 exit()
dedupvalue = sys.argv[2]
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl, querycommand)
filesave("logs/listHAPool.txt", "w", resp_listHAPool)
data = json.loads(resp_listHAPool.text)
hapools = data ["listHAPoolResponse"]["hapool"]
for hapool in hapools:
     pool_id = hapool['id']
     pool_name = hapool['name']
     for x in range(1, int(config['Number_of_Pools'])+1):
       if pool_name == "%s" %(config['poolName%d' %(x)]):
           id = pool_id
           querycommand='command=updateHAPool&id=%s&deduplication=%s&' %(id,dedupvalue)
           startTime=ctime()
           resp_updateHAPool = sendrequest(stdurl, querycommand)
           filesave("logs/updateHAPool.txt", "w", resp_updateHAPool)
           data = json.loads(resp_updateHAPool.text)
           if "errortext" in data['updateHAPoolResponse']:
               print "\nError : "+data['updateHAPoolResponse']['errortext'];
               endTime=ctime() 
               resultCollection( "Failed to update deduplication as \"%s\" on pool \"%s\""%(dedupvalue,pool_name),["FAILED", ''],startTime,endTime)
           else:
               print "deduplication for %s updated" %(pool_name)
               endTime=ctime()
               resultCollection( "PASS to update deduplication as \"%s\" on  pool \"%s\""%(dedupvalue,pool_name),["PASSED",''],startTime,endTime)
       

import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
print "VDev Creation Begins"

verifyFromDev = 0 ; verifyFromNode = 0;
###To List the Current Number of Sites
for x in range(1, int(config['Number_of_Pools'])+1):
     ### To ListController  and get Diskids
     querycommand = 'command=listHAPool'
     resp_listController = sendrequest(stdurl, querycommand)
     filesave("logs/listPool.txt", "w", resp_listController)
     data = json.loads(resp_listController.text)
     pools = data["listHAPoolResponse"]["hapool"]
     for pool in pools:
         if pool['name'] == "%s" %(config['poolName%d' %(x)]):
             verifyFromDev = 1;
             break;
NPool={}
with open('poolDetails.txt') as pd:
        NPool = json.loads(pd.read());
        print pd.read()




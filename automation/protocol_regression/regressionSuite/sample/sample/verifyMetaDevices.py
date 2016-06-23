import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection
config = configFile(sys.argv)

if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print "python verifyMetaDevices.py config.txt PoolName "
    exit()
poolName = sys.argv[2]
print poolName

noOfMetaDisks1 = 0; noOfMetaDisks2 = 0;
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
######## To Make A Pool Begins
###Stage 1 to 3 , first 2 commands are for listing
with open('poolDetails.txt') as pd:
     NPool = json.loads(pd.read());

verifyPoolFromDev = 0 ; verifyPoolFromNode = 0;
verifyMetaFromDev = 0 ; verifyMetaFromNode = 0;
verifyFromNode = 0; verifyFromDev = 0;
###To List the Current Number of Sites
for x in range(1, int(config['Number_of_Pools'])+1):
    startTime = ctime()
    ### To ListController  and get Diskids
    querycommand = 'command=listHAPool'
    resp_listController = sendrequest(stdurl, querycommand)
    filesave("logs/listPool.txt", "w", resp_listController)
    data = json.loads(resp_listController.text)
    pools = data["listHAPoolResponse"]["hapool"]
    for pool in pools:
        #if pool['name'] == "%s" %(config['poolName%d' %(x)]):
        if pool['name'] == "%s" %(poolName):
            poolName = pool['name']
            verifyFromDev = 1;
            if pool['name'] == "%s" %(NPool['pool']):
                verifyFromNode = 1;
                break;

if verifyFromDev == 1 and verifyFromNode == 1:
    endTime = ctime()
    resultCollection("verification of creation of Pool : %s in DevMan and Node " %(poolName), ["PASSED",""],startTime,endTime);
else:
    endTime = ctime()
    resultCollection("verification of creation of Pool : %s in DevMan and Node " %(poolName), ["FAILED",""],startTime,endTime);

for x in range(1, int(config['Number_of_Pools'])+1):
    startTime = ctime()
      ### To ListController  and get Diskids
      querycommand = 'command=listHAPool'
      resp_listController = sendrequest(stdurl, querycommand)
      filesave("logs/listPool.txt", "w", resp_listController)
      data = json.loads(resp_listController.text)
      pools = data["listHAPoolResponse"]["hapool"]
      for pool in pools:
          for group in pool['grouplist']:
            if group['type'].split()[0] == 'meta':
                noOfMetaDisks1 = len(group) - 4 + noOfMetaDisks1;
          for y in range(1, int(config['Number_of_VDevs'])+1):
              if config['DiskPoolName%d' %(y)] == pool['name']:
                  if config['DiskGroupType%d' %(y)].split('%')[0] == 'meta':
                      noOfMetaDisks2 = int(config['NumOfDisksAllocated%d' %(y)]) + noOfMetaDisks2;
          if noOfMetaDisks1 == noOfMetaDisks2:
              verifyMetaFromDev = 1;
          noOfMetaDisks3 = NPool['noOfMetaDisks'];
          if noOfMetaDisks2 == int(noOfMetaDisks3):
              verifyMetaFromNode = 1;
          if verifyMetaFromNode == 1 and verifyMetaFromDev == 1:
              endTime = ctime()
              resultCollection("verification of creation Meta Devices for %s in DevMan and Node " %(poolName), ["PASSED",""],startTime,endTime);
          else:
              endTime = ctime()
              resultCollection("verification of creation Meta Devices for %s in DevMan and Node " %(poolName), ["FAILED",""],startTime,endTime);

import json
import sys
import md5
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);

stdurl = 'https://%s/client/api?response=%s&' %(config['host'], config['response'])


for x in range(1, int(config['Number_of_HAAdmins'])+1):
    startTime = ctime()
    querycommand = 'command=listHACluster&apikey=%s' %(config['haAdminApikey%d' %(x)])
    resp_listCluster = sendrequest(stdurl,querycommand)
    filesave("logs/listCluster.txt", "w" , resp_listCluster)
    data = json.loads(resp_listCluster.text)
    for y in range (1, int(config['noOfHAAssociated%d' %(x)])+1):
        if "%s" %(config['haAssociatedName%d%d' %(y,x)]) in  str(data):
            success1 = 1 
        else:
            success1 = 0 
            break
        if "%s" %(config['haNotAssociatedName%d' %(x)]) not in  str(data):
            success2 = 1
        else:
            success2 = 0
            break
    
    if ((success1 == 1) and (success2 == 1)):
        print "PASS"
        endTime = ctime()
        resultCollection("HA Admin  %s Access Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "FAIL"
        endTime = ctime()
        resultCollection("HA Admin  %s Access Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["FAILED", ""],startTime,endTime) 



















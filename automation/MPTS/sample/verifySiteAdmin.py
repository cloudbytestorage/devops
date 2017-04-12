import json
import sys
import md5
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);

stdurl = 'https://%s/client/api?response=%s&' %(config['host'], config['response'])


for x in range(1, int(config['Number_of_SiteAdmins'])+1):
    startTime = ctime()
    querycommand = 'command=listSite&apikey=%s' %(config['siteAdminApikey%d' %(x)])
    resp_listSite = sendrequest(stdurl,querycommand)
    filesave("logs/listSite.txt", "w" , resp_listSite)
    data = json.loads(resp_listSite.text)
    for y in range (1, int(config['noOfSitesAssociated%d' %(x)])+1):
        if "%s" %(config['siteAssociatedName%d%d' %(y,x)]) in  str(data):
            success1 = 1 
        else:
            success1 = 0 
            break
        if "%s" %(config['siteNotAssociatedName%d' %(x)]) not in  str(data):
            success2 = 1
        else:
            success2 = 0
            break
    
    if ((success1 == 1) and (success2 == 1)):
        print "PASS"
        endTime = ctime()
        resultCollection("Site Admin  %s Access Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "FAIL"
        endTime = ctime()
        resultCollection("Site Admin  %s Access Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["FAILED", ""],startTime,endTime) 



















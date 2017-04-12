import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

#########To Add the Sites
print "Site Creation Begins"
timetrack("Site Creation Begins")
for x in range(1, int(config['Number_of_Sites'])+1):
    startTime = ctime()
    querycommand = 'command=createSite&location=%s&name=%s&description=%s' %(config['siteLocation%d' %(x)], config['siteName%d'%(x)], config['siteDescription%d' %(x)])
    resp_createSite = sendrequest(stdurl, querycommand)
    filesave("logs/AddSiteList.txt", "w", resp_createSite)
    data = json.loads(resp_createSite.text)
    if "errortext" in data["createSiteResponse"]:
        print "Error in deleting the %s "  %(config['siteName%d' %(x)])
        endTime = ctime()
        resultCollection("Site %s Creation" %(config['siteName%d' %(x)]),["FAILED", "%s" %(data["createSiteResponse"]["errortext"])],startTime,endTime)
    else:
        print "Added the Site %s" %(config['siteName%d' %(x)])
        endTime = ctime()
        resultCollection("Site %s Creation" %(config['siteName%d' %(x)]),["PASSED", "" ],startTime,endTime)
    print "Site %d Creation Begins" %(x)
#timetrack("Site Creation Done")
print "Site Creation Done" 


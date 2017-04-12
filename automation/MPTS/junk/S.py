import json
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configfilefun
import sys

config = configfilefun(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

#########To Add the Sites
print "Site Creation Begins"
timetrack("Site Creation Begins")
for x in range(1, int(config['Number_of_Sites'])+1):
    querycommand = 'command=createSite&location=%s&name=%s&description=%s' %(config['siteLocation%d' %(x)], config['siteName%d'%(x)], config['siteDescription%d' %(x)])
    resp_createSite = sendrequest(stdurl, querycommand)
    filesave("logs/AddSiteList.txt", "w", resp_createSite)
    print "Site %d Creation Begins" %(x)
timetrack("Site Creation Done")
print "Site Creation Done" 


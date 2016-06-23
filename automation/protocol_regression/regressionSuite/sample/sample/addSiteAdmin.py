import json
import sys
import md5
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])



for x in range(1, int(config['Number_of_SiteAdmins'])+1):
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentSitesList.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    sites = data["listSiteResponse"]["site"]
    sites_list_id = ""
    for site in sites:
        for y in range (1, int(config['noOfSitesAssociated%d' %(x)])+1):
            if "%s" %(config['siteAssociatedName%d%d' %(y,x)]) ==  site['name']:
                sites_list_id += "siteslist="
                sites_list_id += site['id']
                sites_list_id += "&"
    print sites_list_id


    ###To create a site-admin
    m = md5.new()
    m.update("%s" %(config['siteAdminPassword%d' %(x)]))
    siteAdminPassword =  m.hexdigest()

    #querycommand = 'command=createDelegatedAdmin&username=%s&password=%s&accounttype=2&account=site-admin' %(config['siteAdminUsername%d' %(x)],config['siteAdminPassword%d' %(x)])
    querycommand = 'command=createDelegatedAdmin&username=%s&password=%s&accounttype=2&account=site-admin' %(config['siteAdminUsername%d' %(x)], siteAdminPassword)
    resp_createdelegatedadmin = sendrequest(stdurl,querycommand)
    filesave("logs/createdelegatedadmin.txt", "w" , resp_createdelegatedadmin)
    data = json.loads(resp_createdelegatedadmin.text)
    #print data
    #pprint.pprint(data)
    # resp_data =  data["createdelegatedadminresponse"]["delegatedadmin"]
    # print resp_data
    print "creating site-admin"

    if not "errortext" in str(data):
        print "Create Site Admin successfully"
        user_id = data["createdelegatedadminresponse"]["delegatedadmin"]["userid"]
    else:
        print "Create Site Admin Failed "
        errorstatus= str(data['createdelegatedadminresponse']['errortext'])
        resultCollection("Site Admin %s Creation Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["FAILED", errorstatus]) 
        continue

    ###To update Delegated Admin

    querycommand = 'command=updateDelegatedAdmin&accounttype=2&%s&userid=%s' %(sites_list_id, user_id )
    resp_updateDelegatedAdmin = sendrequest(stdurl,querycommand)
    filesave("logs/updateDelegatedAdmin.txt", "w" , resp_updateDelegatedAdmin)
    data = json.loads(resp_updateDelegatedAdmin.text)

    if not "errortext" in str(data):
        print "Create Site Admin successfully"
        resultCollection("Site Admin %s Creation Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["PASSED", ""]) 
    else:
        print "Create Site Admin Failed "
        errorstatus= str(data['updateDelegatedAdminResponse']['errortext'])
        resultCollection("Site Admin %s Creation Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["FAILED", errorstatus]) 


















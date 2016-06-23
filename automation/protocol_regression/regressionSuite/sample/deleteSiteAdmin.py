import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])



for x in range(1, int(config['Number_of_SiteAdmins'])+1):
    startTime = ctime()
    querycommand = 'command=listUsers'
    resp_listUsers = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentUsersList.txt", "w", resp_listUsers)
    data = json.loads(resp_listUsers.text)
    users = data["listusersresponse"]["user"]
    user_id = ""
    for user in users:
        if "%s" %(config['siteAdminUsername%d' %(x)]) ==  user['account']:
            user_id = user['accountid']
            print user['account']
            print user_id


    ###To create a site-admin

    querycommand = 'command=deleteDelegatedAdmin&id=%s' %(user_id)
    resp_createdelegatedadmin = sendrequest(stdurl,querycommand)
    filesave("logs/createdelegatedadmin.txt", "w" , resp_createdelegatedadmin)
    data = json.loads(resp_createdelegatedadmin.text)
    #print data
    #pprint.pprint(data)
    # resp_data =  data["createdelegatedadminresponse"]["delegatedadmin"]
    # print resp_data
    print "Deleting SiteAdmin %s" %(config['siteAdminUsername%d' %(x)])

    if not "errortext" in str(data):
        print "Delete Site Admin successfully"
        #user_id = data["deleteaccountcreatedelegatedadminresponse"]["delegatedadmin"]["userid"]
    else:
        print "Delete Site Admin Failed "
        errorstatus= str(data['deleteaccountresponse']['errortext'])
        endTime = ctime()
        resultCollection("Site Admin %s Deletion Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 
        continue

    ###To update Delegated Admin

    querycommand = 'command=updateDelegatedAdmin&userid=%s&unsassign=true' %( user_id )
    resp_updateDelegatedAdmin = sendrequest(stdurl,querycommand)
    filesave("logs/updateDelegatedAdmin.txt", "w" , resp_updateDelegatedAdmin)
    data = json.loads(resp_updateDelegatedAdmin.text)

    if "errortext" in str(data):
        print "Delete Site Admin successfully"
        endTime = ctime()
        resultCollection("Site Admin %s Deletion Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "Delete Site Admin Failed "
        errorstatus= str(data['updateDelegatedAdminResponse']['errortext'])
        endTime = ctime()
        resultCollection("Site Admin %s Deletion Verification from Devman" %(config['siteAdminUsername%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 


















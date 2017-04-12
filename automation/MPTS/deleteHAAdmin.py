import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])



for x in range(1, int(config['Number_of_HAAdmins'])+1):
    startTime = ctime()
    querycommand = 'command=listUsers'
    resp_listUsers = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentUsersList.txt", "w", resp_listUsers)
    data = json.loads(resp_listUsers.text)
    users = data["listusersresponse"]["user"]
    user_id = ""
    for user in users:
        if "%s" %(config['haAdminUsername%d' %(x)]) ==  user['account']:
            user_id = user['accountid']
            print user['account']
            print user_id


    ###To create a HA Admin

    querycommand = 'command=deleteDelegatedAdmin&id=%s' %(user_id)
    resp_createdelegatedadmin = sendrequest(stdurl,querycommand)
    filesave("logs/createdelegatedadmin.txt", "w" , resp_createdelegatedadmin)
    data = json.loads(resp_createdelegatedadmin.text)
    #print data
    #pprint.pprint(data)
    # resp_data =  data["createdelegatedadminresponse"]["delegatedadmin"]
    # print resp_data
    print "Deleting HAAdmin %s" %(config['haAdminUsername%d' %(x)])

    if not "errortext" in str(data):
        print "Delete HA Admin successfully"
        #user_id = data["deleteaccountcreatedelegatedadminresponse"]["delegatedadmin"]["userid"]
    else:
        print "Delete HA Admin Failed "
        errorstatus= str(data['deleteaccountresponse']['errortext'])
        endTime = ctime()
        resultCollection("HA Admin %s Deletion Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 
        continue

    ###To update Delegated Admin

    querycommand = 'command=updateDelegatedAdmin&userid=%s&unsassign=true' %( user_id )
    resp_updateDelegatedAdmin = sendrequest(stdurl,querycommand)
    filesave("logs/updateDelegatedAdmin.txt", "w" , resp_updateDelegatedAdmin)
    data = json.loads(resp_updateDelegatedAdmin.text)

    if "errortext" in str(data):
        print "Delete HA Admin successfully"
        endTime = ctime()
        resultCollection("HA Admin %s Deletion Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "Delete HA Admin Failed "
        errorstatus= str(data['updateDelegatedAdminResponse']['errortext'])
        endTime = ctime()
        resultCollection("HA Admin %s Deletion Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 


















import json
import requests
import md5
import fileinput
import sys
import time
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, configFileName

config = configFile(sys.argv);
configfilename = configFileName(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#######Generate Apikeys for Site Admin

for x in range(1, int(config['Number_of_SiteAdmins'])+1):
    ### List Users
    querycommand = 'command=listUsers'
    resp_listUsers = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentUsersList.txt", "w", resp_listUsers)
    data = json.loads(resp_listUsers.text)
    users = data["listusersresponse"]["user"]
    user_id = ""
    for user in users:
        if "%s" %(config['siteAdminUsername%d' %(x)]) ==  user['account']:
            user_id = user['id']
            print user['account']
            print user_id

    m = md5.new()
    m.update("%s" %(config['siteAdminPassword%d' %(x)]))
    md5_site_pwd =  m.hexdigest()


    ### Generate ApiKey
    querystring = 'command=registerUserKeys&id=%s' %(user_id)
    resp_registerUserKeys = sendrequest(stdurl, querystring)
    filesave("logs/registerUserkeys.txt", "w", resp_registerUserKeys)
    data = json.loads(resp_registerUserKeys.text)
    #print data
    try:
        apikey = data["registeruserkeysresponse"]["userkeys"]["apikey"]
        print "Current Apikey from Devman --- "+apikey
    except:
        print "Didnt get Apikey"
        continue
    existingApikey = "%s" %(config['siteAdminApikey%d' %(x)])
    print "Existing API Key in Config File --- "+existingApikey
    print "ConfigFilename %s" %(configfilename) 
    for line in fileinput.FileInput('%s' %(configfilename),inplace=1):
        line = line.replace(existingApikey,apikey)
        print line,
    fileinput.close()
    print "End of loop1"

#############Apikey Generated for Site Admin

#config = configFile(sys.argv);
#configfilename = configFileName(sys.argv);
#stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#######Generate Apikeys for HA Admin

for x in range(1, int(config['Number_of_HAAdmins'])+1):
    ### List Users
    querycommand = 'command=listUsers'
    resp_listUsers = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentUsersList.txt", "w", resp_listUsers)
    data = json.loads(resp_listUsers.text)
    users = data["listusersresponse"]["user"]
    user_id = ""
    for user in users:
        if "%s" %(config['haAdminUsername%d' %(x)]) ==  user['account']:
            user_id = user['id']
            print user['account']
            print user_id

    m = md5.new()
    m.update("%s" %(config['haAdminPassword%d' %(x)]))
    md5_ha_pwd =  m.hexdigest()


    ### Generate ApiKey
    querystring = 'command=registerUserKeys&id=%s' %(user_id)
    resp_registerUserKeys = sendrequest(stdurl, querystring)
    filesave("logs/registerUserkeys.txt", "w", resp_registerUserKeys)
    data = json.loads(resp_registerUserKeys.text)
    #print data
    try:
        hapikey = data["registeruserkeysresponse"]["userkeys"]["apikey"]
        print "Current Apikey from Devman --- "+hapikey
    except:
        print "Didnt get Apikey"
        continue

    hexistingApikey = "%s" %(config['haAdminApikey%d' %(x)])
    print "Existing API Key in Config File --- "+hexistingApikey
    print "ConfigFilename for HA %s" %(configfilename) 
    for line in fileinput.FileInput('%s' %(configfilename),inplace=1):
        line = line.replace(hexistingApikey,hapikey)
        print line,
    fileinput.close()
    print "End of loop1"
#############Apikey Generated

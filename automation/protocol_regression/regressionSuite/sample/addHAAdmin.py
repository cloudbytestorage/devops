import json
import sys
import md5
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])



for x in range(1, int(config['Number_of_HAAdmins'])+1):
    startTime = ctime()
    
    ### List HAClusters
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentHAList.txt", "w", resp_listHACluster)
    data = json.loads(resp_listHACluster.text)
    clusters = data["listHAClusterResponse"]["hacluster"]
    clusters_list_id = ""
    for cluster in clusters:
        for y in range (1, int(config['noOfHAAssociated%d' %(x)])+1):
            if "%s" %(config['haAssociatedName%d%d' %(y,x)]) ==  cluster['name']:
                clusters_list_id+= "clusterslist="
                clusters_list_id+= cluster['id']
                clusters_list_id+= "&"
                print cluster['name']
                print cluster['id']
    print clusters_list_id


    ### List HAClusters
    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['haAccountName%d' %(x)]):
            account_id = account['id']
            break



    ###To create a HA Admin
    m = md5.new()
    m.update("%s" %(config['haAdminPassword%d' %(x)]))
    md5HAAdminPassword =  m.hexdigest()

    querycommand = 'command=createDelegatedAdmin&username=%s&password=%s&accounttype=4&account=HAGroup-Admin' %(config['haAdminUsername%d' %(x)], md5HAAdminPassword)
    resp_createdelegatedadmin = sendrequest(stdurl,querycommand)
    filesave("logs/createdelegatedadmin.txt", "w" , resp_createdelegatedadmin)
    data = json.loads(resp_createdelegatedadmin.text)
    #print data
    #pprint.pprint(data)
    # resp_data =  data["createdelegatedadminresponse"]["delegatedadmin"]
    # print resp_data
    print "creating HA Admin"

    if not "errortext" in str(data):
        print "Create HA Admin successfully"
        user_id = data["createdelegatedadminresponse"]["delegatedadmin"]["userid"]
    else:
        print "Create HA Admin Failed "
        errorstatus= str(data['createdelegatedadminresponse']['errortext'])
        resultCollection("HA Admin %s Creation Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["FAILED", errorstatus]) 
        continue

    ###To update Delegated Admin

    querycommand = 'command=updateDelegatedAdmin&accounttype=2&%s&userid=%s&accountid=%s' %(clusters_list_id, user_id, account_id)
    resp_updateDelegatedAdmin = sendrequest(stdurl,querycommand)
    filesave("logs/updateDelegatedAdmin.txt", "w" , resp_updateDelegatedAdmin)
    data = json.loads(resp_updateDelegatedAdmin.text)

    if not "errortext" in str(data):
        print "Create HA Admin successfully"
        resultCollection("HA Admin %s Creation Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["PASSED", ""],startTime,endTime) 
    else:
        print "Create HA Admin Failed "
        errorstatus= str(data['updateDelegatedAdminResponse']['errortext'])
        resultCollection("HA Admin %s Creation Verification from Devman" %(config['haAdminUsername%d' %(x)]), ["FAILED", errorstatus],startTime,endTime) 


















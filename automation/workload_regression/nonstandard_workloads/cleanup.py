import json
import md5
import requests
import time
from cbrequest import configFile, sendrequest, filesave, get_apikey, get_url
from utils import assign_iniator_gp_to_LUN
conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
stdurl = get_url(conf, APIKEY)

#########Delete File Systems
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"].get("filesystem")
if filesystems == None:
    print 'There are no volumes'
else:
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        acct_id = filesystem.get('accountid')
        init_grp = filesystem.get('initiatorgroup')
        if init_grp == 'ALL':
            assign_iniator_gp_to_LUN(stdurl, filesystem_id, acct_id, 'None')
        querycommand = 'command=deleteFileSystem&id=%s&forcedelete=true' %(filesystem_id)
        print querycommand
        resp_delete_volume = sendrequest(stdurl, querycommand)
        time.sleep(2)
        filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
        print "Deleted the Volume", filesystem_name

##########Delete TSMs
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/listTSM.txt", "w", resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data["listTsmResponse"].get("listTsm")
if tsms == None:
    print 'There are no tsms'
else:
    for tsm in tsms:
        tsm_id = tsm['id']
        tsm_name = tsm['name']
        querycommand = 'command=deleteTsm&id=%s&forcedelete=true' %(tsm_id)
        resp_delete_tsm = sendrequest(stdurl, querycommand)
        time.sleep(2)
        filesave("logs/Deletetsm", "w", resp_delete_tsm)
        print "Deleted the TSM", tsm_name

##########Delete HAPool
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl, querycommand)
filesave("logs/listHAPool.txt", "w", resp_listHAPool)
data = json.loads(resp_listHAPool.text)
hapools = data["listHAPoolResponse"].get("hapool")
if hapools == None:
    print 'There are no pools'
else:
    for hapool in hapools:
        hapool_id = hapool['id']
        hapool_name = hapool['name']
        querycommand = 'command=deleteHAPool&id=%s&forcedelete=true' %(hapool_id)
        resp_delete_hapool = sendrequest(stdurl, querycommand)
        time.sleep(2)
        filesave("logs/DeleteHAPool", "w", resp_delete_hapool)
        print "Deleted the HAPool", hapool_name

'''
##########Delete Accounts
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/listAccount.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)
accounts = data["listAccountResponse"]["account"]
for account in accounts:
    account_id = account['id']
    account_name = account['name']
    account_user_id = account['acusers'][0]['id']
    #querycommand = 'command=deleteAccount&id=%s&forcedelete=true' %(account_id)
    #print account_id
    #print account_user_id
    ### Delete AccountUser
    querycommand = 'command=deleteAccountUser&id=%s' %(account_user_id)
    resp_delete_accountuser = sendrequest(stdurl, querycommand)
    time.sleep(2)
    filesave("logs/Deleteaccountuser", "w", resp_delete_accountuser)
    ### Delete Account
    querycommand = 'command=deleteAccount&id=%s' %(account_id)
    resp_delete_account = sendrequest(stdurl, querycommand)
    time.sleep(2)
    filesave("logs/Deleteaccount", "w", resp_delete_account)
    print "Deleted the account", account_name

##########Delete Node
querycommand = 'command=listController'
resp_listController = sendrequest(stdurl, querycommand)
filesave("logs/listController.txt", "w", resp_listController)
data = json.loads(resp_listController.text)
controllers = data["listControllerResponse"]["controller"]
for controller in controllers:
    controller_id = controller['id']
    controller_name = controller['name']
    ### Change the state of Controller to Maintenance 
    querycommand = 'command=changeControllerState&id=%s&state=Maintenance' %(controller_id)
    resp_maintenance_controller = sendrequest(stdurl, querycommand)
    filesave("logs/ControllerMaintenance", "w", resp_maintenance_controller)
    time.sleep(60)
    querycommand = 'command=deleteController&id=%s' %(controller_id)
    resp_delete_controller = sendrequest(stdurl, querycommand)
    time.sleep(60)
    filesave("logs/DeleteController", "w", resp_delete_controller)
    print "Deleted the controller", controller_name

##########Delete HACluster
querycommand = 'command=listHACluster'
resp_listHACluster = sendrequest(stdurl, querycommand)
filesave("logs/listHACluster.txt", "w", resp_listHACluster)
data = json.loads(resp_listHACluster.text)
haclusters = data["listHAClusterResponse"]["hacluster"]
for hacluster in haclusters:
    hacluster_id = hacluster['id']
    hacluster_name = hacluster['name']
    querycommand = 'command=deleteHACluster&id=%s' %(hacluster_id)
    resp_delete_hacluster = sendrequest(stdurl, querycommand)
    filesave("logs/DeleteHACluster", "w", resp_delete_hacluster)
    print "Deleted the HACluster", hacluster_name

##########Delete Site
querycommand = 'command=listSite'
resp_listSite = sendrequest(stdurl, querycommand)
filesave("logs/listSite.txt", "w", resp_listSite)
data = json.loads(resp_listSite.text)
sites = data["listSiteResponse"]["site"]
for site in sites:
    site_id = site['id']
    site_name = site['name']
    querycommand = 'command=deleteSite&id=%s' %(site_id)
    resp_delete_site = sendrequest(stdurl, querycommand)
    time.sleep(2)
    filesave("logs/DeleteSite", "w", resp_delete_site)
    print "Deleted the Site", site_name

### Change Admin Password to password
querycommand = 'command=listUsers'
resp_listUsers = sendrequest(stdurl, querycommand)
filesave("logs/listUsers.txt", "w", resp_listUsers)
data = json.loads(resp_listUsers.text)
users = data["listusersresponse"]["user"]
for user in users:
    if user['username'] == "admin":
        user_id = user['id']

m = md5.new()
m.update("password")
md5_set_pwd =  m.hexdigest()

### Update User ID
querycommand = 'command=updateUser&id=%s&password=%s' %(user_id, md5_set_pwd)
resp_updateUser = sendrequest(stdurl, querycommand) 
filesave("logs/updateUsers.txt", "w", resp_updateUser)

print "Updated the Admin Password to -- password"
'''

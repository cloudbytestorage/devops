import json
import requests
import time

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;
 
def resultCollection(testcase,value):
    f=open("results/regression_result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value)
    f.write("\n")
    return;


#### Function(s) Declartion Ends

config = {}
with open('regression_config.txt') as cfg:
  config = json.load(cfg)

print "*********Warning*********"
print "This Script will delete All the Volumes, TSMs and Account from the configuration regression_config.txt"
print "Devman IP %s" %(config['host'])
print "*********Warning*********"
#msg = 'Press y to Continue or Any other key to exit? \n'
#if (raw_input("%s (y/N) " % msg).lower() == 'y'):
#    print "Script for deleting starts"
#else:
#    exit()

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])

#########Delete File Systems
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
            #querycommand = 'command=deleteFileSystem&id=%s&forcedelete=true' %(filesystem_id)
            querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
            #print querycommand
            resp_delete_volume = sendrequest(stdurl, querycommand)
            time.sleep(10)
            filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
            print "Deleted the Volume", filesystem_name

for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
            #querycommand = 'command=deleteFileSystem&id=%s&forcedelete=true' %(filesystem_id)
            querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
            #print querycommand
            resp_delete_volume = sendrequest(stdurl, querycommand)
            time.sleep(10)
            filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
            print "Deleted the Volume", filesystem_name

for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
            #querycommand = 'command=deleteFileSystem&id=%s&forcedelete=true' %(filesystem_id)
            querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
            #print querycommand
            resp_delete_volume = sendrequest(stdurl, querycommand)
            time.sleep(10)
            filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
            print "Deleted the Volume", filesystem_name



##########Delete TSMs
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/listTSM.txt", "w", resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data["listTsmResponse"]["listTsm"]
for x in range(1, int(config['Number_of_TSMs'])+1):
    for tsm in tsms:
        tsm_id = tsm['id']
        tsm_name = tsm['name']
        if tsm_name == "%s" %(config['tsmName%d' %(x)]):
            #querycommand = 'command=deleteTsm&id=%s&forcedelete=true' %(tsm_id)
            querycommand = 'command=deleteTsm&id=%s' %(tsm_id)
            #print querycommand
            resp_delete_volume = sendrequest(stdurl, querycommand)
            time.sleep(10)
            filesave("logs/Deletetsm", "w", resp_delete_volume)
            print "Deleted the TSM", tsm_name

########### Check whether TSM and Volumes are really deleted Begins


#### Check TSMs
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/listTSM.txt", "w", resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data["listTsmResponse"]["listTsm"]
for x in range(1, int(config['Number_of_TSMs'])+1):
    failedToDel=0
    for tsm in tsms:
        tsm_id = tsm['id']
        tsm_name = tsm['name']
        if tsm_name == "%s" %(config['tsmName%d' %(x)]):
            print "The TSM", tsm_name, "Not Deleted", "Failed"
            resultCollection("Deletion of TSM %s" %(tsm_name), "FAILED")
            failedToDel=1
            break
    if failedToDel == 0:
        resultCollection("Deletion of TSM %s" %(config['tsmName%d' %(x)]), "PASSED")
            

#### Check Volumes
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    failedToDel=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
            print "The NFS Volume", filesystem_name , "Not Deleted"
            resultCollection("Deletion of NFS Volume %s" %(filesystem_name), "FAILED")
            failedToDel=1
            break
    if failedToDel == 0:
        resultCollection("Deletion of NFS Volume %s" %(config['volDatasetname%d' %(x)]), "PASSED")


for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    failedToDel=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
            print "The ISCSI Volume", filesystem_name, "Not Deleted"
            resultCollection("Deletion of ISCSI Volume %s" %(filesystem_name), "FAILED")
            failedToDel=1
            break
    if failedToDel == 0:
            resultCollection("Deletion of ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), "PASSED")

for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    failedToDel=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
            print "The CIFS Volume", filesystem_name, "Not Deleted"
            resultCollection("Deletion of CIFS Volume %s" %(filesystem_name), "FAILED")
            failedToDel=1
            break
    if failedToDel == 0:
        resultCollection("Deletion of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), "PASSED")


########### Check whether TSM and Volumes are really deleted Done



exit()
'''
##########Delete Accounts
querycommand = 'command=listAccount2'
resp_listAccount2 = sendrequest(stdurl, querycommand)
filesave("logs/listAccount2.txt", "w", resp_listAccount2)
data = json.loads(resp_listAccount2.text)
accounts = data["listAccountResponse"]["account"]
for account in accounts:
    account_id = account['id']
    account_name = account['name']
    querycommand = 'command=deleteAccount2&id=%s&forcedelete=true' %(account_id)
    print querycommand
    resp_delete_volume = sendrequest(stdurl, querycommand)
    time.sleep(2)
    filesave("logs/Deleteaccount", "w", resp_delete_volume)
    print "Deleted the account", account_name
'''




import json
import requests
import md5
import fileinput
import subprocess
import time
import datetime

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    #print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;

def timetrack(event):
    f=open("results/config_creation_result.csv","a")
    f.write(event)
    f.write("--")
    time = datetime.datetime.now()
    f.write(str(time))
    f.write("\n")
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
with open('config.txt') as cfg:
  config = json.load(cfg)

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
       

#### Check Volumes
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]
'''
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    createdSuccessfully=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
            print "The NFS Volume", filesystem_name , "Created"
            resultCollection("Creation of NFS Volume %s" %(config['volDatasetname%d' %(x)]), "PASSED")
            createdSuccessfully=1
            break
    if createdSuccessfully == 0:
        resultCollection("Creation of NFS Volume %s" %(config['volDatasetname%d' %(x)]), "FAILED")

'''
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    createdSuccessfully=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
            print "The ISCSI Volume", filesystem_name, "Created"
            resultCollection("Creation of ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), "PASSED")
            createdSuccessfully=1
            #print filesystem_id
            querycommand = 'command=listVolumeiSCSIService&storageid=%s' %(filesystem_id)
            resp_listVolumeiSCSIService = sendrequest(stdurl, querycommand)
            filesave("logs/listVolumeiSCSIService.txt", "w", resp_listVolumeiSCSIService)
            data1 = json.loads(resp_listVolumeiSCSIService.text)
            #print data1
            iscsi_service_id = data1["listVolumeiSCSIServiceResponse"]["iSCSIService"][0]["id"]
            #print iscsi_service_id
            querycommand = 'command=updateVolumeiSCSIService&status=true&igid=1allcloudbyte234a&initialdigest=Auto&queuedepth=32&id=%s' %(iscsi_service_id)
            resp_updateVolumeiSCSIService = sendrequest(stdurl, querycommand)
            filesave("logs/updateVolumeiSCSIService.txt", "w", resp_updateVolumeiSCSIService)
            break
    if createdSuccessfully == 0:
        resultCollection("Creation of ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), "FAILED")
'''
for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
    createdSuccessfully=0
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
            print "The CIFS Volume", filesystem_name, "Created"
            resultCollection("Creation of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), "PASSED")
            createdSuccessfully=1
            break
    if createdSuccessfully == 0:
        resultCollection("Creation of CIFS Volume %s" %(config['volCifsDatasetname%d' %(x)]), "FAILED")
'''

########### Check whether TSM and Volumes are really created Done



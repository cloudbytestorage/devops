import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
       
if len(sys.argv) < 2:
    print "Argument is not correct.. Correct way as below"
    print " python setISCSIauthGroup.py config.txt AuthGrpname"
    exit()

###AuthGroup name
if len(sys.argv)==3:
   AG = sys.argv[2]
else:
   AG = "None"

#### Set the iSCSI AuthGroup 
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
            querycommand = 'command=listVolumeiSCSIService&storageid=%s' %(filesystem_id)
            resp_listVolumeiSCSIService = sendrequest(stdurl, querycommand)
            filesave("logs/listVolumeiSCSIService.txt", "w", resp_listVolumeiSCSIService)
            data1 = json.loads(resp_listVolumeiSCSIService.text)
            iscsi_service_id = data1["listVolumeiSCSIServiceResponse"]["iSCSIService"][0]["id"]
	    #ag_id = data1["listVolumeiSCSIServiceResponse"]["iSCSIService"][0]["ag_id"]
            #print "agid"
            #print ag_id
            print "serviceid"
            print iscsi_service_id

            querycommand = 'command=listAccount'
            resp_listAccount = sendrequest(stdurl, querycommand)
            filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
            data = json.loads(resp_listAccount.text)
            accounts = data["listAccountResponse"]["account"]
            for account in accounts:
                if account['name'] == "%s" %(config['voliSCSIAccountName%d' %(x)]):
                    account_id = account['id']
                    break
            
            querycommand = 'command=listiSCSIInitiator&accountid=%s' %(account_id)
            resp_listiSCSIInitiator = sendrequest(stdurl, querycommand)
            filesave("logs/listiSCSIInitiator.txt", "w", resp_listiSCSIInitiator)
            data = json.loads(resp_listiSCSIInitiator.text)
            initiators = data["listInitiatorsResponse"]["initiator"]
            print initiators
            for initiator in initiators:
                print initiator
                if initiator['name'] == "ALL":
                    initiator_id = initiator['id']
                    print "initiator id"
                    print initiator_id
                    break
            querycommand = 'command=listiSCSIAuthGroup&accountid=%s' %(account_id)
            resp_listiSCSIAuthGroup = sendrequest(stdurl, querycommand)
            filesave("logs/listiSCSIAuthGroup.txt", "w", resp_listiSCSIAuthGroup)
            data = json.loads(resp_listiSCSIAuthGroup.text)
            AuthGroups = data["listiSCSIAuthGroupResponse"]["authgroup"]
            print AuthGroups
            for AuthGroup in AuthGroups:
               print AuthGroup
               if AuthGroup['name'] == AG:
                   ag_id = AuthGroup['id']
                   print "AuthGroupid"
                   print ag_id
                   break

            querycommand = 'command=updateVolumeiSCSIService&status=true&authmethod=None&authgroupid=%s&igid=%s&initialdigest=Auto&queuedepth=32&id=%s' %(ag_id, initiator_id, iscsi_service_id)
            resp_updateVolumeiSCSIService = sendrequest(stdurl, querycommand)
            filesave("logs/updateVolumeiSCSIService.txt", "w", resp_updateVolumeiSCSIService)
            break
########### Check whether TSM and Volumes are really created Done



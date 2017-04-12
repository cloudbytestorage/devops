import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
       
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python setISCSIInitiatorGroup.py config.txt number_of_clones clone_name_prefix Initiator_group(optional)"
    exit()

###initiator name
if len(sys.argv) == 5:
   init = sys.argv[4]
else:
   init = "ALL"

prefixName = sys.argv[3]
No_of_Clones = sys.argv[2]

#### Set the iSCSI Initiator 
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    for i in range(1, int(No_of_Clones)+1):
        for filesystem in filesystems:
            filesystem_id = None
            cloneName = prefixName + '%s' %(config['voliSCSIDatasetname%d' %(x)]) + '%d' %(i)
            if filesystem['name'] == cloneName:
                filesystem_id = filesystem['id']
                filesystem_name = filesystem['name']
                if filesystem_id:
                    querycommand = 'command=listVolumeiSCSIService&storageid=%s' %(filesystem_id)
                    resp_listVolumeiSCSIService = sendrequest(stdurl, querycommand)
                    filesave("logs/listVolumeiSCSIService.txt", "w", resp_listVolumeiSCSIService)
                    data1 = json.loads(resp_listVolumeiSCSIService.text)
                    iscsi_service_id = data1["listVolumeiSCSIServiceResponse"]["iSCSIService"][0]["id"]
                    ag_id = data1["listVolumeiSCSIServiceResponse"]["iSCSIService"][0]["ag_id"]
                    print "agid"
                    print ag_id
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
                        if initiator['name'] == init:
                            initiator_id = initiator['id']
                            print "initiator id"
                            print initiator_id
                            break

                    querycommand = 'command=updateVolumeiSCSIService&status=true&authmethod=None&authgroupid=%s&igid=%s&initialdigest=Auto&queuedepth=32&id=%s' %(ag_id, initiator_id, iscsi_service_id)
                    resp_updateVolumeiSCSIService = sendrequest(stdurl, querycommand)
                    filesave("logs/updateVolumeiSCSIService.txt", "w", resp_updateVolumeiSCSIService)
                    break
########### Check whether TSM and Volumes are really created Done



import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])


for x in range(1, int(config['Number_of_fcVolumes'])+1):
     querycommand = 'command=listAccount'
     resp_listAccount = sendrequest(stdurl, querycommand)
     filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
     data = json.loads(resp_listAccount.text)
     accounts = data["listAccountResponse"]["account"]
     for account in accounts:
         if account['name'] == "%s" %(config['volfcAccountName%d' %(x)]):
             account_id = account['id']
             break
     #### List FC initiator
     querycommand ='command=listFCInitiator&accountid=%s' %(account_id )
     fc_init  = sendrequest(stdurl, querycommand)
     filesave("logs/listfcinit.txt", "w", fc_init)
     data = json.loads(fc_init.text)
     inits = data["listFCInitiatorsResponse"]["initiator"]
     for init in inits:
         if init['name'] == "%s" %(config['volfcInitName%d' %(x)]):
            init_id = init['id']
            break
     #### List Volume and take perticular lunid
     querycommand = 'command=listFileSystem'
     resp_listFileSystem = sendrequest(stdurl, querycommand)
     filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
     data = json.loads(resp_listFileSystem.text)
     filesystems = data["listFilesystemResponse"]["filesystem"]
     for filesystem in filesystems:
         filesystem_name1 = filesystem['name']
         filesystem_name2 = "%s" %(config['volfcDatasetname%d' %(x)])
         filesystem_id = filesystem['id']
         if filesystem_name1 == filesystem_name2:
             break ;
     querycommand = 'command=assignFcLuntoGroup&accountid=%s&lunid=%s&fcinitiatorid=%s' %(account_id,filesystem_id,init_id)
     #querycommand= 'command=updateVolumeFCService&fcinitiatorid=%s&id=%s&fctargetgroupid=%s' %(init_id,fc_id,target_id);
     print "%s is  assigned to %s" %(filesystem_name2,config['volfcInitName%d' %(x)])
     resp_updateVolumeFCService  = sendrequest(stdurl, querycommand)
     filesave("logs/resp_updateVolumeFCService", "w",resp_updateVolumeFCService)


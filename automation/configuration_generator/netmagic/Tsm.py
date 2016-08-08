import sys
import time
from time import ctime
import json
import requests
from cbrequest import configFile, executeCmd, resultCollection, sendrequest, filesave, configFileName

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_
config = configFile(sys.argv);

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
######## To Make A TSM Begins here

print "TSM Creation Begins"
for x in range(1, int(config['Number_of_TSMs'])+1):
#for x in range (1, NoofTSMs+1): 
    ###Stage 1 to 8 ... Prior to that 2 commands are for listing.

    #querycommand = 'command=createAccount&name=%s&description=%s' %(config['tsmName%d' %(x)], config['tsmDescription%d' %(x)])
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    print data["listHAPoolResponse"].keys()
    print 'Mardan'
    print data
    hapools = data["listHAPoolResponse"]["hapool"]

    for hapool in hapools:
        if hapool['name'] == "%s" %(config['tsmPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
        #print "Poolid =" ,pool_id


    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['tsmAccountName%d' %(x)]):
            account_id = account['id']
            break
            #print "Accountid =", account_id


    ###Stage1 Command addTSM
    querycommand = 'command=addTsm&accountid=%s&poolid=%s&name=%s&ipaddress=%s&subnet=%s&router=%s&dnsname=%s&dnsserver=%s&tntinterface=%s&gracecontrol=%s&graceallowed=%s&blocksize=%s&latency=%s&iopscontrol=%s&totaliops=%s&tpcontrol=%s&totalthroughput=%s&backuptpcontrol=%s&totalbackupthroughput=%s&iqnname=%s&quotasize=%s' %(account_id, pool_id, config['tsmName%d' %(x)], config['tsmIPAddress%d' %(x)], config['tsmSubnet%d' %(x)], config['tsmRouter%d' %(x)], config['tsmDNSName%d' %(x)], config['tsmDNSServer%d' %(x)], config['tsmTntInterface%d' %(x)], config['tsmGraceControl%d' %(x)], config['tsmGraceAllowed%d' %(x)], config['tsmBlocksize%d' %(x)], config['tsmLatency%d' %(x)], config['tsmIopsControl%d' %(x)], config['tsmTotalIops%d' %(x)], config['tsmTpControl%d' %(x)], config['tsmTotalThroughput%d' %(x)], config['tsmBackupTpcontrol%d' %(x)], config['tsmTotalBackupThroughput%d' %(x)], config['tsmIqnName%d' %(x)], config['tsmQuotasize%d' %(x)])
    resp_addTsm = sendrequest(stdurl, querycommand)
    filesave("logs/AddTsm.txt", "w", resp_addTsm)
    data = json.loads(resp_addTsm.text)
    print data
    tsm_id=data["addTsmResponse"]["tsm"]["id"]
    controller_id=data["addTsmResponse"]["tsm"]["controllerid"]
    #print "TSM ID=", tsm_id
    #print "Controller_id", controller_id

    ####Stage2 Command addStorage
    querycommand = 'command=addStorage&tsmid=%s&poolid=%s&deduplication=off&compression=off&sync=standard&noofcopies=1&recordsize=4K&quotasize=%s' %(tsm_id, pool_id, config['tsmQuotasize%d' %(x)])
    resp_addStorage = sendrequest(stdurl, querycommand)
    filesave("logs/AddStorage.txt", "w", resp_addStorage)
    data = json.loads(resp_addStorage.text)
    storage_id=data["addStorageResponse"]["storage"]["id"]
    #print "Storage id", storage_id

    ####Stage3 updateControllerCommand tsmid
    querycommand = 'command=updateController&tsmid=%s&type=tsm&id=%s' %(tsm_id, controller_id)
    resp_updateController1 = sendrequest(stdurl, querycommand)
    filesave("logs/updateController1.txt", "w", resp_updateController1)

    ####Stage4 updateControllerCommand Storageid
    querycommand = 'command=updateController&storageid=%s&type=storage&id=%s' %(storage_id, controller_id)
    resp_updateController2 = sendrequest(stdurl, querycommand)
    filesave("logs/updateController2.txt", "w", resp_updateController2)

    ####Stage5 addTsmiSCSIService
    querycommand = 'command=addTsmiSCSIService&tsmid=%s' %(tsm_id)
    resp_addTsmiSCSIService = sendrequest(stdurl, querycommand)
    filesave("logs/resp_addTsmiSCSIService.txt", "w", resp_addTsmiSCSIService)
    data = json.loads(resp_addTsmiSCSIService.text)
    iscsi_id = data["tsmiSCSIserviceresponse"]["tiscsioptions"]["id"]
    #print "iSCSIID=",iscsi_id

    ####Stage6 updateController
    querycommand = 'command=updateController&iscsiid=%s&type=configuretsmiscsi&id=%s' %(iscsi_id, controller_id)
    resp_updateControlleriSCSI = sendrequest(stdurl, querycommand)
    filesave("logs/resp_updateControlleriSCSI.txt", "w", resp_updateControlleriSCSI)

    ####Stage7 addTSMCIFSService
    querycommand = 'command=addTsmCifsService&tsmid=%s&netbiosname=%s&authentication=user&workgroup=workgroup&doscharset=CP437&unixcharset=UTF-8&loglevel=Minimum&timeserver=false' %(tsm_id, config['tsmName%d' %(x)])
    resp_addTSMCIFSService = sendrequest(stdurl, querycommand)
    filesave("logs/resp_addTsmiSCSIService.txt", "w", resp_addTSMCIFSService)
    data = json.loads(resp_addTSMCIFSService.text)
    cifs_id = data["tsmCifsserviceResponse"]["cifsService"]["id"]
    #print "Cifs id", cifs_id

    ####Stage8 updateController
    querycommand = 'command=updateController&tcifsid=%s&type=configuretsmcifs&id=%s' %(cifs_id, controller_id)
    resp_updateControllerCIFS = sendrequest(stdurl, querycommand)
    filesave("logs/resp_updateControllerCIFS", "w", resp_updateControllerCIFS)
    print "TSM %d created" %(x)

print "TSM Creation Done"
##### TSM Creation ends here


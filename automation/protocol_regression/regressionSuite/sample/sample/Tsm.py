import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
######## To Make A TSM Begins here

print "TSM Creation Begins"
for x in range(1, int(config['Number_of_TSMs'])+1):
    startTime = ctime()
#for x in range (1, NoofTSMs+1): 
    ###Stage 1 to 8 ... Prior to that 2 commands are for listing.

    #querycommand = 'command=createAccount&name=%s&description=%s' %(config['tsmName%d' %(x)], config['tsmDescription%d' %(x)])
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
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

    #Stage1 Command addTSM
    querycommand = 'command=createTsm&accountid=%s&poolid=%s&name=%s&ipaddress=%s&subnet=%s&router=%s&dnsname=%s&dnsserver=%s&tntinterface=%s&gracecontrol=%s&graceallowed=%s&blocksize=%s&latency=%s&iopscontrol=%s&totaliops=%s&tpcontrol=%s&totalthroughput=%s&backuptpcontrol=%s&totalbackupthroughput=%s&quotasize=%s' %(account_id, pool_id, config['tsmName%d' %(x)], config['tsmIPAddress%d' %(x)], config['tsmSubnet%d' %(x)], config['tsmRouter%d' %(x)], config['tsmDNSName%d' %(x)], config['tsmDNSServer%d' %(x)], config['tsmTntInterface%d' %(x)], config['tsmGraceControl%d' %(x)], config['tsmGraceAllowed%d' %(x)], config['tsmBlocksize%d' %(x)], config['tsmLatency%d' %(x)], config['tsmIopsControl%d' %(x)], config['tsmTotalIops%d' %(x)], config['tsmTpControl%d' %(x)], config['tsmTotalThroughput%d' %(x)], config['tsmBackupTpcontrol%d' %(x)], config['tsmTotalBackupThroughput%d' %(x)],  config['tsmQuotasize%d' %(x)])
    resp_addTsm = sendrequest(stdurl, querycommand)
    filesave("logs/AddTsm.txt", "w", resp_addTsm)
    data = json.loads(resp_addTsm.text)
    job_id = data["addTsmResponse"]["jobid"]
    #queryAsyncJobResult(stdurl, job_id);
    rstatus=queryAsyncJobResult(stdurl, job_id);
    print rstatus
    endTime = ctime()
    resultCollection("TSM %s Creation" %(config['tsmName%d' %(x)]), rstatus,startTime,endTime) 

    print "\nTSM %d Created\n" %(x);
   
print "TSM Creation Done"
##### TSM Creation ends here

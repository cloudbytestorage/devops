import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])


wwpn_list= ""

for x in range(1, int(config['Number_Of_FC_Initiator_group'])+1):
    for y in range(1,  int(config['fcNoOfWWPN%d' %(x)])+1):           ### separating WWPN's with ',' -> replacing it with %2C as encoding in URL
            wwpn_list+= config['fcWWPN%d%d' % (y,x)]
            wwpn_list+="%2C"
    print wwpn_list    
    

    ### listing the Accounts
    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['fcAccountName%d' %(x)]):
            account_id = account['id']
            break


    ## Add Fc initiator group
    
    querycommand = 'command=addFCInitiator&accountid=%s&wwpn=%s&name=%s' %(account_id ,wwpn_list,config['fcInitName%d' %(x)])
    resp_Add_FC_Initiator = sendrequest(stdurl, querycommand)
    filesave("logs/AddFCInitiator.txt", "w", resp_listAccount)

    data = json.loads(resp_Add_FC_Initiator.text)
    print data
    

    ## Collecting  the result/logs
    if not "errortext" in str(data):
        print "FC Initiator added successfully"
        resultCollection("Fc Initiator Addition %s Verification from Devman" %(config['fcInitName%d' %(x)]), ["PASSED", ""])
    else:
        print "FC Initiator addition Failed "
        errorstatus= str(data['tsmFCInitiatorResponse']['errortext'])
        resultCollection("FC Initiator  Addition %s Verification from Devman" %(config['fcInitName%d' %(x)]), ["FAILED", errorstatus])

    
    
    
    



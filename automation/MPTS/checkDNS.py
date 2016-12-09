import json
import sys
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, queryAsyncJobResultNegative


config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

def all_same(items):
    return all(x == "127.0.0.1" for x in items)

querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/listTsm.txt", "w",resp_listTsm)
data = json.loads(resp_listTsm.text)
tsms = data['listTsmResponse']['listTsm']

dnslist = list();
startTime = ctime()
for x in range(1, int(config['Number_of_TSMs'])+1):
    for tsm in tsms:
        tsm_name = tsm['name'];
        tsm_id = tsm['id'];
        acc_id = tsm['accountid'];
        if tsm_name == "%s"%config["tsmName%d" %(x)]:
            querycommand = 'command=listTsmDNSSettings&tsmid=%s'%(tsm_id)
            resp_TsmDnsSettings = sendrequest(stdurl, querycommand)
            filesave("logs/resp_TsmDnsSettings.txt","w",resp_TsmDnsSettings)
            data = json.loads(resp_TsmDnsSettings.text)
            print data
            primaryDns = data['listTsmDnsSettingsResponse']['dnssettings'][0]['dns1']
            print primaryDns
            dnslist.append(primaryDns)
        
endTime = ctime()
flag = all_same(dnslist)
print flag
if flag:
    resultCollection("TSM default dns ip address is 127.0.0.1",["PASSED",""], startTime, endTime)
else:
    resultCollection("TSM default dns ip address 127.0.0.1",["FAILED",""], startTime, endTime)



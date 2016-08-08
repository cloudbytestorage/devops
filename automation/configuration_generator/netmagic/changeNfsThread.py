import json
import sys
import fileinput
import string
from time import ctime
from cbrequest import configFile, executeCmd, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 3:
    print bcolors.WARNING + "python changeNfsThread.py snapshot.txt Number_of_Threads" + bcolors.ENDC
    exit()
config = configFile(sys.argv);
No_of_threads = sys.argv[2]

print No_of_threads
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
filesave("logs/ListTsm.txt", "w", resp_listTsm)
dataTsm = json.loads(resp_listTsm.text)
tsms = dataTsm['listTsmResponse']['listTsm']
for x in range(1, int(config['Number_of_TSMs'])+1):
    startTime = ctime()
    for listTsm in tsms:
        tsmid = None
        if listTsm['name'] == "%s" %(config['tsmName%d' %(x)]):
            tsmid = listTsm['id']
            print tsmid
            if tsmid is not None:
                querycommand = 'command=updateTsmNfsOptions&nfsworkerthreads=%s&tsmid=%s' %(No_of_threads, tsmid)
                change_NFSThread_resp = sendrequest(stdurl, querycommand)
                filesave("logs/changeNFSThreads.txt", "w", change_NFSThread_resp)
                changeThreadResp = json.loads(change_NFSThread_resp.text)
                if 'errortext' in str(changeThreadResp):
                    errorstatus = str((changeThreadResp)['updateTsmNfsOptionsResponse']['errortext'])
                    endTime = ctime()
                    resultCollection("Failed to change nfs threads", ['FAILED', errorstatus], startTime, endTime)
                else:
                    endTime = ctime()
                    resultCollection("Successfully changed NFS threads to %s" %(No_of_threads), ['PASSED', ''], startTime, endTime)
            else:
                endTime = ctime()
                resultCollection("not able to get TSM_ID", ['FAILED', ''], startTime, endTime)




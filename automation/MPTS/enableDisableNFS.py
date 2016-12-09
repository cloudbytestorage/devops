import json
import sys
import fileinput
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend


###
# Provide configuration file true/false and IP address of controller as parameter
###
    

config = configFile(sys.argv);
#configfilename = configFileName(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = createSnp = deleteSnp = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 3:
    print bcolors.FAIL + "Arguments are not correct. Please provide as follows..." + bcolors.ENDC
    print bcolors.WARNING + "python enableDisableNFS.py config.txt true/false" + bcolors.ENDC
    exit()

nfsenabled = sys.argv[2].lower()

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

### NFS
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    startTime = ctime()
    for filesystem in filesystems:
        filesystem_id = None
        if filesystem['name'] == "%s" %(config['volDatasetname%d' %(x)]):
            filesystem_id = filesystem['id']
            filesystem_name = filesystem['name']
            if filesystem_id is not None:
                querycommand = 'command=updateFileSystem&id=%s&nfsenabled=%s' %(filesystem_id, nfsenabled)
                respListSnapshot = sendrequest(stdurl, querycommand)
                filesave("logs/ListSnapshot.txt", "w",respListSnapshot)
                data2 = json.loads(respListSnapshot.text)
                if not "errorcode" in str(data2['updatefilesystemresponse']):
                    endTime = ctime()
                    resultCollection("Result for NFS Status \"%s\" on volume %s is: " %(nfsenabled, filesystem_name), ["PASSED", ""], startTime, endTime)
                else:
                    endTime = ctime()
                    errorstatus = str(data2['updatefilesystemresponse']['errortext'])
                    resultCollection("Result for NFS Status \"%s\" on volume %s is: " %(nfsenabled, filesystem_name), ["FAILED", "errorstatus"], startTime, endTime)

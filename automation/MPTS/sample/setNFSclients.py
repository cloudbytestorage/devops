import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#querycommand = 'command=%s' %(config['command'])
       

#### Check Volumes
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
            querycommand = 'command=nfsService&datasetid=%s&authnetwork=All&managedstate=true&alldirs=Yes&mapuserstoroot=Yes&readonly=No&response=json' %filesystem_id
            set_NFSServiceToAll = sendrequest(stdurl, querycommand) 
            filesave("logs/set_NFSServiceToAll.txt", "w",set_NFSServiceToAll)
            data1 = json.loads(set_NFSServiceToAll.text);
            if "errortext" in str(data1):
                print "Already set "
                continue
            nfs_id = data1["nfsserviceprotocolresponse"]["nfs"]["id"]
            ctrl_id = data1["nfsserviceprotocolresponse"]["nfs"]["controllerid"];
            querycommand = 'command=updateController&nfsid=%s&type=configurenfs&id=%s&response=json' %(nfs_id,ctrl_id)
            UpadateNFSServiceToAll = sendrequest(stdurl, querycommand);
            filesave("logs/UpadateNFSServiceToAll.txt", "w",UpadateNFSServiceToAll)
            print "NFS Service is Set to All for %s" %(filesystem_name)

########### Check whether TSM and Volumes are really created Done



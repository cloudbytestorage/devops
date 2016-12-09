import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python updateVolumeIOPS.py config.txt NFS 0"
    print "python updateVolumeIOPS.py config.txt ISCSI 1000"
    print "python updateVolumeIOPS.py config.txt ALL 100"
    print "python updateVolumeIOPS.py config.txt NFS ISCSI 0 -- Not Allowed"
    exit()

if sys.argv[2].lower() == "%s" %("nfs"):
    nfsFlag = 1;
elif sys.argv[2].lower() == "%s" %("cifs"):
    cifsFlag = 1;
elif sys.argv[2].lower() == "%s" %("fc"):
    fcFlag = 1;
elif sys.argv[2].lower() == "%s" %("iscsi"):
    iscsiFlag = 1;
elif sys.argv[2].lower() == "%s" %("all"):
    allFlag = 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python .updateVolumeIOPSpy config.txt NFS 0"
    print "python updateVolumeIOPS.py config.txt ISCSI 1000"
    print "python updateVolumeIOPS.py config.txt ALL 100"
    print "python updateVolumeIOPS.py config.txt NFS ISCSI 0 -- Not Allowed"
    exit()

volIops = sys.argv[3]
graceAllowed = "false"

if len(sys.argv) == 5: 
    if sys.argv[4] == "true":
        graceAllowed = "true"
    else:
        graceAllowed = "false"

###### To Increase the IOPS
#####List Filesystem
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
    filesystem_id = filesystem['groupid']
    filesystem_name = filesystem['name']
    ###NFS
    if nfsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_NFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateQosGroup&id=%s&iops=%s&graceallowed=%s' %(id, volIops, graceAllowed)
                resp_updateNFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
                print ">>>> NFS >>>>updated %s" %(filesystem_name)
    ###CIFS
    if cifsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateQosGroup&id=%s&iops=%s&graceallowed=%s' %(id, volIops, graceAllowed)
                resp_updateCIFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
                print ">>>> CIFS >>updated %s" %(filesystem_name)


    ###ISCSI
    if iscsiFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateQosGroup&id=%s&iops=%s&graceallowed=%s' %(id, volIops, graceAllowed)
                resp_updateISCSI = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
                print ">>>> ISCSI >> >> updated %s" %(filesystem_name) 

                                                                                   
    ###FC
    if fcFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateQosGroup&id=%s&iops=%s&graceallowed=%s' %(id, volIops, graceAllowed)
                resp_updateFC = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                print ">>>> FC >>>> updated %s" %(filesystem_name)

print "done"







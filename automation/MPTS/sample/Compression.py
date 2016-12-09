import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection
nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0
if len(sys.argv) < 4:
    print "Argument is not correct.. Correct way as below"
    print "python Compression.py config.txt CIFS/NFS/iSCSI/FC/ALL on/off"
    exit()

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
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
    print "python Compression.py config.txt CIFS/NFS/iSCSI/FC/ALL on/off"
    exit()

compvalue = sys.argv[3]

#####List Filesystem
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
    filesystem_id = filesystem['id']
    filesystem_name = filesystem['name']
    ###NFS
    if nfsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_NFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateNFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
                print ">>>> NFS >>>>updated %s" %(filesystem_name)
                '''
                if "errortext" in data['updateqosresponse']:
                  print "\nError : "+data['updateqosresponse']['errortext'];
                  endTime=ctime()
                  resultCollection( "Failed to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volCifsDatasetname%d' %(x)]),["FAILED", ''],startTime,endTime)
                else:
                   print "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volCifsDatasetname%d' %(x)])
                   endTime=ctime()
                   resultCollection( "PASS to update Compression as \"%s\" on Dataset %s" %(compvalue,config['volCifsDatasetname%d' %(x)]),["PASSED",''],startTime,endTime)
                #resultCollection("Readonly value for Volume %s updated as %s" %(config['volCifsDatasetname%d' %(x)],readonlyvalue), ('PASSED', ' '), startTime, endTime)
                '''
    ###CIFS
    if cifsFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
            if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateCIFS = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
                print ">>>> CIFS >>updated %s" %(filesystem_name)


    ###ISCSI
    if iscsiFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateISCSI = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
                print ">>>> ISCSI >> >> updated %s" %(filesystem_name) 

                                                                                   
    ###FC
    if fcFlag == 1 or allFlag == 1:
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                id = filesystem_id
                querycommand='command=updateFileSystem&id=%s&compression=%s' %(id, compvalue)
                resp_updateFC = sendrequest(stdurl, querycommand)
                filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
                print ">>>> FC >>>> updated %s" %(filesystem_name)

print "done"







import json
import sys
import fileinput
import time
from cbrequest import configFile, executeCmd, resultCollection, sendrequest, filesave, configFileName

config = configFile(sys.argv);
configfilename = configFileName(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag = 0

########### TestCase Execution Starts..
if len(sys.argv) < 2:
    print "Argument is not correct.. Correct way as below"
    print "python expandVol.py config.txt nfs/cifs/iscsi quotasize"
    print "python expandVol.py config.txt ALL quotasize"
    print "python expandVol.py config.txt ALL, by default quotasize of 5GB will be extended for each volume"
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
     allFlag == 1;
else:
    print "Argument is not correct.. Correct way as below"
    print "python expandVol.py config.txt nfs/cifs/iscsi quotasize"
    print "python expandVol.py config.txt ALL quotasize"
    print "python expandVol.py config.txt ALL, by default quotasize of 5GB will be extended for each volume"
    exit()


querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data["listFilesystemResponse"]["filesystem"]

####NFS
if nfsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_NFSVolumes'])+1):
        for filesystem in filesystems:
            filesystem_id = filesystem['id']
            filesystem_name = filesystem['name']
            if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
                q1 = config['volQuotasize%d' %(x)]
                print q1[:-1]
                if len(sys.argv) > 3:
                    q2 = sys.argv[3]
                else:
                    q2 = 5
                quota = int(q1[:-1]) + int(q2)
                quota = str(quota) + "G"
                print quota

                querycommand = 'command=updateFileSystem&id=%s&quotasize=%s&readonly=false' % (filesystem_id, quota)
                resp_updateFileSystem  = sendrequest(stdurl, querycommand)
                filesave("logs/updateFileSystem.txt", "w", resp_updateFileSystem)
                data = json.loads(resp_updateFileSystem.text)
                #print data

                ## Collecting  the result/logs
                if not "errortext" in str(data):
                    print "%s volume expanded successfully" %(config['volDatasetname%d' %(x)])
                    resultCollection("%s volume expanded successfully" %(config['volDatasetname%d' %(x)]), ["PASSED", ""])
                else:
                    print "%s volume expansion failed"  %(config['volDatasetname%d' %(x)])
                    errorstatus= str(data['Response']['errortext'])
                    resultCollection("%s volume expansion failed" %(config['volDatasetname%d' %(x)]), ["FAILED", errorstatus])
            
                vol='volQuotasize%d' %(x)
                for line in fileinput.FileInput('%s' %(configfilename), inplace=1):
                    if vol in line:
                        line=line.replace(q1, quota) ### replace config.txt with new quota size for that volume
                    print line,




####ISCSI
if iscsiFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
        for filesystem in filesystems:
            filesystem_id = filesystem['id']
            filesystem_name = filesystem['name']
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                q1 = config['voliSCSIQuotasize%d' %(x)]
                print q1[:-1]
            
                if len(sys.argv) > 2:
                    q2 = sys.argv[2]
                else:
                    q2 = 5

                quota = int(q1[:-1]) + int(q2)
                quota = str(quota) + "G"
                print quota
            
                querycommand = 'command=updateFileSystem&id=%s&quotasize=%s&readonly=false' % (filesystem_id, quota)
                resp_updateFileSystem  = sendrequest(stdurl, querycommand)
                filesave("logs/updateFileSystem.txt", "w", resp_updateFileSystem)
                data = json.loads(resp_updateFileSystem.text)
                #print data
            
                ## Collecting  the result/logs
                if not "errortext" in str(data):
                    print "%s volume expanded successfully" %(config['voliSCSIDatasetname%d' %(x)])
                    resultCollection("%s volume expanded successfully" %(config['voliSCSIDatasetname%d' %(x)]), ["PASSED", ""])
                else:
                    print "%s volume expansion failed"  %(config['voliSCSIDatasetname%d' %(x)])
                    errorstatus= str(data['Response']['errortext'])
                    resultCollection("%s volume expansion failed" %(config['voliSCSIDatasetname%d' %(x)]), ["FAILED", errorstatus])
                        
                vol='voliSCSIQuotasize%d' %(x)
                for line in fileinput.FileInput('%s' %(configfilename), inplace=1):
                    if vol in line:
                        line=line.replace(q1, quota) ### replace config.txt with new quota size for that volume
                    print line,


####CIFS

if cifsFlag == 1 or allFlag == 1:
    for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
        for filesystem in filesystems:
            filesystem_id = filesystem['id']
            filesystem_name = filesystem['name']
            if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                q1 = config['volCifsQuotasize%d' %(x)]
                print q1[:-1]
                if len(sys.argv) > 2:
                    q2 = sys.argv[2]
                else:
                    q2 = 5

                quota = int(q1[:-1]) + int(q2)
                quota = str(quota) + "G"
                print quota

                querycommand = 'command=updateFileSystem&id=%s&quotasize=%s&readonly=false' % (filesystem_id, quota)
                resp_updateFileSystem  = sendrequest(stdurl, querycommand)
                filesave("logs/updateFileSystem.txt", "w", resp_updateFileSystem)
                data = json.loads(resp_updateFileSystem.text)
                #print data

                ## Collecting  the result/logs
                if not "errortext" in str(data):
                    print "%s volume expanded successfully" %(config['volCifsDatasetname%d' %(x)])
                    resultCollection("%s volume expanded successfully" %(config['volCifsDatasetname%d' %(x)]), ["PASSED", ""])
                else:
                    print "%s volume expansion failed"  %(config['volCifsDatasetname%d' %(x)])
                    errorstatus= str(data['Response']['errortext'])
                    resultCollection("%s volume expansion failed" %(config['volCifsDatasetname%d' %(x)]), ["FAILED", errorstatus])
            
                vol='volCifsQuotasize%d' %(x)
                for line in fileinput.FileInput('%s' %(configfilename), inplace=1):
                    if vol in line:
                        line=line.replace(q1, quota) ### replace config.txt with new quota size for that volume
                    print line,





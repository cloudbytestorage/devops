import json
import requests
from hashlib import md5
import fileinput
import subprocess
import sys
import time
from cbrequest import sendrequest,filesave, filesave1, timetrack, queryAsyncJobResult, configFile, executeCmd, createSFTPConnection, getControllerInfo 

config = configFile(sys.argv);

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

#for x in range(1, int(config['Number_of_NFSVolumes'])+1):
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
     filesystem_id = filesystem['id']
     filesystem_name = filesystem['name']
     for x in range(1, int(config['Number_of_NFSVolumes'])+1):
       if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateFileSystem&id=%s&deduplication=on&readonly=false' %(id)
           resp_updateNFS = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
           data = json.loads(resp_updateNFS.text)
           if "errortext" in data['updatefilesystemresponse']:
               print "\nError : "+data['updatefilesystemresponse']["errortext"];
           else:
               print "deduplication for %s enabeled" %(filesystem_name)

#cifs
     for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
       if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateFileSystem&id=%s&deduplication=on&readonly=false' %(id)
           resp_updateCIFS = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
           data = json.loads(resp_updateCIFS.text)
           if "errortext" in data['updatefilesystemresponse']:
               print "\nError : "+data['updatefilesystemresponse']["errortext"];
           else:
               print "deduplication for %s enabeled" %(filesystem_name)
               


#iscsi
     for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
       if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateFileSystem&id=%s&deduplication=on&readonly=false' %(id)
           resp_updateISCSI = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
           data = json.loads(resp_updateISCSI.text)
           if "errortext" in data['updatefilesystemresponse']:
                print "\nError : "+data['updatefilesystemresponse']["errortext"];
           else:
                print "deduplication for %s enabeled" %(filesystem_name)

                                                                                   
  #fc
     for x in range(1, int(config['Number_of_fcVolumes'])+1):
       if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateFileSystem&id=%s&deduplication=on&readonly=false' %(id)
           resp_updateFC = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
           data = json.loads(resp_updateISCSI.text)
           if "errortext" in data['updatefilesystemresponse']:
                print "\nError : "+data['updatefilesystemresponse']["errortext"];
           else:
                print "deduplication for %s enabeled" %(filesystem_name)








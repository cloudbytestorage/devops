import sys
import json
import requests
from cbrequest import configFile

def sendrequest(url, querystring):
    #print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission)
    f.write(content.text)
    f.close()
    return;

#### Function(s) Declartion Ends

'''
config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)
'''
config = configFile(sys.argv)
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
quotasize = sys.argv[2]
#print quotasize
#exit()
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
           id= filesystem_id
           #print "hi"
           querycommand='command=updateFileSystem&id=%s&quotasize=%s&noofcopies=%s&readonly=%s' %(id, config['volQuotasize%d' %(x)],config['volNoofCopies%d' %(x)], config['volReadOnly%d' %(x)])
           resp_updateNFS = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
           print "updated %s" %(filesystem_name)
#cifs
     for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
       if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
          id= filesystem_id
          #print "hi"
          querycommand='command=updateFileSystem&id=%s&quotasize=%s&noofcopies=%s&readonly=%s' %(id, config['volCifsQuotasize%d' %(x)],config['volCifsNoofCopies%d' %(x)], config['volCifsReadOnly%d' %(x)])
          resp_updateCIFS = sendrequest(stdurl, querycommand)
          filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
          print "updated %s" %(filesystem_name)


#iscsi
     for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
         print quotasize
       if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
          id= filesystem_id
          #print "hi"
          querycommand='command=updateFileSystem&id=%s&quotasize=%s&noofcopies=%s' %(id, quotasize, config['voliSCSINoofCopies%d' %(x)])
          resp_updateISCSI = sendrequest(stdurl, querycommand)
          filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
          print "updated %s" %(filesystem_name) 

                                                                                   
  #fc
     for x in range(1, int(config['Number_of_fcVolumes'])+1):
       if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
          id= filesystem_id
           #print "hi"
          querycommand='command=updateFileSystem&id=%s&quotasize=%s&noofcopies=%s&readonly=%s' %(id, config['volfcQuotasize%d' %(x)],config['volfcNoofCopies%d' %(x)], config['volfcReadOnly%d' %(x)])
          resp_updateFC = sendrequest(stdurl, querycommand)
          filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
          print "updated %s" %(filesystem_name)

print "done"







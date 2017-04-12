import json
import requests

def sendrequest(url, querystring):
    # print url+querystring
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


config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

#for x in range(1, int(config['Number_of_NFSVolumes'])+1):
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
filesystems = data ["listFilesystemResponse"]["filesystem"]
for filesystem in filesystems:
     filesystem_id = filesystem['groupid']
     filesystem_name = filesystem['name']
     for x in range(1, int(config['Number_of_NFSVolumes'])+1):
       if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateQosGroup&id=%s&graceallowed=%s' %(id,  config['volGraceallowed%d' %(x)])
           resp_updateNFS = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateNFS.txt", "w", resp_listFileSystem)
           print ">>>> NFS >>>>updated %s" %(filesystem_name)
#cifs
     for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
       if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateQosGroup&id=%s&graceallowed=%s' %(id,  config['volCifsGraceallowed%d' %(x)])
           resp_updateCIFS = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateCIFS.txt", "w", resp_listFileSystem)
           print ">>>> CIFS >>updated %s" %(filesystem_name)


#iscsi
     for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
       if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateQosGroup&id=%s&graceallowed=%s' %(id, config['voliSCSIGraceallowed%d' %(x)])
           resp_updateISCSI = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateISCSI.txt", "w", resp_listFileSystem)
           print ">>>> ISCSI >> >> updated %s" %(filesystem_name) 
         


                                                                                   
  #fc
     for x in range(1, int(config['Number_of_fcVolumes'])+1):
       if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
           id = filesystem_id
           querycommand='command=updateQosGroup&id=%s&graceallowed=%s' %(id, config['volfcGraceallowed%d' %(x)])
           resp_updateFC = sendrequest(stdurl, querycommand)
           filesave("logs/resp_updateFC.txt", "w", resp_listFileSystem)
           print ">>>> FC >>>> updated %s" %(filesystem_name)

print "done"







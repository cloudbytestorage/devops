import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

###listTSM'S 
for x in range(1, int(config['Number_of_TSMs'])+1):
  querycommand = 'command=listTsm'
  resp_listTsm = sendrequest(stdurl, querycommand)
  filesave("logs/listTsm.txt", "w",resp_listTsm)
  data = json.loads(resp_listTsm.text)
  tsms = data['listTsmResponse']['listTsm']
  for tsm in tsms:
      tsm_name1 = tsm['name'];
      tsm_name2 = config["tsmName%d" %(x)];
      tsm_id = tsm['id'];
      Acc_name = tsm['accountname'];
      acc_id = tsm['accountid']
      if tsm_name1==tsm_name2:
          break;
  AUTH_Name1= "%sAUTH" %(Acc_name);
     
  querycommand = 'command=listTsmCifsService&tsmid=%s' %(tsm_id)
  resp_cifsService = sendrequest(stdurl, querycommand)
  filesave("logs/resp_cifsService.txt","w",resp_cifsService)
  data = json.loads(resp_cifsService.text)
  cifsServices = data['listTsmcifsServiceResponse']['cifsService']
  for cifsService in cifsServices:
      cifs_id = cifsService['id'];
      tsm_id2 = cifsService['tsmid']
      if tsm_id == tsm_id2: 
          break;

  ##ListCIFSAuthgroup
  #querycommand = 'command=listCIFSAuthGroup&'
  querycommand = 'command=listCIFSAuthGroup&accountid=%s' %(acc_id)
  resp_listCIFSAuthGroup =sendrequest(stdurl, querycommand)
  filesave("logs/listCIFSAuthGroup.txt","w",resp_listCIFSAuthGroup)
  data = json.loads(resp_listCIFSAuthGroup.text)
  auth_groups = data['listcifsauthgroupresponse']['cifsauthgroup']
  for auth_group in auth_groups :
      auth_name = auth_group['name'];
      auth_id = auth_group['id'];
      if AUTH_Name1 == auth_name:
          break ;
  querycommand = 'command=updateTsmCifsService&&netbiosname=Default&description=&authentication=user&workgroup=workgroup&doscharset=CP437&unixcharset=UTF-8&loglevel=Minimum&timeserver=false&authgroupid=%s&id=%s' %(auth_id,cifs_id)
  resp_updateTsmCifsService = sendrequest(stdurl, querycommand)
  filesave("logs/resp_updateTsmCifsService.txt","w",resp_updateTsmCifsService)
  print "%s is set to %s" %(auth_name,tsm_name1)

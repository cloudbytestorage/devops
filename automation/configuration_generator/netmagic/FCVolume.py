import json
import sys
import time
from time import ctime
import requests
from cbrequest import sendrequest, filesave, configFile

config = configFile(sys.argv)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

######## To Make A FC Volume Begins here

print "FC Volume Creation Begins"
###Stage 1 to 6 , prior to this first 3 commands are for listing.
for x in range(1, int(config['Number_of_fcVolumes'])+1):
#for x in range (1, NooffcVolumes+1):
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentHAPoolList.txt","w",resp_listHAPool) 
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"]["hapool"]
    for hapool in hapools:
        if hapool['name'] == "%s" %(config['volfcPoolName%d' %(x)]):
            pool_id = hapool['id']
            break
 #  print "Poolid = %d" ,pool_id


    querycommand = 'command=listAccount'
    resp_listAccount = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
    data = json.loads(resp_listAccount.text)
    accounts = data["listAccountResponse"]["account"]
    for account in accounts:
        if account['name'] == "%s" %(config['volfcAccountName%d' %(x)]):
            account_id = account['id']
            break
 #  print "Accountid =", account_id


    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/CurrentTsmList.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"]["listTsm"]
    for listTsm in tsms:
        if listTsm['name'] == "%s" %(config['volfcTSMName%d' %(x)]):
            tsm_id = listTsm['id']
	    dataset_id = listTsm['datasetid']
            break
  # print "Tsmid =", tsm_id
  # print "Datasetid =", dataset_id

    ###Stage1 Command addQoSGroup
    querycommand = 'command=addQosGroup&tsmid=%s&name=%s&latency=%s&blocksize=%s&tpcontrol=%s&throughput=%s&iopscontrol=%s&iops=%s&graceallowed=%s&memlimit=%s&networkspeed=%s&datasetname=%s&protocoltype=%s&quotasize=%s&datasetid=%s' %(tsm_id, config['volfcName%d' %(x)], config['volfcLatency%d' %(x)], config['volfcBlocksize%d' %(x)], config['volfcTpcontrol%d' %(x)], config['volfcThroughput%d' %(x)], config['volfcIopscontrol%d' %(x)], config['volfcIops%d' %(x)], config['volfcGraceallowed%d' %(x)], config['volfcMemlimit%d' %(x)], config['volfcNetworkspeed%d' %(x)], config['volfcDatasetname%d' %(x)], config['volfcProtocoltype%d' %(x)], config['volfcQuotasize%d' %(x)], dataset_id) 
    resp_addQosGroup = sendrequest(stdurl, querycommand)
    filesave("logs/AddQosGroup.txt", "w", resp_addQosGroup)
    data = json.loads(resp_addQosGroup.text)
    if not 'errorcode' in data["addqosgroupresponse"]:
        qosgroup_id = data["addqosgroupresponse"]["qosgroup"]["id"]
    else:
        errormsg = data["addqosgroupresponse"]["errortext"]
        print errormsg
        exit()
  # print "QosGroup id=",qosgroup_id
  # print "stage 1 : ",stdurl+querycommand

    ###Stage2 add Volume
    querycommand = 'command=addVolume2&type=%s&accountid=%s&qosgroupid=%s&tsmid=%s&poolid=%s&name=%s&quotasize=%s&datasetid=%s&recordsize=%s&blocklength=%s&deduplication=%s&compression=%s&sync=%s&mountpoint=%s&noofcopies=%s&casesensitivity=%s&readonly=%s&unicode=%s&iscsienabled=%s&fcenabled=%s' %(config['volfcType%d' %(x)], account_id, qosgroup_id, tsm_id, pool_id, config['volfcDatasetname%d' %(x)], config['volfcQuotasize%d' %(x)], dataset_id, config['volfcBlocksize%d' %(x)],config['volfcBlocklength%d' %(x)], config['volfcDeduplication%d' %(x)], config['volfcCompression%d' %(x)],config['volfcSync%d' %(x)], config['volfcMountpoint%d' %(x)], config['volfcNoofCopies%d' %(x)], config['volfcCasesensitivity%d' %(x)], config['volfcReadonly%d' %(x)], config['volfcUnicode%d' %(x)], config['volfcISCSIEnabled%d' %(x)], config['volfcfcEnabled%d' %(x)])
    resp_addVolume2 = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolume.txt", "w", resp_addVolume2)
    data = json.loads(resp_addVolume2.text)
    storage_id=data["addvolumeresponse"]["storage"]["id"]

  # print "stage 2 : ",stdurl+querycommand
  # print "Storage id =",storage_id
	
  

	
    ###Stager3 Update Controller
    querycommand = 'command=updateController&type=qosgroup&qosid=%s&tsmid=%s' %(qosgroup_id, tsm_id)
    resp_updateControllerqosgroup = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController1.txt", "w", resp_updateControllerqosgroup)
   # print "stage 3  : ",stdurl+querycommand

    ###Stager4 Update Controller
    querycommand = 'command=updateController&storageid=%s&type=storage&tsmid=%s' %(storage_id, tsm_id)
    resp_updateControllerstorage = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateController2.txt", "w", resp_updateControllerstorage)

    #print "stage 4 : ",stdurl+querycommand

	  ###Stager5 Add fc Serveice
    querycommand = 'command=addVolumeFcService&datasetid=%s&name=%s&description=default&status=%s&targetport=%s' %(storage_id,config['volfcDatasetname%d' %(x)],config['volfcManagedState%d' %(x)],'all')
    resp_addvVolumefcService = sendrequest(stdurl, querycommand)
    filesave("logs/AddVolumefcService.txt", "w", resp_addvVolumefcService)
    data = json.loads(resp_addvVolumefcService.text)
    fc_id = data["volumeFcserviceResponse"]["fcservice"]["id"]
    fc_targ_grp_id= data["volumeFcserviceResponse"]["fcservice"]["fctargetgroupid"]
    #print "stage 5  : ",stdurl+querycommand
    #print "fc id =", fc_id 
    #print "targ_grp_id ",fc_targ_grp_id

	
    ###Stage6 Update Controller
    querycommand ='command=updateController&fcid=%s&type=%s' %(fc_id,'configurevolumefc')
    resp_updateControllerfc = sendrequest(stdurl, querycommand)
    filesave("logs/UpdateControllerfc.txt", "w", resp_updateControllerfc)
   
    #print "stage 6  : ",stdurl+querycommand
    print "FC Volume %d Created" %(x)
    
    '''
    ###################### Add FC initiators to the FC Volume ##################### 
    #### List FC initiator 
    querycommand ='command=listFCInitiator&accountid=%s' %(account_id )
    fc_init  = sendrequest(stdurl, querycommand)
    filesave("logs/listfcinit.txt", "w", fc_init)
    data = json.loads(fc_init.text)
    inits = data["listFCInitiatorsResponse"]["initiator"]
    for init in inits:
          if init['name'] == "%s" %(config['volfcInitName%d' %(x)]):
              init_id = init['id']
              break
    
   # print "init_id :",init_id

    #### Update Volume FC Service
    
    querycommand ='command=updateVolumeFCService&fcinitiatorid=%s&id=%s&fctargetgroupid=%s' %(init_id,fc_id,fc_targ_grp_id)
    addinit = sendrequest(stdurl, querycommand)
    filesave("logs/addfcinit.txt", "w", addinit)
    '''
print "FC Volume Creation Done" 

######## To Make A fc Volume Ends here






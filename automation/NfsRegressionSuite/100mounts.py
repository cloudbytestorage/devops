import sys
import json
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, configFile, queryAsyncJobResult,\
        resultCollection, queryAsyncJobResultNegative, mountNFS, umountVolume,\
        get_url, get_apikey
from volumeUtils import create_volume, delete_volume, addNFSclient
import logging
from tsmUtils import create_tsm

if len(sys.argv) < 2:
    print 'Incorrect parameters, please specify as follows...'
    print 'python example.py conf.txt '
    exit()

logging.basicConfig(format = '%(asctime)s %(levelname)s: %(message)s', \
        filename = 'logs/automation_execution.log', filemode = 'a', level = logging.DEBUG)

logging.info("---------------execution begins-----------------")
print ("---------------execution begins-----------------")
conf = configFile(sys.argv);
logging.info("getting apiKey")
apikey = get_apikey(conf)
logging.debug("apikey :%s"% apikey)
logging.info("processing stdurl")
stdurl = get_url(conf, apikey[1])
logging.debug("stdUrl :%s"% stdurl)
print stdurl

## getting pool id ##

logging.info("")
def get_poolID(hapools):
    pool_id = None
    for hapool in hapools:
        pool_id = hapool['id']
        break
    return pool_id
logging.info("Listing pool ID to create tsm ")
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl,querycommand)
data = json.loads(resp_listHAPool.text)

try:
    hapools = data["listHAPoolResponse"]["hapool"]
    logging.info("paasing an exeception to catch KeyError while lsiting poolID")
except KeyError:
    print " no POOLs are Available, Minimum 1 POOL required to proceed"
    logging.error('No Pool available please have minimum 1 POOL to proceed %s'%\
        KeyError)
    exit()
pool_id = get_poolID(hapools)

logging.info("Listing pool ID was sucessful")

#print pool_id

###getting account ID to create TSM

def get_accID(accounts):
     account_id = None
     for account in accounts:
         account_id = account['id']
         break
     return account_id
logging.info("Listing Account ID")
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
filesave("logs/CurrentAccountList.txt", "w", resp_listAccount)
data = json.loads(resp_listAccount.text)

try:
    accounts = data["listAccountResponse"]["account"]
    logging.info("paasing an exeception to catch KeyError while lsiting poolID")
except KeyError:
    endTime = ctime()
    print " no Accounts are Available, Minimum 1 Account required to proceed"
    logging.error('No Accounts available please have minimum 1 Account to proceed %s'%\
                                                            KeyError)
    exit()
account_id = get_accID(accounts)
print account_id
logging.info("Listing Account ID was sucessful")
                
## creation of tsm begins  #####
### creating a loop to create 5 tsm's

logging.info("creation of TSM begins")
for x in range(1, 6):
    tsm_params = {'name': 'TTTSM%d' %x, 'accountid': account_id, 'poolid': pool_id, \
        'ipaddress': conf["ipVSM%d" %x], 'quotasize': '1T', 'blocksize': '4k', \
        'latency': 15, 'totaliops': 1000, 'totalthroughput': '', \
        'graceallowed': 'true', 'subnet': 8, 'tntinterface': conf["interfaceVSM%d" %x], \
        'dnsname': 'sdsd@s.c', 'dnsserver': '8.8.8.8', \
        'gracecontrol': 'false', 'iopscontrol': 'true', \
        'tpcontrol': 'true', 'backuptpcontrol': 'false', \
        'totalbackupthroughput': 0}
    tsm_params['totalthroughput'] = tsm_params['totaliops']*4
    
    # calling method to create tsm
    
    logging.info("calling method to create tsm")
    result_tsm = create_tsm(tsm_params, stdurl)
    if result_tsm[0] == 'FAILED':
        print "FAILED TO CREATE VSM "
        logging.error("FAILED TO CREATE VOLUME: %s"% result_tsm)
    elif result_tsm[0] == 'PASSED':
        print "ADDITION OF VSM WAS SUCESSFUL "
        logging.info("Adding TSM was sucessful")
        querycommand = 'command=listTsm'
        logging.debug("passing querycommand to list tsm \n %s"% querycommand)
        resp_listTsm = sendrequest(stdurl, querycommand)
        data = json.loads(resp_listTsm.text)
        logging.info("sucessfully loaded data to list TSM")
        tsms = data["listTsmResponse"]["listTsm"]
        
        # fetcing datasetID and tsmID to create volumes
        
        for tsm in tsms:
            if tsm['name'] == tsm_params['name']: 
                logging.info("fetching Dataset id and TSM id ")               
                dataset_id = tsm['datasetid']
                tsm_id = tsm['id']
                logging.info("sucessfully updated Dataset id and TSM id ")
                for y in range(1, 21):
                    logging.info("processing forloop to create volumes")
                    volume = {'name': '%sNFS%d' %(tsm_params['name'], y), 'tsmid':\
                            tsm_id, 'datasetid': dataset_id,'protocoltype': 'NFS'}
                    
                    # calling method to create volume
                    
                    logging.info("creation of volume begins")                  
                    result_vol = create_volume(volume ,stdurl)
                    if result_vol[0] == 'FAILED':
                       print("Adding NFS client FAILED %s "% result_vol)
                       logging.error("FAILED TO ADD VOLUMES %s "% result_vol)
                       exit()
                    elif result_vol[0] == 'PASSED': 
                       print("Adding NFS client PASSED %s "% result_vol)
                       logging.info("SUCESSFULLY CREATED VOLUMES")
                       
                       #Listing filesystem to add NFS clients to all 
                       
                       querycommand = 'command=listFileSystem&tsmid=%s'% (tsm_id)
                       logging.info(" "% result_vol)
                       resp_listVolume = sendrequest(stdurl, querycommand)
                       data1 = json.loads(resp_listVolume.text)
                       if 'errorcode' in str(data1): 
                           errormsg =  str(data["listFilesystemResponse"]["errortext"])
                           print ("%s"% errormsg)
                           logging.error("Failed to list volumes %s "% errormsg)
                           exit()
                       else:
                           volumes = data1['listFilesystemResponse']['filesystem']
                           logging.info("Listing volumes was sucessful")
                        
                        # getting volid mountpoint and Tsm_ip to set nfs client to all
                        
                           for vol in volumes:
                               if vol['name'] ==  volume['name']:
                                   volId = vol['id']
                                   mount_p = vol['mountpoint']
                                   Tsm_ip = vol['ipaddress']
                                   result_addnfs= addNFSclient(stdurl, volId, 'all')
                                   if result_addnfs[0] == 'FAILED':
                                       print("Adding NFS client was UNsuccessfuil%d")
                                       logging.error("Failed to add NFS clients :  %s "% result_addnfs)
                                       exit()
                                   elif result_addnfs[0] == 'PASSED':
                                      print("Adding NFS client FAILED %s "% result_addnfs)
                                      logging.info("Sucessfully added NFS clients")
                                   
                                   # started mounting NFS volumes
                                    
                                      volume_1 = {'name': volume['name'], 'mountPoint': mount_p, 'TSMIPAddress': Tsm_ip}
                                      result_mount = mountNFS(volume_1)
                                      if result_mount[0] == 'PASSED':
                                          print ("mounting volume was %s"% result_mount)
                                          logging.info("Sucessfully added NFS clients")
                                      elif result_mount[0] == 'FAILED':
                                           print ("mounting volume was %s"% result_mount)
                                           logging.error("FAILED TO MOUNT NFS VOLUMES %s"% result_mount)
                                           exit()
'''                              
                           else: 
                                   print (" no volumes with name %d exists"% volume['name']) 
                                   logging.error("NO VOLUMES FOUND %s")
                                   exit()
                           
                           
                           for z in range(1, 21):
                               logging.info("IN the loop to mount all volumes")
                               volume_umount = {'name': '%sNFS%s' %(tsm_params['name'], volume['name']), 'tsmid':\
                                       tsm_id, 'datasetid': dataset_id,'protocoltype': 'NFS'}
                               
                               # STARTED UNMOUNT NFS VOLUMES
                               
                               logging.info("STARTED UNMOUNT NFS VOLUMES")
                               result_umount = umountVolume(volume_umount)
                               if result_umount[0] == 'FAILED':
                                   print result_umount
                                   logging.error("failed to mount %s"% result_umount)
                                   exit()
                               elif result_umount[0] == 'PASSED':
                                   print result_umount
                                   logging.info("mounted sucssfully")'''


logging.info("---------------execution begins-----------------")
print ("---------------execution begins-----------------")


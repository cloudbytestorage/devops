import sys
import json
from time import ctime
import logging
from cbrequest import sendrequest, configFile,\
        queryAsyncJobResult, resultCollection, queryAsyncJobResultNegative,\
        mountNFS, umountVolume, get_url, get_apikey
from volumeUtils import create_volume, delete_volume, addNFSclient

startTime = ctime()
if len(sys.argv) < 2:
    print 'Incorrect parameters, please specify as follows...\n'
    print 'python CreateMountDeletenfs.py conf.txt '
    exit()

logging.basicConfig(format = '%(asctime)s %(levelname)s: %(message)s', \
        filename = 'logs/automation_execution.log', filemode = 'a',\
        level = logging.DEBUG)
logging.info("---------------Execution of CreateMountDeletenfs.py'\
        ' script begins-----------------")
conf = configFile(sys.argv)
logging.info("getting apiKey")
apikey = get_apikey(conf)
logging.debug("apikey :%s"% apikey)
logging.info("processing stdurl")
stdurl = get_url(conf, apikey[1])
logging.debug("stdUrl :%s"% stdurl)

#Function to Fetch existing TSM_ID & dataset_ID
def get_id(tsms):
    logging.info("calling method to get TSM_ID & dataset_id")
    #dataset_id = None
    #tsm_id = None
    for tsm in tsms:
        dataset_id = tsm['datasetid']
        tsm_id = tsm['id']
        break
    return dataset_id,tsm_id

querycommand = 'command=listTsm'
resp_listTsm = sendrequest(stdurl, querycommand)
data = json.loads(resp_listTsm.text)
logging.debug('listing Tsm_ID and Dataset id %s '% data)

try:
    tsms = data['listTsmResponse']['listTsm']

except KeyError:
    endTime = ctime()
    print " no Tsms are Available, Minimum 1 TSM required to proceed"
    logging.error('No Tsm available please have minimum 1 TSM to proceed %s'%\
            KeyError)    
    exit()
dataset_id,tsm_id = get_id(tsms)

#adding Nfs volume
logging.info("processing creation of volume")
volume = {'name': 'mountvol1', 'tsmid': tsm_id, 'datasetid': dataset_id,\
        'protocoltype': 'NFS'}
result = create_volume(volume, stdurl)
if result[0] ==  'PASSED':
    logging.info("volume creeated sucessfully")
    print 'volume created successfully'
else:
    logging.error("volume creation failed %s"% result)
    print ('volume creation failed %s'% result[1])
    endTime = ctime()
    resultCollection('nfs Volume creation is failed so test case is', \
            ['BLOCKED', ''], startTime, endTime)

## fetching volume id and mountpoint etc
logging.info('fetching volume id and  mountpoint')
querycommand = 'command=listFileSystem&tsmid=%s'% (tsm_id)
resp_listVolume = sendrequest(stdurl, querycommand)
data1 = json.loads(resp_listVolume.text)
if 'errorcode' in str(data1):
    errormsg =  str(data["listFilesystemResponse"]["errortext"])
    logging.error('No volumes available due to', errormsg)
    endTime = ctime()
    resultCollection('No volumes in TSM so test case is', \
                                     ['BLOCKED',''], startTime, endTime)
    exit()
else:  
    volumes = data1['listFilesystemResponse']['filesystem']
    for vol in volumes:
        if vol['name'] == volume['name']:
            volId = vol['id']
            mount_p = vol['mountpoint']
            Tsm_ip = vol['ipaddress'] 
            volName = vol['name']
            logging.info("volume id and  mountpoint sucessfully received")


    ### set nfs client
    logging.info("Setting NFS clients to all")
    result_addnfs= addNFSclient(stdurl, volId, 'all')       
    if result_addnfs[0] == 'PASSED':
        logging.info(" SUCCESSFUL %s "% result_addnfs )
        print("Adding NFS client was successful")

    elif result_addnfs[0] == 'FAILED':
        logging.info(" Failed to add NFS clients %s "% result_addnfs)
        endTime = ctime()
        resultCollection(' Failed to add NFS clients', \
                ['BLOCKED', ''], startTime, endTime)
        print("Adding NFS client FAILED %s "% result_addnfs)

    # mount and umount nfs volumes
    volume = {'name': volume['name'], 'mountPoint': mount_p, 'TSMIPAddress': Tsm_ip}
    logging.info("Mounting Nfs volumes")
    result_mount = mountNFS(volume)
    if result_mount == 'PASSED':
        logging.info("volume mounted sucessfully %s"% result_mount )
    elif result_mount == 'FAILED':
        logging.error("Failed to mount volumes %s so ending the script"% result_mount)
        endTime = ctime()
        resultCollection('Umounting volume test case is', \
                ['BLOCKED', result_mount], startTime, endTime)

    logging.info("Started umounting volumes")
    result_umount = umountVolume(volume)
    print result_umount
    if result_umount == 'PASSED':
        logging.info('volume umounted succesfull')
        endTime = ctime()
        resultCollection('Volume is Unmounted Succesfully is', \
                            ['PASSED', ''], startTime, endTime)
    elif result_umount == 'FAILED':
        logging.error("failed to umount %s "% result_umount)
        endTime = ctime()
        resultCollection('Volume is not unmounted Succesfully', \
                ['FAILED', ''], startTime, endTime)


    ## deleting volumes
    if result_umount == 'PASSED':
        logging.info("volume deletion is in progress")
        result_delete = delete_volume(volId, stdurl)
        if result_delete[0] ==  'PASSED':
            logging.info("volume deleted sucessfully")
            print result_delete
        elif result_delete[0] == 'FAILED':
            print result_delete
            logging.error('Failed to umount volumes %s'%  result_delete)
            endTime = ctime()
            resultCollection('Failed to Delete', \
                    ['BLOCKED', result_mount], startTime, endTime)
    logging.info('---------------Execution of CreateMountDeletenfs.py script'\
            'ENDs-----------------')

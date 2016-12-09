import json
import md5
import sys
import requests
import time
from cbrequest import configFile, sendrequest, filesave, get_apikey, get_url, queryAsyncJobResult
from utils import assign_iniator_gp_to_LUN
conf = configFile(sys.argv)
DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']
APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
stdurl = get_url(conf, APIKEY)

def deleteVolume():
    #########Delete File Systems
    querycommand = 'command=listFileSystem'
    resp_listFileSystem = sendrequest(stdurl, querycommand)
    filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
    data = json.loads(resp_listFileSystem.text)
    filesystems = data["listFilesystemResponse"].get("filesystem")
    if filesystems == None:
        print 'There are no volumes'
    else:
        for filesystem in filesystems:
            filesystem_id = filesystem['id']
            filesystem_name = filesystem['name']
            acct_id = filesystem.get('accountid')
            init_grp = filesystem.get('initiatorgroup')
            if init_grp == 'ALL':
                assign_iniator_gp_to_LUN(stdurl, filesystem_id, acct_id, 'None')
                time.sleep(1)
            querycommand = 'command=deleteFileSystem&id=%s&forcedelete=true' %(filesystem_id)
            resp_delete_volume = sendrequest(stdurl, querycommand)
            data = json.loads(resp_delete_volume.text)
            if 'errorcode' in str(data):
                errormsg = str(data['deleteFileSystemResponse'].get('errortext'))
                print 'Not able to delete volume %s, due to%s' %(filesystem_name, errormsg)
            else:
                deleteJobId = data['deleteFileSystemResponse'].get('jobid')
                delete_volume_status = queryAsyncJobResult(stdurl, deleteJobId)
                if delete_volume_status[0] == 'PASSED':
                    print 'Volume %s deleted successfully' %(filesystem_name)
                else:
                    print 'Not able to delete volume %s' %(filesystem_name)

def deleteVSM():
    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/listTSM.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data["listTsmResponse"].get("listTsm")
    if tsms == None:
        print 'There are no tsms'
    else:
        for tsm in tsms:
            tsm_id = tsm['id']
            tsm_name = tsm['name']
            querycommand = 'command=deleteTsm&id=%s&forcedelete=true' %(tsm_id)
            resp_delete_tsm = sendrequest(stdurl, querycommand)
            data = json.loads(resp_delete_tsm.text)
            if 'errorcode' in str(data):
                errormsg = str(data['deleteTsmResponse']['errortext'])
                print errormsg
            else:
                print "Deleted the TSM", tsm_name
            time.sleep(1)

def deletePool():
    querycommand = 'command=listHAPool'
    resp_listHAPool = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listHAPool.text)
    hapools = data["listHAPoolResponse"].get("hapool")
    if hapools == None:
        print 'There are no pools'
    else:
        for hapool in hapools:
            hapool_id = hapool['id']
            hapool_name = hapool['name']
            querycommand = 'command=deleteHAPool&id=%s&forcedelete=true' %(hapool_id)
            resp_delete_hapool = sendrequest(stdurl, querycommand)
            data = json.loads(resp_delete_hapool.text)
            if 'errorcode' in str(data):
                errormsg = str(data['deleteHAPoolResponse']['errortext'])
                print errormsg
            else:
                print "Deleted the HAPool", hapool_name
            time.sleep(1)

deleteVolume()
time.sleep(2)

deleteVSM()
time.sleep(2)

deletePool()

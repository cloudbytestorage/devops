import json
import sys
import time
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection

config = configFile(sys.argv);

nfsFlag = cifsFlag = iscsiFlag =  fcFlag =  allFlag =  tsmFlag = accFlag = poolFlag = nodeFlag = haFlag = siteFlag = 0 
if len(sys.argv) < 3:
    print "Argument is not correct.. Correct way as below"
    print "python delete.py config.txt NFS"
    print "python delete.py config.txt ALL"
    print "python delete.py config.txt NFS CIFS FC ISCSI TSM ACC POOL JBOD NODE HA SITE"
    exit()
for x in range(2, len(sys.argv)):
    if sys.argv[x].lower() == "%s" %("nfs"):
        nfsFlag = 1;
    elif sys.argv[x].lower() == "%s" %("cifs"): 
        cifsFlag = 1;
    elif sys.argv[x].lower() == "%s" %("fc"): 
        fcFlag = 1;
    elif sys.argv[x].lower() == "%s" %("iscsi"): 
        iscsiFlag = 1;
    elif sys.argv[x].lower() == "%s" %("tsm"): 
        tsmFlag = 1;
    elif sys.argv[x].lower() == "%s" %("all"): 
        allFlag = 1;
    elif sys.argv[x].lower() == "%s" %("acc"):
        accFlag = 1;
    elif sys.argv[x].lower() == "%s" %("pool"):
        poolFlag = 1;
    elif sys.argv[x].lower() == "%s" %("node"):
        nodeFlag = 1;
    elif sys.argv[x].lower() == "%s" %("ha"):
        haFlag = 1;
    elif sys.argv[x].lower() == "%s" %("site"):
        siteFlag = 1;
    else:
        print "Argument is not correct.. Correct way as below"
        print "python delete.py config.txt NFS"
        print "python delete.py config.txt ALL"
        print "python delete.py config.txt NFS CIFS FC ISCSI TSM ACC POOL JBOD NODE HA SITE"
        exit()
        
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
querycommand = 'command=listFileSystem'
resp_listFileSystem = sendrequest(stdurl, querycommand)
filesave("logs/ListFileSystem.txt", "w", resp_listFileSystem)
data = json.loads(resp_listFileSystem.text)
if "filesystem" in data ["listFilesystemResponse"]:
    filesystems = data ["listFilesystemResponse"]["filesystem"]
else:
    filesystems = {}
if nfsFlag == 1 or allFlag ==1:
    print "\nDeleting NFS Volumes ...\n"
    for filesystem in filesystems:
       filesystem_id = filesystem['id']
       filesystem_name = filesystem['name']
       for x in range(1, int(config['Number_of_NFSVolumes'])+1):
           startTime = ctime()
           if filesystem_name == "%s" %(config['volDatasetname%d' %(x)]):
               querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
               resp_delete_volume = sendrequest(stdurl, querycommand)
               filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
               data = json.loads(resp_delete_volume.text)
               job_id = data["deleteFileSystemResponse"]["jobid"]
               #queryAsyncJobResult(stdurl, job_id);
               rstatus=queryAsyncJobResult(stdurl, job_id);
               print rstatus
               endTime = ctime()
               resultCollection("NFS Volume %s Deletion" %(config['volDatasetname%d' %(x)]), rstatus,startTime,endTime) 
               print "\n%s is deleted\n" %(filesystem_name)
    print "All NFS Volumes are Deleted"
    time.sleep(2);

if cifsFlag == 1 or allFlag == 1:
    print "\nDeleting CIFS Volumes ...\n"
    for filesystem in filesystems:
         filesystem_id = filesystem['id']
         filesystem_name = filesystem['name']
         for x in range(1, int(config['Number_of_CIFSVolumes'])+1):
             startTime = ctime()
             if filesystem_name == "%s" %(config['volCifsDatasetname%d' %(x)]):
                 querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                 resp_delete_volume = sendrequest(stdurl, querycommand)
                 filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
                 data = json.loads(resp_delete_volume.text)
                 job_id = data["deleteFileSystemResponse"]["jobid"]
                 #queryAsyncJobResult(stdurl, job_id);
                 rstatus=queryAsyncJobResult(stdurl, job_id);
                 print rstatus
                 endTime = ctime()
                 resultCollection("CIFS Volume %s Deletion" %(config['volCifsDatasetname%d' %(x)]), rstatus,startTime,endTime) 
                 print "\n%s is deleted\n" %(filesystem_name)
    print "All CIFS Volumes are Deleted"
    time.sleep(2);

if iscsiFlag == 1 or allFlag == 1:
    print "\nDeleting ISCSI Volumes ...\n"
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
            startTime = ctime()
            if filesystem_name == "%s" %(config['voliSCSIDatasetname%d' %(x)]):
                querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                resp_delete_volume = sendrequest(stdurl, querycommand)
                filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
                data = json.loads(resp_delete_volume.text)
                job_id = data["deleteFileSystemResponse"]["jobid"]
                #queryAsyncJobResult(stdurl, job_id);
                rstatus=queryAsyncJobResult(stdurl, job_id);
                print rstatus
                endTime = ctime()
                resultCollection("ISCSI Volume %s Deletion" %(config['voliSCSIDatasetname%d' %(x)]), rstatus,startTime,endTime) 
                print "\n%s is deleted\n" %(filesystem_name)
    print "All ISCSI Volumes are Deleted"
    time.sleep(2);

if fcFlag == 1 or allFlag == 1:
    print "\nDeleting FC Volumes ...\n"
    for filesystem in filesystems:
        filesystem_id = filesystem['id']
        filesystem_name = filesystem['name']
        for x in range(1, int(config['Number_of_fcVolumes'])+1):
            startTime = ctime()
            if filesystem_name == "%s" %(config['volfcDatasetname%d' %(x)]):
                querycommand = 'command=deleteFileSystem&id=%s' %(filesystem_id)
                resp_delete_volume = sendrequest(stdurl, querycommand)
                filesave("logs/DeleteFileSystem", "w", resp_delete_volume)
                data = json.loads(resp_delete_volume.text)
                job_id = data["deleteFileSystemResponse"]["jobid"]
                #queryAsyncJobResult(stdurl, job_id);
                rstatus=queryAsyncJobResult(stdurl, job_id);
                print rstatus
                endTime = ctime()
                resultCollection("FC Volume %s Deletion" %(config['volfcDatasetname%d' %(x)]), rstatus,startTime,endTime) 
                print "\n%s is deleted\n" %(filesystem_name)
    print "All FC Volumes are Deleted"
    time.sleep(2);

if tsmFlag == 1 or allFlag == 1:
    print "\nDeleting TSM Buckets ...\n"
    querycommand = 'command=listTsm'
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave("logs/listTSM.txt", "w", resp_listTsm)
    data = json.loads(resp_listTsm.text)
    if "listTsm" in data["listTsmResponse"]:
        tsms = data["listTsmResponse"]["listTsm"];
    else:
        print "There are no Tsm's";
        tsms = {}
    for tsm in tsms:
        tsm_id = tsm['id']
        tsm_name = tsm['name']
        for x in range(1, int(config['Number_of_TSMs'])+1):
            startTime = ctime()
            if tsm_name == "%s" %(config['tsmName%d' %(x)]):
                #querycommand = 'command=deleteTsm&id=%s&forcedelete=true' %(tsm_id)
                querycommand = 'command=deleteTsm&id=%s' %(tsm_id)
                resp_delete_tsm = sendrequest(stdurl, querycommand)
                data = json.loads(resp_delete_tsm.text)
                if "errortext" in data["deleteTsmResponse"]:
                    print "Error : "+data["deleteTsmResponse"]["errortext"];
                    endTime = ctime()
                    resultCollection("TSM %s Deletion" %(config['tsmName%d' %(x)]),["FAILED", "%s" %(data["deleteTsmResponse"]["errortext"])],startTime,endTime)
                else:
                    print "%s deleted" %(config['tsmName%d' %(x)])
                    endTime = ctime()
                    resultCollection("TSM %s Deletion" %(config['tsmName%d' %(x)]),["PASSED", ""],startTime,endTime)
                time.sleep(5);
                filesave("logs/Deletetsm", "w", resp_delete_tsm)
                print "Deleted the TSM", tsm_name
    print "\nDeleted TSM Buckets"
    time.sleep(2);

if accFlag == 1 or allFlag == 1:
    print "\nDeleting ACCOUNTS ...\n"
    querycommand = 'command=listAccount';
    resp_listAcc = sendrequest(stdurl, querycommand)
    filesave("logs/listAcc.txt", "w", resp_listAcc)
    data = json.loads(resp_listAcc.text);
    if "account" in data["listAccountResponse"]:
        accounts = data["listAccountResponse"]["account"];
    else:
        print "There are no Accounts"
        accounts = {}
    for account in accounts:
        acc_id = account["id"];
        acc_name = account["name"]
        for x in range(1, int(config['Number_of_Accounts'])+1):
            startTime = ctime()
            if acc_name == "%s" %(config['accountName%d' %(x)]):
                querycommand = "command=listCIFSAuthGroup&accountid=%s" %(acc_id);
                resp_listCifsAuth=sendrequest(stdurl, querycommand)
                filesave("logs/listCifsAuth.txt", "w", resp_listCifsAuth);
                data = json.loads(resp_listCifsAuth.text);
                cifs_auths = data["listcifsauthgroupresponse"]["cifsauthgroup"]
                confirm = ""
                for auth in cifs_auths:
                    auth_id = auth["id"];
                    auth_name = auth["name"];
                    if auth_name == "None":
                        continue;
                    querycommand = "command=deleteCIFSAuthGroup&id=%s&accountid=%s" %(auth_id,acc_id);
                    resp_deleteCifsAuth=sendrequest(stdurl, querycommand);
                    filesave("logs/deleteCifsAuth.txt", "w", resp_deleteCifsAuth);
                    data = json.loads(resp_deleteCifsAuth.text);
                    if "success" in data["deletecifsauthgroupresponse"]:
                      confirm = data["deletecifsauthgroupresponse"]["success"];
                    if confirm == "true":
                          print "%s is deleted" %(auth_name);
                    else:
                        print "Error : %s" %(data["deletecifsauthgroupresponse"]["errortext"]);
                querycommand = 'command=deleteAccount&id=%s' %(acc_id);
                resp_listDeleteAcc=sendrequest(stdurl, querycommand)
                filesave("logs/listCifsAcc.txt", "w", resp_listDeleteAcc);
                data = json.loads(resp_listDeleteAcc.text);
                if "errortext" in data["deleteAccountResponse"]:
                    print "Error : "+data["deleteAccountResponse"]["errortext"];
                    endTime = ctime()
                    resultCollection("Account %s Deletion" %(config['accountName%d' %(x)]),["FAILED", "%s" %(data["deleteAccountResponse"]["errortext"])],startTime,endTime)
                else:
                    print "%s deleted" %(acc_name)
                    endTime = ctime()
                    resultCollection("Account %s Deletion" %(config['accountName%d' %(x)]),["PASSED", ""],startTime,endTime)
                    time.sleep(1);
    print "\nDeleted ACCOUNTS "
    time.sleep(2);

if poolFlag == 1 or allFlag == 1:
    print "\nDeleting the Pool ... \n"
    querycommand = 'command=listHAPool'
    resp_listPool = sendrequest(stdurl, querycommand)
    filesave("logs/listPool.txt", "w", resp_listPool)
    data = json.loads(resp_listPool.text);
    if "hapool" in data["listHAPoolResponse"]:
        pools = data["listHAPoolResponse"]["hapool"];
    else:
        print "There are no Pools"
        pools = {}
    for pool in pools:
        pool_name = pool["name"];
        pool_id = pool["id"];
        for x in range(1, int(config['Number_of_Pools'])+1):
            startTime = ctime()
            if pool_name == "%s" %(config['poolName%d' %(x)]):
                querycommand = 'command=deleteHAPool&id=%s' %(pool_id)
                resp_deletePool = sendrequest(stdurl, querycommand)
                filesave("logs/deletePool.txt", "w", resp_deletePool)
                data = json.loads(resp_deletePool.text);
                if "success" in data["deleteHAPoolResponse"]:
                    if data["deleteHAPoolResponse"]["success"] == "true":
                        endTime = ctime()
                        print "%s is deleted" %(pool_name)
                        resultCollection("Pool %s Deletion" %(config['poolName%d' %(x)]),["PASSED", ""],startTime,endTime)
                elif "errortext" in data["deleteHAPoolResponse"]:
                    print "Error in Deleting %s : %s " %(pool_name,data["deleteHAPoolResponse"]["errortext"])
                    endTime = ctime()
                    resultCollection("Pool %s Deletion" %(config['poolName%d' %(x)]),["FAILED", "%s" %(data["deleteHAPoolResponse"]["errortext"])],startTime,endTime)
                else:
                    print "something went wrong in deleting Pool see the logs"
                    endTime = ctime()
                    resultCollection("Pool %s Deletion" %(config['poolName%d' %(x)]),["FAILED", "Something went wrong not sure of the cause look into logs"],startTime,endTime)
            time.sleep(1);
    print "\nDeleted All Pools"
    time.sleep(2);

if nodeFlag == 1 or allFlag ==1:
    print "\nDeleting the Node ...\n"
    querycommand = 'command=listController'
    resp_listcontroller = sendrequest(stdurl, querycommand)
    filesave("logs/ListController.txt", "w", resp_listcontroller)
    data = json.loads(resp_listcontroller.text)
    state="Available"
    if "controller" in data["listControllerResponse"]:
        controllerlist = data["listControllerResponse"]["controller"]
    else:
        print "There are no Nodes"
        controllerlist = {}

    for controller in controllerlist:
        startTime = ctime()
        status=controller['managedstate']
        ctrl_name = controller['name']
        ctrl_id = controller['id'];
        if status == state:
            # Maintenance mode
            print "%s is in %s Mode so moving to Maintenance Mode" %(controller['name'],controller['managedstate'] )
            querycommand = 'command=changeControllerState&id=%s&state=Maintenance'%(controller['id'])
            resp_stateofnode= sendrequest(stdurl, querycommand)
            filesave("logs/nodemaintenance.txt", "w", resp_stateofnode)
            data1 = json.loads(resp_stateofnode.text)
            hajob_id=data1["changeControllerStateResponse"]["controller"]["hajobid"]
            querycommand = 'command=listHAJobActivities&hajobid=%s' %(hajob_id)
            hajob=sendrequest(stdurl, querycommand)
            filesave("logs/hajob.txt", "w", hajob)
            data2= json.loads(hajob.text)
            job_id = data2["listHAJobActivitiesResponse"]["jobid"]
            queryAsyncJobResult(stdurl, job_id);
            time.sleep(1);
        querycommand = 'command=deleteController&id=%s' %(ctrl_id)
        resp_delete_controller = sendrequest(stdurl, querycommand)
        filesave("logs/DeleteController", "w", resp_delete_controller)
        data = json.loads(resp_delete_controller.text);
        #print data# 'deleteControllerResponse': {u'success': u'true}
        if not "errortext" in data["deleteControllerResponse"]:
            confirm  = data["deleteControllerResponse"]["success"];
            if confirm == "true":
                endTime = ctime()
                print "%s is deleted" %(ctrl_name)
                resultCollection("Node %s Deletion" %(config['nodeName%d' %(x)]),["PASSED", ""],startTime,endTime)
        else:
            print "\nError in deleteing the %s : %s" %(ctrl_name,data["deleteControllerResponse"]["errortext"])
            endTime = ctime()
            resultCollection("Node %s Deletion" %(config['nodeName%d' %(x)]),["FAILED", "%s" %(data["deleteControllerResponse"]["errortext"])],startTime,endTime)
        #queryAsyncJobResult(stdurl, job_id);
    print "\nDeleted the controllers"
    time.sleep(2);

if haFlag == 1 or allFlag ==1:
    print "\nDeleting Clusters ...\n"
    querycommand = 'command=listHACluster'
    resp_listHACluster = sendrequest(stdurl, querycommand)
    filesave("logs/listHACluster.txt", "w", resp_listHACluster)
    data = json.loads(resp_listHACluster.text)
    if "hacluster" in data["listHAClusterResponse"]:
        haclusters = data["listHAClusterResponse"]["hacluster"]
    else:
        print "There are no clusters"
        haclusters = {} 
    confirm = ""
    for hacluster in haclusters:
         hacluster_id = hacluster['id']
         hacluster_name = hacluster['name']
         for x in range(1, int(config['Number_of_Clusters'])+1):
             startTime = ctime()
             if hacluster_name == "%s" %(config['clusterName%d' %(x)]):
                 if not 'jbods' in hacluster:
                     jbods = {};
                 else:
                     jbods = hacluster['jbods'];
                     print "\nDeleting Jbods ..."
                 for jbod in jbods:
                     jbod_id = jbod['id'];
                     jbod_name = jbod['name'];
                     querycommand = 'command=deleteJBOD&id=%s' %(jbod_id)
                     resp_deleteJBOD = sendrequest(stdurl, querycommand)
                     filesave("logs/resp_deleteJBOD", "w", resp_deleteJBOD)
                     data = json.loads(resp_deleteJBOD.text)
                     if not "errortext" in data["deleteJbodResponse"]:
                         confirm  = data["deleteJbodResponse"]["success"];
                     if confirm == "true":
                         print "%s is deleted" %(jbod_name)
                     else:
                        print "Error in deleteing the %s : %s" %(jbod_name,data["deleteJbodResponse"]["errortext"])
                     time.sleep(1);
                 print "Jbods are Deleted\n";
                 querycommand = 'command=deleteHACluster&id=%s' %(hacluster_id)
                 resp_delete_hacluster = sendrequest(stdurl, querycommand)
                 filesave("logs/DeleteHACluster", "w", resp_delete_hacluster)
                 data = json.loads(resp_delete_hacluster.text)
                 if "errortext" in data["deleteClusterResponse"]:
                     endTime = ctime()
                     print "Error in deleteing the %s : %s"  %(hacluster_name,data["deleteClusterResponse"]["errortext"])
                     resultCollection("HA Cluster %s Deletion" %(config['clusterName%d' %(x)]),["FAILED", "%s" %(data["deleteClusterResponse"]["errortext"])],startTime,endTime)
                 else:
                     confirm  = data["deleteClusterResponse"]["success"];
                 if confirm == "true":
                     print "Deleted the ", hacluster_name
                     endTime = ctime()
                     resultCollection("HA Cluster %s Deletion" %(config['clusterName%d' %(x)]),["PASSED", "" ],startTime,endTime)
                     time.sleep(1);
    print "\nDeleted all Clusters" 
    time.sleep(2);

if siteFlag == 1 or allFlag == 1:
    print "\nDeleting the Sites ...\n"
    querycommand = 'command=listSite'
    resp_listSite = sendrequest(stdurl, querycommand)
    filesave("logs/listSite.txt", "w", resp_listSite)
    data = json.loads(resp_listSite.text)
    confirm =""
    if "site" in data["listSiteResponse"]:
        sites = data["listSiteResponse"]["site"]
    else:
        print "There are no Site's"
        sites = {};
    for site in sites:
        site_id = site['id']
        site_name = site['name']
        for x in range(1, int(config['Number_of_Sites'])+1):
            startTime = ctime()
            if site_name == "%s" %(config['siteName%d' %(x)]):
                querycommand = 'command=deleteSite&id=%s' %(site_id)
                resp_delete_site = sendrequest(stdurl, querycommand)
                time.sleep(1)
                filesave("logs/DeleteSite", "w", resp_delete_site)
                data = json.loads(resp_delete_site.text)
                if "errortext" in data["deleteSiteResponse"]:
                     print "Error in deleting the %s : %s"  %(site_name,data["deleteSiteResponse"]["errortext"])
                     endTime = ctime()
                     resultCollection("Site %s Deletion" %(config['siteName%d' %(x)]),["FAILED", "%s" %(data["deleteSiteResponse"]["errortext"])],startTime,endTime)
                else:
                     confirm  = data["deleteSiteResponse"]["success"];
                if confirm == "true":
                     print "Deleted the Site", site_name
                     endTime = ctime()
                     resultCollection("Site %s Deletion" %(config['siteName%d' %(x)]),["PASSED", "" ],startTime,endTime)

        print "Deleted the ", site_name
    print "\nDeleted all Sites\n"
    time.sleep(2);


import json
import sys
from time import ctime
from cbrequest import *


''' Program to HostAllow and HostDeny in Cifs filesystem        '''
argvlist = []
for i in sys.argv:
    argvlist.append(i)

print argvlist
startTime = ctime()
if len(argvlist) < 4:
    print "Please enter the command properly with required components"
    print "Thr correct command would be: python 'Script.py' 'configfile' 'HostAllow' 'IPs seperated by space' 'HostDeny' 'IP's seperated by space'"
    endTime = ctime()
    resultCollection("Updating HostAllow and HostDeny",["Failed","ProperArgumentRequired"],startTime,endTime)
    exit()
elif str(argvlist[argvlist.index('HostAllow')]) == 'HostAllow' and str(argvlist[argvlist.index('HostDeny')]) == 'HostDeny':
    config = configFile(sys.argv)
    stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
else:
    print "Enter the correct Syntax"
    endTime = ctime()
    resultCollection("Updating HostAllow and HostDeny",["Failed","Enter proper syntax"],startTime,endTime)
    exit()


def HostAllowList(listed):
    argvlist = listed
    posHA = argvlist.index('HostAllow')
    posHD = argvlist.index('HostDeny')
    iplist = []
    for i in range(posHA+1,posHD,1):
        iplist.append(argvlist[i])
    
    return iplist

def HostDeny(listed):
    argvlist = listed
    posHD = argvlist.index('HostDeny')
    lastelement = len(argvlist)
    iplist = []
    for i in range(posHD+1,lastelement,1):
        iplist.append(argvlist[i])
    
    return iplist


tmplist  = []
for i in range(0,len(sys.argv),1):
    tmplist.append(sys.argv[i])

#HAList and HDList tmplist
HAList = HostAllowList(tmplist)
HDList = HostDeny(tmplist)

#To Compare the HAList and HDList to see if a common ip is given present in both Lists
 
for i in HAList:
    if i in HDList:
        print "The same IP %s is present in both HostAllow and HostDeny, hence removing the IP from the HostDeny List " %(HDList.remove(i))


#print "The HostAllow ",HAList, "The Host Deny", HDList

''' List TSM code '''

'''Program to enable CIFS Authentication on All TSM'''
list1 = [1,]
#for x in range(1,int(config['Number_of_TSMs'])+1):
for x in list1:
    querycommand = 'command=listTsm&type=all'
    resp_listTsm = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentTSMList.txt","w",resp_listTsm)
    data = json.loads(resp_listTsm.text)
    tsms = data['listTsmResponse']['listTsm']
    for tsm in tsms:
        if tsm['name'] == "%s"%(config['tsmName%d'%(x)]):
            account_id = tsm['accountid']
            tsm_id = tsm['id']
            break

    querycommand = 'command=listCIFSAuthGroup&accountid=%s'%(account_id)
    resp_listCifsAuthGroup = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentAccountlist","w",resp_listCifsAuthGroup)
    data = json.loads(resp_listCifsAuthGroup.text)
    authgroups = data['listcifsauthgroupresponse']['cifsauthgroup']
    for authgroup in authgroups:
        authName = "%sAUTH" %(config['accountName%d' %(x)])
        #print authName
        if authgroup['name'] == authName:
            authgroup_id = authgroup['id']
            authname = authgroup['name']
            break

    querycommand = 'command=listTsmCifsService&tsmid=%s' %(tsm_id)
    resp_listCifsServiceResponse = sendrequest(stdurl,querycommand)
    data = json.loads(resp_listCifsServiceResponse.text)
    serviceids = data['listTsmcifsServiceResponse']['cifsService']
    for serviceid in serviceids:
        if serviceid['tsmid'] == tsm_id:
            ag_id = serviceid['ag_id']
            serviceid = serviceid['id']
            break


    querycommand = 'command=updateTsmCifsService&&netbiosname=%s&description=undefined&authentication=user&workgroup=undefined&doscharset=CP437&unixcharset=UTF-8&loglevel=Minimum&timeserver=false&authgroupid=%s&id=%s'%(authname,authgroup_id,serviceid)
    resp_updateAccountAuth = sendrequest(stdurl,querycommand)
    data = json.loads(resp_updateAccountAuth.text)
    
#for x in range(1,int(config['Number_of_CIFSVolumes'])+1):
for x in list1:
    querycommand = 'command=listFileSystem'
    resp_listFS = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentFSList.txt","w",resp_listFS)
    data = json.loads(resp_listFS.text)
    fileSystemLists = data['listFilesystemResponse']['filesystem']
    #print fileSystemLists
    for fileSystemList in fileSystemLists:
        if fileSystemList['name'] == "%s" %(config['volCifsDatasetname%d'% (x)]):
            storage_id = fileSystemList['id']
            print "\n\nThe CifsVOlume id is ", fileSystemList['name']
            break
                

    #to obtain CifsService_id
    querycommand = 'command=listFsCifsService&storageid=%s'%(storage_id)
    resp_listCifsFs = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentCifsFS.txt","w",resp_listFS)
    data = json.loads(resp_listCifsFs.text)
    CifsFsLists = data['listFscifsServiceResponse']['cifsService']
    for CifsFsList in CifsFsLists:
        if CifsFsList['storageid'] == storage_id:
            cifsService_id = CifsFsList['id']
            break
                
                
    #To enable HostAllow and HostDeny

    if tmplist[tmplist.index('HostDeny')] == 'HostDeny' and tmplist[tmplist.index('HostAllow')] == 'HostAllow':
        iplength1,iplength2 = len(HDList),len(HAList)
        hdListString = ','.join(HDList)
        haListString = ','.join(HAList)
        querycommand = 'command=updateFsCifsService&datasetid=%s&name=undefined&browseable=false&readonly=false&inheritpermission=true&recyclebin=true&hidedotfiles=false&hostsallow=%s&hostsdeny=%s&id=%s'%(storage_id,haListString,hdListString,cifsService_id)
        resp_updateCifsValue = sendrequest(stdurl,querycommand)
        data = json.loads(resp_updateCifsValue.text)

       
    #Connect to local client
    #Variables need to execute in order
    createDir = 'mkdir /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
    #print createDir
    unmountCommand = 'umount /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
    mountCommand = 'mount -t cifs //%s/%s /mnt/%s -o username=Account1user,password=Account1user'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)],config['volCifsMountpoint%d'%(x)])
    print mountCommand
    mountConfirm = 'mount | grep //%s/%s'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)])
    
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('www.google.com',0))
    HostIp = s.getsockname()[0]
    for ip in HAList:
        if HostIp == ip:
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
    #mountConfirmResult = str(getControllerInfo('127.0.0.1','',mountConfirm,'outputFile'))
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            print mountConfirmResult
            if mountConfirmResult[0].split('/')[2] == "%s" %(config['volCifsIPAddress%d'%(x)]):
                endTime = ctime()
                print "The HostAllow is updated "
                resultCollection("HostAllowIP is updated and verified",["Passed"," "],startTime,endTime)
                executeCmd(umountCommand)
            else:
                #errorStatus = str(data['listFscifsServiceResponse']['cifsService'])
                print "Host Allow failed"
                resultCollection("HostAllowIP Update",["FAILED"," "],startTime,endTime)
                executeCmd(unmountCommand)
                exit()
        else:
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            if mountConfirmResult[0].split('/')[2] == "%s" %(config['volCifsIPAddress%d'%(x)]):
                print "The HostAllow is Successfull"
                endTime = ctime()
                resultCollection("HostAllowIP is updated and verified",["Passed"," "],startTime,endTime)
                executeCmd(unmountCommand)
            else:
                #errorStatus = str(data['listFscifsServiceResponse']['cifsService']['errortext'])
                print "Host Allow failed"
                resultCollection("HostAllowIP Update",["FAILED","errorStatus"],startTime,endTime)
                executeCmd(unmountCommand)
                exit()
    
    #To enable HostDeny

    for ip in HDList:
        if HostIp == ip:
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            if len(mountConfirmResult) == 0:
                print "The host deny has updated and verified"
                endTime = ctime()
                resultCollection("HostDenyIP is updated and verified",["Passed"," "],startTime,endTime)
                executeCmd(umountCommand)
            else:
                print "The HostDenyFeature has failed"
                #errorStatus = str(data['listFscifsServiceResponse']['cifsService'])
                resultCollection("HostAllowIP Update",["FAILED"," "],startTime,endTime)
                executeCmd(unmountCommand)
                exit()
        else:
            querycommand = 'command=updateFsCifsService&datasetid=%s&name=undefined&browseable=false&readonly=false&inheritpermission=true&recyclebin=true&hidedotfiles=false&hostsallow=%s&hostsdeny=%s&id=%s'%(storage_id,haListString,HostIp,cifsService_id)
            resp_updateCifsValue = sendrequest(stdurl,querycommand)
            data = json.loads(resp_updateCifsValue.text)
            
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            print mountConfirmResult
            if len(mountConfirmResult) == 0:
                print "The host deny has updated and verified"
                endTime = ctime()
                resultCollection("HostDenyIP is updated and verified",["Passed"," "],startTime,endTime)
            else:
                print "The HostDeny feature has failed"
                #errorStatus = str(data['listFscifsServiceResponse']['cifsService'])
                resultCollection("HostDenyIP Update",["FAILED"," "],startTime,endTime)
                executeCmd(unmountCommand)
                exit()

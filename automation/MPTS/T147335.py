import json
import sys
from time import ctime
from cbrequest import *
import os


''' Program to Enable and Disable Recycle Bin
        '''
startTime = ctime()

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

#Authentication of CIFS Volumes
#CIFSAuthentication = 'python CIFSAuthentication.py %s'%(sys.argv[1])
#executeCmd(CIFSAuthentication)

# Operation on all CIFS volumes
#for x in range(1,int(config['Number_of_CIFSVolumes'])+1):
for x in range(1,2):
    startTime = ctime()
    #Obtain storage_id through file system
    querycommand = 'command=listFileSystem'
    resp_listFS = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentFSList.txt","w",resp_listFS)
    data = json.loads(resp_listFS.text)
    fileSystemLists = data['listFilesystemResponse']['filesystem']
    #print fileSystemLists
    for fileSystemList in fileSystemLists:
        if fileSystemList['name'] == "%s" %(config['volCifsDatasetname%d'% (x)]):
            storage_id = fileSystemList['id']
            print "\n\nThe storage id is \n", storage_id
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
    
    
    #to enable recycle-bin value
    querycommand = 'command=updateFsCifsService&datasetid=%s&name=undefined&browseable=true&readonly=false&inheritpermission=true&recyclebin=true&hidedotfiles=false&hostsallow=&hostsdeny=&id=%s'%(storage_id,cifsService_id)
    resp_updateCifsValue = sendrequest(stdurl,querycommand)
    filesave("logs/RecycleBinValue","w",resp_updateCifsValue)
    #data = json.loads(resp_updateCifsValue)

    querycommand = 'command=listFsCifsService&storageid=%s'%(storage_id)
    resp_listCifsFs = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentCifsFS.txt","w",resp_listFS)
    data = json.loads(resp_listCifsFs.text)
    CifsFsLists = data['listFscifsServiceResponse']['cifsService']
    for CifsFsList in CifsFsLists:
    #hdValue = data['updateFscifsServiceResponce']['cifsService']
        if str(CifsFsList['recyclebin']) == 'True':
            print "The recycleBinvalue is changed to ",CifsFsList['recyclebin']

            
            #---------x-------Connect to local client--------x-------
            #Variables need to execute in order
            print "\n\n\n\n"
            createDir = 'mkdir /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            unmountCommand = 'umount /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            mountCommand = 'mount -t cifs //%s/%s /mnt/%s -o username=Account1user,password=Account1user'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)],config['volCifsMountpoint%d'%(x)])
            mountConfirm = 'mount | grep //%s/%s'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)])
            
            #Variables need to execute to track recycle bin
            #traceThePath = 'cd /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            createFile = 'touch /mnt/%s/hello1.txt'%(config['volCifsMountpoint%d'%(x)])
            removeFile = 'rm /mnt/%s/hello1.txt'%(config['volCifsMountpoint%d'%(x)])
            lowerIndexOfAccount = config['volCifsAccountName%d' %(x)].lower()
            #traceThePathToRecyclebin = '.recycle/%suser' %(lowerIndexOfAccount)
            delFileConfirm = 'ls /mnt/%s/.recycle/%suser | grep hello1.txt'%(config['volCifsMountpoint%d'%(x)],lowerIndexOfAccount)
            

            print "\n\n\n"

            #Execute declared variables
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            if str(mountConfirmResult[0].split('/')[2]) == "%s" %(config['volCifsIPAddress%d'%(x)]):
                
                executeCmd(createFile)
                executeCmd(removeFile)
                executeCmd(delFileConfirm)
                #recyclebinConfirmation = 'ls /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
                #executeCmd(recyclebinConfirmation)
                #output1 = subprocess.Popen(recyclebinConfirmation, shell=True, stdout=subprocess.PIPE)
                
                output = subprocess.Popen(delFileConfirm, shell=True, stdout=subprocess.PIPE)
                delConfirmResult= output.stdout.readlines()
                createdFile = delConfirmResult[delConfirmResult.index('hello1.txt\n')].split('\n')[0]
                if createdFile == 'hello1.txt':
                    endTime = ctime()
                    print "Recyclebin enabled feature passed"
                    #resultCollection("Recyclebin enabled feature",["PASSED"," "],startTime,endTime)
                else:
                    endTime = ctime()
                    print "Recyclebin enabled feature failed"
                    resultCollection("Recyclebin enabled feature",["FAILED"," "],startTime,endTime)
                    executeCmd(umountCommand)
                    exit()
                executeCmd(unmountCommand)
            else:
                print "Mount the volume failed"
                resultCollection("Recyclebin enable feature failed",["FAILED","Failed to mount volumes"],startTime,endTime)
                executeCmd(unmountCommand)
                exit()
                
        else:
            endTime = ctime()
            errorstatus = CifsFsLists = data['listFscifsServiceResponse']['cifsService']['errortext'] 
            print "The recyclebinvalue is still not changed ",CifsFsList['recyclebin']
            resultCollection("Recyclebin feature failed to update",["Failed","errorstatus"],startTime,endTime)
            exit()

    
    #to disable recycle bin value and observe

    #-----------x-------------x---------------

    querycommand = 'command=updateFsCifsService&datasetid=%s&name=undefined&browseable=true&readonly=false&inheritpermission=true&recyclebin=false&hidedotfiles=false&hostsallow=&hostsdeny=&id=%s'%(storage_id,cifsService_id)
    resp_updateCifsValue = sendrequest(stdurl,querycommand)
    filesave("logs/RecycleBinValue","w",resp_updateCifsValue)
    #data = json.loads(resp_updateCifsValue)
    querycommand = 'command=listFsCifsService&storageid=%s'%(storage_id)
    resp_listCifsFs = sendrequest(stdurl,querycommand)
    filesave("logs/CurrentCifsFS.txt","w",resp_listFS)
    data = json.loads(resp_listCifsFs.text)
    CifsFsLists = data['listFscifsServiceResponse']['cifsService']
    for CifsFsList in CifsFsLists:
        #hdValue = data['updateFscifsServiceResponce']['cifsService']
        if str(CifsFsList['recyclebin']) == 'False':
            print "The recyclebin value is changed to ",CifsFsList['recyclebin']


            #---------x-------Connect to local client--------x-------
            #Variables need to execute in order
            print "\n\n"
            createDir = 'mkdir /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            unmountCommand = 'umount /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            mountCommand = 'mount -t cifs //%s/%s /mnt/%s -o username=Account1user,password=Account1user'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)],config['volCifsMountpoint%d'%(x)])
            mountConfirm = 'mount | grep //%s/%s'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)])

            #Variables need to execute to track recycle bin
            #traceThePath = 'cd /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
            createFile = 'touch /mnt/%s/hello2.txt'%(config['volCifsMountpoint%d'%(x)])
            removeFile = 'rm /mnt/%s/hello2.txt'%(config['volCifsMountpoint%d'%(x)])
            lowerIndexOfAccount = config['volCifsAccountName%d' %(x)].lower()
            #traceThePathToRecyclebin = '.recycle/%suser' %(lowerIndexOfAccount)
            delFileConfirm = 'ls /mnt/%s/.recycle/%suser | grep hello2.txt'%(config['volCifsMountpoint%d'%(x)],lowerIndexOfAccount)
            
            print "\n\n\n"

            #Execute declared variables
            executeCmd(createDir)
            executeCmd(unmountCommand)
            executeCmd(mountCommand)
            output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
            mountConfirmResult = output.stdout.readlines()
            if str(mountConfirmResult[0].split('/')[2]) == "%s" %(config['volCifsIPAddress%d'%(x)]):
                executeCmd(createFile)
                executeCmd(removeFile)
                executeCmd(delFileConfirm)
                
                #recyclebinConfirmation = 'ls /mnt/%s'%(config['volCifsMountpoint%d'%(x)])
                #executeCmd(recyclebinConfirmation)
                #output1 = subprocess.Popen(recyclebinConfirmation, shell=True, stdout=subprocess.PIPE)

                output = subprocess.Popen(delFileConfirm, shell=True, stdout=subprocess.PIPE)
                delConfirmResult= output.stdout.readlines()
                #createdFile = delConfirmResult[delConfirmResult.index('hello2.txt\n')].split('\n')[0]
                for item in delConfirmResult:
                    if item != 'hello2.txt\n':
                        endTime = ctime()
                        print "Recyclebin enabled feature passed"
                        #resultCollection("Recyclebin enabled feature",["PASSED"," "],startTime,endTime)
                    else:
                        endTime = ctime()
                        print "Recyclebin enabled feature failed"
                        resultCollection("Recyclebin enabled feature",["FAILED"," "],startTime,endTime)
                        executeCmd(umountCommand)
                        exit()
                executeCmd(unmountCommand)
            else:
                print "Volume mounting failed"
                resultCollection("Recyclebin disable feature failed",["FAILED","Failed to mount volumes"],startTime,endTime)
                executeCmd(unmountCommand)
                exit()
        else:
            endTime = ctime()
            errorstatus = str(data['listFscifsServiceResponse']['cifsService'])
            print errorstatus
            print "The recyclebinvalue is still not changed to ",CifsFsList['recyclebin']
            resultCollection("Recyclebin feature failed to update",["Failed","%s"%(errorstatus)],startTime,endTime)
            exit()

        endTime = ctime()
        resultCollection("Recyclebin feature tested and verified",["PASSED"," "],startTime,endTime)
            #---------------------x---------------------x-------------------

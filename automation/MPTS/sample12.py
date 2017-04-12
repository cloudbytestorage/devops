import os
from cbrequest import *
import ctypes

#def configFileAccess():
#    config = configFile(sys.argv)
#    getURL(config)
#    return config

def ToExecuteCmdOnShellAndReturnOutput(cmdToBeExecuted):
    output = subprocess.Popen(cmdToBeExecuted, shell=True, stdout=subprocess.PIPE)
    return output.stdout.readlines()

def getDiskAllocatedToISCSI(configfile):
    #config = configFileAccess()
    config = configfile
    toGetIpList = 'iscsiadm -m session'
    toGetAttachedScsiDisk = "iscsiadm -m session -P3 | grep 'Attached scsi disk'"
    strlist = ToExecuteCmdOnShellAndReturnOutput(toGetIpList)
    scsiAssociatedDisk = ToExecuteCmdOnShellAndReturnOutput(toGetAttachedScsiDisk)
    ipList = [i.split(' ')[2].split(':')[0] for i in strlist]
    #print ipList
    accountName = [i.split(' ')[3].split(':')[1].split('\n')[0] for i in strlist]
    #print accountName
    diskAllocatedToScsi = [i.split(' ')[3].split('\t')[0] for i in scsiAssociatedDisk]
    #print diskAllocatedToScsi
    indexDict = {}
    for x in range (0,int(config["Number_of_ISCSIVolumes"]),1):
        for i in range(0,len(ipList),1):
            for j in range(0,len(accountName),1):
                #print ipList[i] + " and " + accountName[j] 
                if ipList[i] == config["voliSCSIIPAddress%d"%(x+1)] and accountName[j] == config["voliSCSIMountpoint%d"%(x+1)]:
                    indexDict = {'%s' %config['voliSCSIDatasetname%d'%(x+1)]:accountName.index(accountName[j])}
                    #print indexDict
    #print indexDict
    for k in indexDict:
        indexDict = {k:diskAllocatedToScsi[indexDict[k]]}
    return indexDict

def toCreateExt4FileSystem(volumeToBeFormated, fs_extension):
    dict1 = getDiskAllocatedToISCSI()
    for i in dict1:
        if i == volumeToBeFormated:
            executeCmd("fdisk /dev/%s < fdisk_response_file" %(dict1[i]))
            executeCmd("mkfs.%s /dev/%s1" %(fs_extension,dict[i]))
            return volumeToBeFormated

if __name__ == "__main__":
    dict1 = getDiskAllocatedToISCSI(configfile)
    print dict1
    #toCreateExt4FileSystem(dict1)
    volumeToBeFormated = 'Account1TSM2ISCSI2'
    toCreateExt4FileSystem(volumeToBeFormated, '/mnt/iscsi1/')

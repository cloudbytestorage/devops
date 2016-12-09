import json
import sys
from time import ctime
from cbrequest import *


''' Program to only Mount and unmount particular volumes '''
config = configFile(sys.argv)
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

if sys.argv[2] == 'mount':
    print "All the mentioned volumes will be mounted"
    for x in range(1,int(config['Number_of_CIFSVolumes'])+1):
        # Mount the volumes from a particular config file.
        createDir = 'mkdir mount/%s'%(config['volCifsMountpoint%d'%(x)])
        #print createDir
        unmountCommand = 'umount mount/%s'%(config['volCifsMountpoint%d'%(x)])
        mountCommand = 'mount -t cifs //%s/%s mount/%s -o username=Account1user,password=Account1user'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)],config['volCifsMountpoint%d'%(x)])
        print mountCommand
        mountConfirm = 'mount | grep //%s/%s'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)])
        executeCmd(createDir)
        executeCmd(unmountCommand)
        executeCmd(mountCommand)
        output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
        mountConfirmResult = output.stdout.readlines()
        print mountConfirmResult
        if mountConfirmResult[0].split('/')[2] == "%s" %(config['volCifsIPAddress%d'%(x)]):
            print "Mounted Successfully"
            print "Volume %s mounted succefully" %(config['volCifsDatasetname%d'%(x)])
        else:
            print "Mounting Unsuccessful"
            exit()
''' Unmount Particular volume '''
if sys.argv[2] == 'umount':
    print "All the volumes mentioned in the config file will be unmounted"
    for x in range(1,int(config['Number_of_CIFSVolumes'])+1):
        #Unmount all the volumes from a particalar file
        unmountCommand = 'umount mount/%s'%(config['volCifsMountpoint%d'%(x)])
        mountConfirm = 'mount | grep //%s/%s'%(config['volCifsIPAddress%d'%(x)],config['volCifsMountpoint%d'%(x)])
        executeCmd(unmountCommand)
        output = subprocess.Popen(mountConfirm, shell=True, stdout=subprocess.PIPE)
        mountConfirmResult = output.stdout.readlines()
        if len(mountConfirmResult) == 0:
            print "Unmounted Successfully"
            print "Volume %s Unmounted succefully" %(config['volCifsDatasetname%d'%(x)])
        else:
            print "Volume Still mounted"
            exit()

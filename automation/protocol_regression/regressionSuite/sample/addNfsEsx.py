import json
import sys
import fileinput
from time import ctime
import time
from itertools import islice
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend, getoutput


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 2:
    print bcolors.WARNING + "python addNfsEsx.py final.txt" + bcolors.ENDC
    exit()

config = configFile(sys.argv);

#tsmip = sys.argv[2]
#esxip = sys.argv[2]
#passwd = sys.argv[3]
esxip = 'ESXIP'
passwd = 'ESXPASSWORD'

#no_of_nfs_share = getoutput('showmount -e %s | wc -l' %(tsmip))
#no_of_nfs_share = int(no_of_nfs_share[0])
#executeCmd('showmount -e %s | awk \'{print $1}\' > nfsdatastore.txt' %(tsmip))
#executeCmd('showmount -e %s |cut -d ":" -f 2|cut -d " " -f 1 > nfsdatastore.txt' %(tsmip))
#f = open('nfsdatastore.txt')

#with open('nfsdatastore.txt') as fin:
#    for line in islice(fin, 1, no_of_nfs_share):
#        mountpoint = str(line)
#        datasetname = mountpoint.split('/')
#        print datasetname[1]
#        #cmd = 'esxcli storage nfs add -H %s -s %s -v %s' %(tsmip, mountpoint, datasetname)

#print no_of_nfs_share
#exit()

for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    startTime = ctime()
    #if tsmip ==  "%s" %(config['volIPAddress%d' %(x)]):
    cmd = 'esxcli storage nfs add -H %s -s %s -v %s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volDatasetname%d' %(x)])
    output = getControllerInfo(esxip, passwd, cmd, "add_nfs_to_esx.txt")
    #if output[0] == 'FAILED':
    #    print 'fail to add'
    print output


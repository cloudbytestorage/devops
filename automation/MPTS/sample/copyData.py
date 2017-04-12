import json
import requests
import md5
import fileinput
import subprocess
import time
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
########### TestCase Execution Starts.. 

print sys.argv[2];
executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')

###NFS
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    if config['volPoolName%d' %(x)] == sys.argv[2]:
        executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
        ######Mount
        executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
        output=executeCmd('mount | grep %s' %(config['volMountpoint%d' %(x)]))
        print "cp -v testfile mount/%s/%s" %(config['volMountpoint%d' %(x)],sys.argv[3])
        #######Copy
        if output[0] == "PASSED":
            executeCmd('cp -v testfile mount/%s/%s' %(config['volMountpoint%d' %(x)],sys.argv[3]))
            print "yes"
        else:
            print "no"
        break ;

executeCmd('umount -a -t cifs -l')
executeCmd('umount -a')

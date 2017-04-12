import json
import requests
import md5
import fileinput
import subprocess
import time

#NoofAccounts=_MyValue_
#NoofTSMs=_MyValue_
#NoofNFSVolumes=_MyValue_
#NoofISCSIVolumes=_MyValue_

#### Function(s) Declaration Begins
def sendrequest(url, querystring): 
    print url+querystring
    response = requests.get(
      stdurl+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;
 

#### Function(s) Declartion Ends


config = {}
with open('config.txt') as cfg:
  config = json.load(cfg)


stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

def executeCmd(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    if rco != 0:
        return "FAILED", str(errors)
    return "PASSED", "\n" ;

def resultCollection(testcase,value):
    f=open("results/result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.close()
    return;

def msg():
    msg = 'Press y to Continue or Any other key to exit? \n'
    if (raw_input("%s (y/N) " % msg).lower() == 'y'):
        print "Proceed"
    else:
        print "Still Proceeding :)"
    return;
 

for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['volMountpoint%d' %(x)]))
    ######Mount
    output=executeCmd('mount -t nfs %s:/%s mount/%s' %(config['volIPAddress%d' %(x)], config['volMountpoint%d' %(x)], config['volMountpoint%d' %(x)]))
    resultCollection("Mount of NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)
    #######Copy
    executeCmd('cp testfile  mount/%s' %(config['volMountpoint%d' %(x)]))
    output=executeCmd('diff testfile mount/%s' %(config['volMountpoint%d' %(x)]))
    resultCollection("Creation of File on NFS Volume %s" %(config['volDatasetname%d' %(x)]), output)



for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    ######Login to ISCSI
    output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --login | grep Login' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
    resultCollection("Login of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
    ######Copy
    executeCmd('fdisk /dev/sdb')
    executeCmd('mkfs.ext3 /dev/sdb1')
    executeCmd('mount /dev/sdb1  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    executeCmd('cp testfile  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    output=executeCmd('diff testfile mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    resultCollection("Creation of File on ISCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)
    msg()

    executeCmd('umount  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
    ######Logout to ISCSI
    output=executeCmd('iscsiadm -m node --targetname "iqn.%s.%s.%s:%s" --portal "%s:3260" --logout | grep Logout' %(time.strftime("%Y-%m"), config['voliSCSIAccountName%d' %(x)], config['voliSCSITSMName%d' %(x)], config['voliSCSIMountpoint%d' %(x)], config['voliSCSIIPAddress%d' %(x)]))
    resultCollection("Logout of iSCSI Volume %s" %(config['voliSCSIDatasetname%d' %(x)]), output)


 
exit()



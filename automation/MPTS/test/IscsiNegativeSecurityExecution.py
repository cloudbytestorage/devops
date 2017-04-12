import json
import requests
import md5
import fileinput
import subprocess
import time
from time import ctime
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, executeCmd, getoutput, getControllerInfo
#import setISCSIInitiatorGroup.py
if len(sys.argv) < 2:
    print "Argument is not correct.. Correct way as below"
    print "python IscsiSecurityExecution.py dedup.txt  "
    exit()
config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
#assign default access to all iscsi volumes
executeCmd('python setISCSIInitiatorGroup.py dedup.txt None')
#executeCmd('python setIscsiAuthMethod.py dedup.txt mutualchap')
# for all iscsi volumes in config files
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    startTime=ctime()
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    #initiator is None
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
       print "no iscsi volumes discovered on the client when initiator is None"
       endTime = ctime()
       resultCollection("iscsi volume %s not discovered on the client when initiator group is None"%(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
    else:
        endTime = ctime()
        resultCollection("iscsi volume %s discovered on the client when volume's initiator group is None"%(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
#end of initiator None
#start of Negative auth method CHAP
executeCmd('python setISCSIInitiatorGroup.py dedup.txt')
executeCmd('python setIscsiAuthGroup.py dedup.txt AuthGrp1')
executeCmd('python setIscsiAuthMethod.py dedup.txt chap')
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    startTime=ctime()
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    #initiator is ALL
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
       print "no iscsi volumes discovered on the client "
       endTime = ctime()
       resultCollection("iscsi volume %s not discovered on the client when initiator group is ALL"%(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
    else:
        ### Login to ISCSI
        print"degault login timeout 120secs,retries login upto 120 secs"
        output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        print output[0]
        time.sleep(5)
        endTime = ctime()
        if output[0] == "PASSED":
            print"iscsi volume login possible on the client when using wrong CHAP credential"
            resultCollection("iscsi volume %s login  possible on the client when using wrong CHAP credential"%(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
            executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        else:
            print"iscsi volume login not possible on the client when using wrong CHAP credential"
            resultCollection("iscsi volume %s login not possible on the client when using wrong CHAP credential"%(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)

#end of Negative auth method CHAP

#start of Negative auth method MutualCHAP
executeCmd('python setISCSIInitiatorGroup.py dedup.txt')
executeCmd('python setIscsiAuthGroup.py dedup.txt AuthGrp1')
executeCmd('python setIscsiAuthMethod.py dedup.txt mutualchap')
for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    startTime=ctime()
    executeCmd('iscsiadm -m discovery -t st -p %s:3260' %(config['voliSCSIIPAddress%d' %(x)]))
    #initiator is ALL
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    print iqnname
    if iqnname==[]:
       print "no iscsi volumes discovered on the client "
       endTime = ctime()
       resultCollection("iscsi volume %s not discovered on the client when initiator group is ALL"%(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
    else:
        ### Login to ISCSI
        print"degault login timeout 120secs,retries login upto 120 secs"
        output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        print output[0]
        time.sleep(5)
        endTime = ctime()
        if output[0] == "PASSED":
            print"iscsi volume login possible on the client when using wrong Mutual-CHAP credential"
            resultCollection("iscsi volume %s login  possible on the client when using wrong Mutual-CHAP credential"%(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
            executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
        else:
            print"iscsi volume login not possible on the client when using wrong Mutual-CHAP credential"
            resultCollection("iscsi volume %s login not possible on the client when using wrong Mutual-CHAP credential"%(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)

#end of Negative auth method MutualCHAP
executeCmd('python setIscsiAuthMethod.py dedup.txt')
executeCmd('python setIscsiAuthGroup.py dedup.txt')

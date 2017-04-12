import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmd, executeCmdNegative,  resultCollection, getoutput
config = configFile(sys.argv);

stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
negativeFlag = 0
if len(sys.argv)== 3:
    if sys.argv[2].lower()== "negative":
        negativeFlag = 1;
    else:
        print "Argument is not correct.. Correct way as below"
        print " python verifyIqn.py config.txt"
        print " python verifyIqn.py config.txt negative"
        exit()


for x in range(1, int(config['Number_of_ISCSIVolumes'])+1):
    startTime = ctime()
    executeCmd('mkdir -p mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))

    ### Discovery
    iqnname = getoutput('iscsiadm -m discovery -t st -p %s:3260 | grep %s | awk {\'print $2\'}' %(config['voliSCSIIPAddress%d' %(x)],config['voliSCSIMountpoint%d' %(x)]))
    # for negative testcase
    if negativeFlag == 1:
        ###no iscsi volumes discovered
        if iqnname==[]: 
            print "Negative testcase-iscsi volume %s login failed on the client with dummy iqn and ip, testcase passed" %(config['voliSCSIDatasetname%d' %(x)])
            endTime = ctime()
            resultCollection("Negative testcase-iscsi volume %s login failed on the client with dummy iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
        ### some iscsi volumes discovered
        else:
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            ### iscsi volume login successfull
            if output[0] == "PASSED":
                print "Negative testcase-iscsi volume %s login passed on the client with dummy iqn and ip, test case failed" %(config['voliSCSIDatasetname%d' %(x)])
                endTime = ctime()
                resultCollection("Negative testcase-iscsi volume %s login passed on the client with dummy iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
            ### iscsi volume login unsuccessfull
            else:
                print "Negative testcase-iscsi volume %s login failed on the client with dummy iqn and ip, testcase passed"  %(config['voliSCSIDatasetname%d' %(x)])
                endTime = ctime()
                resultCollection("Negative testcase-iscsi volume %s login failed on the client with dummy iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)

    
    # for positive testcase
    else:   
        ###no iscsi volumes discovered
        if iqnname==[]:
            print "iscsi volume %s login failed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)])
            endTime = ctime()
            resultCollection("iscsi volume %s login failed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
        ### some iscsi volumes discovered
        else:
            output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --login | grep Login' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))
            ### iscsi volume login successfull
            if output[0] == "PASSED":
                print "iscsi volume %s login passed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)])
                endTime = ctime()
                resultCollection("iscsi volume %s login passed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
                #### if login successfull mount and copy some data
                device = getoutput('iscsiadm -m session -P3 | grep \'Attached scsi disk\' | awk {\'print $4\'}')
                device2 = (device[0].split('\n'))[0]
                executeCmd('fdisk /dev/%s < fdisk_response_file' (device2))
                executeCmd('mkfs.ext3 /dev/%s1' %(device2))
                executeCmd('mount /dev/%s1  mount/%s' %(device2, config['voliSCSIMountpoint%d' %(x)]))
                executeCmd('cp testfile  mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                output=executeCmd('diff testfile mount/%s' %(config['voliSCSIMountpoint%d' %(x)]))
                if output[0] == "PASSED":
                    endtime = ctime() 
                    resultCollection("Creation of File on ISCSI Volume %s passed on the client with iqn and ip credentials" %(config['voliSCSIDatasetname%d' %(x)]),["PASSED",""], startTime, endTime)
                else:
                    endtime = ctime()
                    resultCollection("Creation of File on ISCSI Volume %s passed on the client with iqn and ip credentials" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
            ### iscsi volume login unsuccessfull
            else:
                print "iscsi volume %s login failed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)])
                endTime = ctime()
                resultCollection("iscsi volume %s login failed on the client with iqn and ip" %(config['voliSCSIDatasetname%d' %(x)]),["FAILED",""], startTime, endTime)
    ### logout
    output=executeCmd('iscsiadm -m node --targetname "%s" --portal "%s:3260" --logout | grep Logout' %(iqnname[0].strip(), config['voliSCSIIPAddress%d' %(x)]))


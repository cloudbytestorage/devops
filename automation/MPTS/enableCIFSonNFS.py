import time
import sys
import os
from time import ctime
from cbrequest import configFile, sendrequest, executeCmd, resultCollection, listVolume, enabledDisableCIFS, mountCIFS, umountVolume

if len(sys.argv) < 3:
    print 'Given parameter are not correct, please provide as folloing parameters'
    print 'python enableCIFSonNFS.py snapshot.txt true/false'
    exit()

config = configFile(sys.argv)
configFileName = sys.argv[1]
operation = sys.argv[2]
startTime = ctime()

#############################################################################################

### If volumes are not created than delete comment

# creating NFS volumes
#createNFS = executeCmd('python NFSVolume.py %s' %(configFileName))

# setting client to ALL
#setToALL = executeCmd('python setNFSclients.py %s' %(configFileName))

# mapping NFS lun to client and running iops
#copyData = executeCmd('python execution.py %s nfs' %(configFileName))

#############################################################################################

# list volumes
volumes = listVolume(config)

endTime = ctime()
# checking volumes are there or not
if volumes[0] == 'PASSED':
    volumes = volumes[1]
elif volumes[0] == 'BLOCKED':
    print 'There is no volume for list'
    resuleCollection('There is no volume, So skippping test case for enabling cifs on nfs enabled volume', ['BLOCKED', ''], startTime, endTime)
    exit()
else:
    print 'Faile to list volumes due to: ' + volumes[1]
    resultCollection('Failed to list volumes, So skipping test case for enabling cifs on nfs enabled volume', ['BLOCKED' , volumes[1]], startTime, endTime)
    exit()

# Enabling cifs on nfs enabled volumes
for x in range(1, int(config['Number_of_NFSVolumes'])+1):
    for volume in volumes:
        # getting volume id
        if volume['name'] == "%s" %(config['volDatasetname%d' %(x)]):
            vol_id = volume['id']
            if vol_id is not None:
                startTime = ctime()
                # enabling cifs
                result = enabledDisableCIFS(config, vol_id, operation)
                endTime = ctime()
                # checking for cifs enable successful or not
                if result[0] == 'PASSED':
                    resultCollection('Enable cifs protocol \"%s\" on a nfs enabled volume %s is :' %(config['volDatasetname%d' %(x)], operation), ['PASSED', ''], startTime, endTime)
                else:
                    resultCollection('Skipping further execution of enable cifs on nfs enabled volume test, Enable cifs protocon \"%s\" on a nfs enabled volume %s is :' %(config['volDatasetname%d' %(x)], operation), ['FAILED', result[1]], startTime, endTime)
                    exit()

                time.sleep(2)
                startTime = ctime()
                # mapping volume as a cifs share
                vol = {'name': '%s' %(config['volDatasetname%d' %(x)]), 'mountPoint': '%s' %(config['volMountpoint%d' %(x)]), 'AccountName': '%s' %(config['volAccountName%d' %(x)]), 'TSMIPAddress': '%s' %(config['volIPAddress%d' %(x)])}
                # mount
                mount = mountCIFS(vol)
                #umount
                uMount = umountVolume(vol)
                endTime = ctime()
                if mount == 'PASSED' and operation.lower() == 'true':
                    print 'Mount passed after cifs enable on a nfs enabled volume'
                    resultCollection('Mount passed after cifs enable on a nfs enabled volume', ['PASSED', ''], startTime, endTime)
                    startTime = ctime()
                    disableResult = enabledDisableCIFS(config, vol_id, 'false')
                    endTime = ctime()
                    if disableResult[0] == 'PASSED':
                        print 'disable cifs on nfs enabled volume is passed'
                        resultCollection('disable cifs on nfs enabled volume is: ', ['PASSED', ''], startTime, endTime)
                    else:
                        print 'disable cifs on nfs enabled volume is failed'
                        resultCollection('disable cifs on nfs enabled volume is: ', ['FAILED', disableResult[1]], startTime, endTime)
                    mountCifsDisable = mountCIFS(vol)
                    endTime = ctime()
                    if mountCifsDisable == 'FAILED':
                        print 'Not able to mount a cifs disable as cifs share, passed'
                        resultCollection('Not able to mount a cifs disable as cifs share', ['PASSED', ''], startTime, endTime)
                    else:
                        print 'Able to mount a cifs disable as cifs share, failed'
                        resultCollection('Able to mount a cifs disable as cifs share', ['FAILED', ''], startTime, endTime)
                elif mount == 'FAILED' and operation.lower() == 'false':
                    print 'Mounting as cifs share on a cifs disabled volume is failed'
                    resultCollection('Mounting as cifs share on a cifs disabled volume is failed', ['PASSED', ''], startTime, endTime)
                elif mount == 'PASSED' and operation.lower() == 'false':
                    umountVolume(vol)
                    print 'Able to mount as a cifs share on a cifs disabled volume'
                    resultCollection('Able to mount as a cifs share on a cifs disabled volume', ['FAILED', ''], startTime, endTime)

                else:
                    print 'Mount as a cifs share of a cifs enabled volume is failed'
                    resultCollection('Mount as a cifs share of a cifs enabled volume is failed', ['FAILED', ''], startTime, endTime)

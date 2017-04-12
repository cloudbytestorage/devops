set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test    
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test      
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?

set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 
> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?
python ISCSIVolume.py regression.txt
should_exit $?
python setISCSIInitiatorGroup.py regression.txt
should_exit $?
python NFSVolume.py regression.txt
should_exit $?
python setNFSclients.py regression.txt
should_exit $?
python CIFSVolume.py regression.txt
should_exit $?
python setCIFSAuthentication.py regression.txt
should_exit $?

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?
python vlanAdd.py regression.txt 20.10.57.103 test
should_exit $?
python vlanDelete.py regression.txt 20.10.57.103 test
should_exit $?

python staticIPAdd.py regression.txt 20.10.57.103 test 
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPAdd.py regression.txt 20.10.57.103 test
should_exit $?
python staticIPDelete.py regression.txt 20.10.57.103 test
should_exit $?


python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?




###############apeksha.sh
######## generating csv files
sh ConfigurationFromCSV.sh expandVol.csv
should_exit $?
sh ConfigurationFromCSV.sh tpAlert.csv
should_exit $?
sh ConfigurationFromCSV.sh spaceReclaim.csv
should_exit $?
sh ConfigurationFromCSV.sh copyVol.csv
should_exit $?
sh ConfigurationFromCSV.sh dummyVol.csv
should_exit $?


########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?



####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?



python Version.py smoketest.txt
should_exit $?



############# Mardan

sh ConfigurationFromCSV.sh snapshot.csv
should_exit $?


python apikey_get.py deleteCloneDataset.txt
python apikey_get.py snapshot.txt


## creating volumes
python ISCSIVolume.py snapshot.txt
should_exit $?
python NFSVolume.py snapshot.txt
should_exit $?
python CIFSVolume.py snapshot.txt
should_exit $?

## enabling the initiators
python setISCSIInitiatorGroup.py snapshot.txt
should_exit $?
python setNFSclients.py snapshot.txt
should_exit $?
python setCIFSAuthentication.py snapshot.txt
should_exit $?


### ------------------------  T89790 & T89838 ----------------------------------------------------

## ------- To check if basic Dataset level Instant Snapshot/Restore/Delete works fine
## ------- Verify data persistence on iscsi LUN instant snapshot restore/rollback
## ------- Delete snapshot part of this test case will be done in next group

## ------- mount write mkfs and copy file(any)
python execution.py snapshot.txt all create cbrequest.py
should_exit $?
## ------- create snapshot
python createDeleteSnapshot.py snapshot.txt all create test_101 20.10.57.103 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
## ------- execution of executionRevertSnapshot
python executionRevertSnapshot.py snapshot.txt all cbrequest.py createDeleteSnapshot.py

### ------------------------ End of T89790 & T89838 ----------------------------------------------


### ------------------------ T89796 & T89797 & T89798 &T89800 & T89801 ---------------------------

## ------- Take snapshot of NFS Volume and Clone it and verify the data
## ------- Take snapshot of CIFS Volume and Clone it and verify the data
## ------- Take snapshot of iSCSI LUN and Clone it and verify the data
## ------- Delete snapshot from which clone is created
## ------- Delete clone

## ------- Clones
python createCloneDataset.py snapshot.txt all test_101 1 20.10.57.103 test 

should_exit $?
## ------- Enabling the initiators
#python setISCSIInitiatorGroup.py deleteCloneDataset.txt
#should_exit $?
#python setNFSclients.py deleteCloneDataset.txt
#should_exit $?
#python setCIFSAuthentication.py deleteCloneDataset.txt
#should_exit $?

## ------- Mount Clone dataset and copy some data
python execution.py deleteCloneDataset.txt all copy execution.py
## ------- Verifying the data of Cloned Volume
python executionRevertSnapshot.py deleteCloneDataset.txt all cbrequest.py

## ------- Mount Clone dataset and copy some data
#python execution.py deleteCloneDataset.txt all copy execution.py

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test

## ------- Delete clone dataset
python delete.py deleteCloneDataset.txt nfs iscsi cifs

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 20.10.57.103 test


### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 20.10.57.103 test
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 20.10.57.103 test

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.py copy2.py copy3.py
python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------

sh mail.sh
should_exit $?


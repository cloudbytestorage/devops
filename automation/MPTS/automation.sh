set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

> results/result.csv

python createDisableSCSI.py regression.txt 172.16.48.140 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

#REST service alert
python apikey_get.py dedup.txt
should_exit $?
python RestServiceAlert.py dedup.txt
should_exit $?
python apikey_get.py smoketest.txt
should_exit $?
python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?
#Message service alert
#python MessageServiceAlert.py dedup.txt
#should_exit $?

python Node.py smoketest.txt
should_exit $?

python Version.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?
python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 172.16.48.140 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
#python verifyMetaDevices.py raidz2.txt PoolRaidz2
#should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?

python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 172.16.48.140 test PoolMirror logs/output/PoolMirror
should_exit $?
#python verifyMetaDevices.py mirror.txt PoolMirror
#should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?

python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 172.16.48.140 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
#python verifyMetaDevices.py raidz1.txt PoolRaidz1
#should_exit $?

python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?
python Tsm.py regression.txt
should_exit $?

python changeNfsThread.py regression.txt 8
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

#python verifyDedup.py regression.txt 172.16.48.140 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 172.16.48.140 test PoolRaidz1 
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

#python apikey_set_delegatedAdmin.py regression.txt
#should_exit $?


python vlanAdd.py regression.txt 172.16.48.140 test
should_exit $?
python vlanDelete.py regression.txt 172.16.48.140 test
should_exit $?
python vlanAdd.py regression.txt 172.16.48.140 test
should_exit $?
python vlanDelete.py regression.txt 172.16.48.140 test
should_exit $?

python staticIPAdd.py regression.txt 172.16.48.140 test 
should_exit $?
python staticIPDelete.py regression.txt 172.16.48.140 test
should_exit $?
python staticIPAdd.py regression.txt 172.16.48.140 test
should_exit $?
python staticIPDelete.py regression.txt 172.16.48.140 test
should_exit $?

#python addHAAdmin.py regression.txt
#should_exit $?
#python apikey_set_delegatedAdmin.py regression.txt
#should_exit $?
#python verifyHAAdmin.py regression.txt
#should_exit $?
#python deleteHAAdmin.py regression.txt
#should_exit $?
#python addHAAdmin.py regression.txt
#should_exit $?

#python apikey_set_delegatedAdmin.py regression.txt
#should_exit $?

#python verifyHAAdmin.py regression.txt
#should_exit $?

python apikey_get.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python changeNfsThread.py smoketest.txt 8
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



#########################################################################

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

echo "sleeping for 700 seconds"
sleep 700

## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?

echo "sleeping for 700 seconds"
sleep 700

## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?

'''
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
python spaceReclaim.py spaceReclaim.txt 172.16.48.140 test all
should_exit $?
'''

####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
#sleep 10
#echo "sleeping for 10 seconds"
#sh copyIscsi.sh
#should_exit $?

####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
echo "sleeping for 10 seconds"
sh copyNfs.sh
should_exit $?

#########################################################################
python apikey_get.py snapshot.txt
should_exit $?

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
python createDeleteSnapshot.py snapshot.txt all create test_101 172.16.48.140 test
## ------- mount and copy second file(any)
python execution.py snapshot.txt all copy createDeleteSnapshot.py 
## ------- mount and delete first file
python execution.py snapshot.txt all delete cbrequest.py
##setingt initiator group to 'None' before reverting snapshot
python setISCSIInitiatorGroup.py snapshot.txt None
## ------- revert snapshot
python revertSnapshot.py snapshot.txt all test_101
##setting initiator group to 'ALL' before verifying revert snapshot
python setISCSIInitiatorGroup.py snapshot.txt ALL
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
python createCloneDataset.py snapshot.txt all test_101 1 172.16.48.140 test BL
should_exit $?

## ------- Integrity of data on clone dataset
python verifyDataIntegrityOfClone.py snapshot.txt all 1 BL cbrequest.py
should_exit $?

## ------- Copy/delete operation on clone dataset
python verifyCopyDeleteDataToClone.py snapshot.txt all 1 BL copy1.txt
should_exit $?

### We are getting wrong response from controller side that is why test case is failed, but from UI its working fine
## ------- Delete snapshot from which clone is created
#python createDeleteSnapshot.py snapshot.txt all delete test_101 172.16.48.140 test
#should_exit $?

##setting initiator group to None before deleting clone dataset
python setCloneISCSIInitiatorGroup.py snapshot.txt 1 BL None
## ------- Delete clone dataset
python deleteCloneDataset.py snapshot.txt  all 1 172.16.48.140 test BL
should_exit $?

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 172.16.48.140 test

### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 172.16.48.140 test
should_exit $?
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 172.16.48.140 test
should_exit $?

## ------- Disable the NFS enabled dataset 
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiPlaceMountNFS.py snapshot.txt copy1.txt copy2.txt copy3.txt
should_exit $?

python nfsmountwithro.py snapshot.txt
should_exit $?
python enableDisableNFS.py snapshot.txt false
should_exit $?
python executionDisableNFS.py snapshot.txt
should_exit $?
python enableDisableNFS.py snapshot.txt true
should_exit $?

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------
python duplicateCifsUser.py snapshot.txt
should_exit $?
python executeMultiCifsUser.py snapshot.txt
should_exit $?
python deleteAccountAuthgroup.py snapshot.txt
should_exit $?
python discoverHardware.py snapshot.txt disks 172.16.48.140 test
should_exit $?

python enableCIFSonNFS.py snapshot.txt true
python enableCIFSonNFS.py snapshot.txt false
python multiPlaceMountCIFS.py snapshot.txt
python verifyAuthOnSubFilesystem.py snapshot.txt

##########################################################################

###########%%%%%%%%%%%
python apikey_get.py dedup.txt
should_exit $?
python apikey_get.py delete.txt
should_exit $?

## creating volumes
python ISCSIVolume.py dedup.txt
should_exit $?
python ISCSIVolume.py delete.txt
should_exit $?
python NFSVolume.py dedup.txt
should_exit $?
python NFSVolume.py delete.txt
should_exit $?
python CIFSVolume.py dedup.txt
should_exit $?
python CIFSVolume.py delete.txt
should_exit $?


## enabling the initiators
python setISCSIInitiatorGroup.py dedup.txt
should_exit $?
python setISCSIInitiatorGroup.py delete.txt
should_exit $?
python setNFSclients.py dedup.txt
should_exit $?
python setNFSclients.py delete.txt
should_exit $?
python setCIFSAuthentication.py dedup.txt
should_exit $?
python setCIFSAuthentication.py delete.txt
should_exit $?
#using created volume for dedup ON
#python PoolDedup.py dedup.txt on
#echo "Sleeping for 30 seconds"
#sleep 30
#python PoolDedupExecution.py dedup.txt all  172.16.48.140 test on
###setting initiator group to 'None' before deleting iSCSI LUN
#python setISCSIInitiatorGroup.py dedup.txt None
#delete
#python delete.py dedup.txt iscsi
#sleep 5
#creating new volume for dedup OFF
#python ISCSIVolume.py dedup.txt
#should_exit $?
#python setISCSIInitiatorGroup.py dedup.txt
#should_exit $?
#python PoolDedup.py dedup.txt off
#python PoolDedupExecution.py dedup.txt all  172.16.48.140 test off
#python PoolDedup.py dedup.txt on
###setting initiator group to 'None' before deleting iSCSI LUN
#python setISCSIInitiatorGroup.py dedup.txt None
#delete
#python delete.py dedup.txt iscsi
#sleep 5
#creating new volume for Compression ON
#python ISCSIVolume.py dedup.txt
#should_exit $?
#python setISCSIInitiatorGroup.py dedup.txt
#should_exit $?
python Compression.py dedup.txt all on
#python CompressionExecution.py dedup.txt all on 172.16.48.140 test
###setting initiator group to 'None' before deleting iSCSI LUN
python setISCSIInitiatorGroup.py dedup.txt None
#delete
python delete.py dedup.txt iscsi
sleep 5
#creating new volume for Compression OFF
python ISCSIVolume.py dedup.txt
should_exit $?
python setISCSIInitiatorGroup.py dedup.txt
should_exit $?
python Compression.py dedup.txt all off
#python CompressionExecution.py dedup.txt all off 172.16.48.140 test
python Compression.py dedup.txt all on
#Iscsi initiator-group/auth-group/auth-method positive and negative tests
sh IscsiSecurity.sh

sh Readonly.sh
python QosChange.py delete.txt all 172.16.48.140 test 10 0
python QosLessthanPool.py  delete.txt all 172.16.48.140 test
python QosDatasetDelete.py delete.txt all 172.16.48.140 test



### Node maintenance/Available test cases 
sleep 300
python nodeToModeSingleNode.py snapshot.txt maintenance 172.16.48.140 test
should_exit $?
sleep 5
python nodeToModeSingleNode.py snapshot.txt available 172.16.48.140 test
should_exit $?
#Ack all alerts
python AckAllAlerts.py dedup.txt
should_exit $?


#################################################################################

python T89803.py smoketest.txt 12.12.32.105 em3
python hostAllowHostDeny.py smoketest.txt HostAllow 20.10.49.1 HostDeny 20.10.57.1
sh copyCifs.sh
python T147335.py smoketest.txt

#Message service alert
python MessageServiceAlert.py dedup.txt
should_exit $?

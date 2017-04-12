set -o history -o histexpand
should_exit(){
    if [ $1 -ne 0 ];
    then
        echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
        exit
    fi
}

#> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

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
python createDeleteSnapshot.py snapshot.txt all create test_101 NODEIP1 NODEPASSWORD1
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
python createCloneDataset.py snapshot.txt all test_101 1 NODEIP1 NODEPASSWORD1 BL
should_exit $?

## ------- Integrity of data on clone dataset
python verifyDataIntegrityOfClone.py snapshot.txt all 1 BL cbrequest.py
should_exit $?

## ------- Copy/delete operation on clone dataset
python verifyCopyDeleteDataToClone.py snapshot.txt all 1 BL copy1.txt
should_exit $?

## ------- Delete snapshot from which clone is created
python createDeleteSnapshot.py snapshot.txt all delete test_101 NODEIP1 NODEPASSWORD1
should_exit $?


## ------- Delete clone dataset
python deleteCloneDataset.py snapshot.txt  all 1 NODEIP1 NODEPASSWORD1 BL
should_exit $?

## ------- Delete Snapshot
python createDeleteSnapshot.py snapshot.txt all delete test_101 NODEIP1 NODEPASSWORD1

### ------------------------ End of T89796 & T89797 & T89798 &T89800 & T89801 --------------------

### ------------------------ T89618 & T89621 & T89623 --------------------------------------------

### ----------------------- TSM level snapshot----------------------------------------------------

python createDeleteSnapshot.py snapshot.txt tsm create tsmsnp101 NODEIP1 NODEPASSWORD1
python createDeleteSnapshot.py snapshot.txt tsm delete tsmsnp101 NODEIP1 NODEPASSWORD1

## ------- Disable the NFS enabled dataset
## ------- Mount NFS Share on 3 different locations and perform IO on all 3 and check the files added from 3 mount points are available on the server side
## ------- Add the nfs mount point in the fstab with ro option and observe the client behavior

python multiplacemount.py snapshot.txt copy1.txt copy2.txt copy3.txt

python nfsmountwithro.py snapshot.txt
python enableDisableNFS.py snapshot.txt false
python executionDisableNFS.py snapshot.txt
python enableDisableNFS.py snapshot.txt true

### ------------------------ End of T89618 & T89621 & T89623 -------------------------------------
python duplicateCifsUser.py snapshot.txt
python executeMultiCifsUser.py snapshot.txt


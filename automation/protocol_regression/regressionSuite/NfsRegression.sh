# CLEAN THE SYSTEM
python cleanup.py conf.txt

python create_pool_vsms.py conf.txt

python addClientsToExports.py conf.txt filesystem_nfs
python removeClientFromExports.py conf.txt filesystem_nfs
python nfsSoftHardmount.py conf.txt soft
python nfsSoftHardmount.py conf.txt hard
python nfsSetAllDirToNo.py conf.txt filesystem_nfs
python TSMIPChangeofNFSdataset.py conf.txt filesystem_nfs
python NFSAlerts.py conf.txt
python NFSHomedir.py conf.txt
python umountUsedmountPoint.py conf.txt filesystem_nfs
python nfsDatasetUsed_AvailSpace.py conf.txt filesystem_nfs
python nfsReadOnlyDataset.py conf.txt filesystem_nfs
python nfsPropEdit.py conf.txt filesystem_nfs


python NFSMountPrtcl.py conf.txt TCP
python NFSMountPrtcl.py conf.txt UDP
python updNFSQos.py conf.txt iopsenable 50
python updNFSQos.py conf.txt iopsdisable 60
python CreateMountDeletenfs.py conf.txt
python nfs_Authorization.py conf.txt

python cleanup.py conf.txt
python create_pool_vsms.py conf.txt

python snpNFSVol.py conf.txt
python graceFullHANFS.py conf.txt
python ungraceFullHANFS.py conf.txt
#python partial_fail_over_nfs.py conf.txt

python cleanup.py conf.txt
python nfs_share_100_mount.py conf.txt

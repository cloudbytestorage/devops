# CLEAN THE SYSTEM
python cleanup.py conf.txt

# creaing configuration for running iscsi regression test cases
python create_pool_vsms.py conf.txt

python moreInitiatorInHostAllow.py conf.txt 
python ISCSIAlerts.py conf.txt
python ISCSIvolcreate.py conf.txt

python updIscsiQos.py conf.txt iopsenable 70
python updIscsiQos.py conf.txt iopsdisable 80
python updIscsiFileSystem.py conf.txt readonly true
python updIscsiFileSystem.py conf.txt compression on
python changeHAAvailabilityInIscsi.py conf.txt 89 75
python iscsiCreateInitGrp.py conf.txt 

python iscsi_with_CHAP.py conf.txt chap1 chapuser1 123456789123 mchapuser1 123456789012 ALL
python snpISCSIVolume.py conf.txt
python graceFullHAiSCSI.py conf.txt
python ungraceFullHAiSCSI.py conf.txt
python partial_fail_over_iscsi.py conf.txt
python ISCSIOvernightio.py conf.txt moreVol #has to change the logic for IOPS 

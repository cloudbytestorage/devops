echo "iSCSI iqn Mapping with disks"
echo "VolumeName,IQN,DISK,SCSI" > /tmp/iscsi_map
echo " VolumeName         IQN                      DISK  SCSI" 
iscsiadm -m session > /tmp/iscsisesssion
iscsiadm -m session -P3  | grep "Target\|sd\|Lun" > /tmp/iscsissessiondetails
while read line
do
   iqn=`echo $line | awk '{print $4}'`
   #echo $iqn
   scsi=`grep $iqn  -A 2 /tmp/iscsissessiondetails | grep Channel | awk '{print $1}'`
   disk=`grep $iqn  -A 2 /tmp/iscsissessiondetails | grep Attached | awk '{print $4}'`
   volumename=` grep -A 1 $scsi /proc/scsi/scsi  | grep Vendor | awk '{print $4}'`
   echo " $volumename $iqn $disk $scsi "
   echo $volumename,$iqn,$disk,$scsi >> /tmp/iscsi_map
done < /tmp/iscsisesssion
echo "Output also available at \"/tmp/iscsi_map\""


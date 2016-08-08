echo "FC LUN Mapping with disks"
echo "SCSI,LUN,DISK" > /tmp/fc_map
echo "SCSI LUN DISK"
ls -l /sys/block/sd[a-z]/device  | rev| cut -d '/' -f 1 | rev > /tmp/fc_lun
while read line
do
validluntest=`echo $line | rev | cut -d ':' -f 1`
if [ $validluntest -ne 0 ]
then
    disk=`ls -l /sys/block/sd[a-z]/device | grep $line | cut -d '/' -f 4`
    scsi=`cat /proc/scsi/scsi | grep -B 1 CLDBYTE | grep $validluntest | grep Host | awk '{print $2}'`
    lun=`cat /proc/scsi/scsi | grep -B 1 CLDBYTE | grep $validluntest | grep Host | awk '{print $8}'`
    echo $scsi $lun $disk
    echo $scsi,$lun,$disk >> /tmp/fc_map
fi
done < /tmp/fc_lun
echo "Output also available at \"/tmp/fc_map\""


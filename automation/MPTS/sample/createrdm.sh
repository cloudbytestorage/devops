#!/bin/sh
vmname=VMNAME
datastore=DATASTORE
ctrl=0
target=1
vmlfile=VMLFILE

date=`date +%d%h%y%H%M%S`
vim-cmd  vmsvc/getallvms > /vmfs/volumes/$datastore/$vmname/vimid_list_backup_$date
vmid=`vim-cmd  vmsvc/getallvms | grep "${vmname}.vmx" | awk '{print $1}'`
echo $vmid
vim-cmd vmsvc/power.off $vmid

cp /vmfs/volumes/$datastore/$vmname/${vmname}.vmx /vmfs/volumes/$datastore/$vmname/${vmname}.backup_$date
j=1
while read line
do
echo $line
vmkfstools -z /vmfs/devices/disks/$line /vmfs/volumes/$datastore/${vmname}/${vmname}_${j}.vmdk
let "j=j+1"
echo $j
done < /autofolder/$vmlfile

virtualdev=`cat /vmfs/volumes/$datastore/$vmname/$vmname.vmx | grep scsi0.virtualDev | cut -d "=" -f 2`
echo $virtualdev

> /autofolder/rdmoutput
for one_rdmp in $(ls /vmfs/volumes/$datastore/$vmname/${vmname}_[0-9]-rdmp.vmdk | sed 's/-rdmp//') $(ls /vmfs/volumes/$datastore/$vmname/${vmname}_[0-9][0-9]-rdmp.vmdk | sed 's/-rdmp//')
do
[ $target -eq 7 ] && let "target=target+1"
[ $target -eq 16 ] && target=0 
    
if [ $target -eq 0 ]; then
let "ctrl=ctrl+1"
echo "scsi${ctrl}.present = \"TRUE\""
echo "scsi${ctrl}.sharedBus = \"none\""
echo "scsi${ctrl}.virtualDev = $virtualdev"
fi 
                        
echo "scsi${ctrl}:${target}.fileName = \"${one_rdmp}\""
echo "scsi${ctrl}:${target}.mode = \"independent-persistent\""
echo "scsi${ctrl}:${target}.deviceType = \"scsi-hardDisk\""
echo "scsi${ctrl}:${target}.present = \"TRUE\""
                                 
let "target=target+1"
done >> /autofolder/rdmoutput


cat /autofolder/rdmoutput >> /vmfs/volumes/$datastore/$vmname/${vmname}.vmx
vim-cmd vmsvc/reload ${vmid}

vim-cmd vmsvc/power.on $vmid

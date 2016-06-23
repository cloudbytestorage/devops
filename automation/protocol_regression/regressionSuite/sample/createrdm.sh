#!/bin/sh
vmname=VMNAME
datastore=DATASTORE
ctrl=0
target=1
vmlfile=VMLFILE

date=`date +%d%h%y%H%M%S`
vim-cmd  vmsvc/getallvms > /t/vimid_list_$date
cp /vmfs/volumes/$datastore/${vmname}.vmx /vmfs/volumes/$datastore/${vmname}.backup_$date

virtualdev=`cat /vmfs/volumes/$datastore/$vmname.vmx | grep scsi0.virtualDev | cut -d "=" -f 2`
echo $virtualdev

> /t/rdmoutput
for one_rdmp in $(ls /vmfs/volumes/$datastore/${vmname}_[0-9]-rdmp.vmdk | sed 's/-rdmp//') $(ls /vmfs/volumes/$datastore/${vmname}_[0-9][0-9]-rdmp.vmdk | sed 's/-rdmp//')
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
done >> /t/rdmoutput


cat /t/rdmoutput >> /vmfs/volumes/$datastore/${vmname}.vmx
vmid=`vim-cmd  vmsvc/getallvms | grep ${vmname} | awk '{print $1}'`
echo $vmid
vim-cmd vmsvc/reload ${vmid}


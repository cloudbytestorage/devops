noofdisks=NoofISCSIVolumes
nooftsms=NoofTSMS
echo $noofdisks
esxcfg-swiscsi -e
adaptername=`esxcli iscsi adapter list | grep iSCSI | awk '{print $1}'`
echo $adpatername

while read line
do
vmkiscsi-tool -D -a $line:3260 ${adaptername}
sleep 5
esxcfg-rescan ${adaptername}
done < /autofolder/tsmlist

disks=0
cnt=0
while [ $disks != $noofdisks ]
do
esxcfg-rescan ${adaptername}
cnt=`expr $cnt+1`
echo "Number of disks"
disks=`ls -l /vmfs/devices/disks/ | grep CloudByt | grep vml | awk '{print $9}' | wc -l`
echo $disks
if [ $cnt == 15 ]
then
    break
fi
echo "sleep for 60 secs"
sleep 60
done

rm /autofolder/VMLFILE
rm /autofolder/vmlfile*

ls -l /vmfs/devices/disks/ | grep CloudByt | grep vml | awk '{print $9}' > /autofolder/VMLFILE

j=0
x=1
k=1
noofdisk_per_vm=NOOFVOLUMES
while read line
do
[ $k -eq 0 ] && let "x=x+1"
echo $line >> /autofolder/vmlfile$x
let "j=j+1"
echo $j
k=`expr $j % $noofdisk_per_vm`
done < /autofolder/VMLFILE

value=`ls /autofolder/vmlfile* | wc -l`
echo $value



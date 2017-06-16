#!/bin/sh

#######################################################################################################################
# Script Name : iscsi_io_runner.sh         									      		
# Description : Discover, login into iSCSI targets, identify corresponding scsi devices & run vdbench I/O             
# Args : Script takes TSM IP as argument                                                                              
# Pre-Requisites :a) Run the configCreator.sh before running this script b) Place the script in the vdbench directory 
# Creation Data : 26/07/2016                                                                                          
# Modifications : None											               		
# Script Author : Karthik											      
#######################################################################################################################

# Assign positional args & define usage

if [ "$1" == "" ]; then echo "Usage : sh iscsi_io_runner.sh vsm_ip1 vsm_ip2..vsm_ipn" ; exit
else continue
fi

#vsm_ip=$1

# Clear temp files

> fout
> target.out
> scsi.out
> iSCSIVDConf

# Discover, Login & identify SCSI devices
for i in $@
do 
iscsiadm -m discovery -t st -p $i:3260 | \
awk 'NF {system ("echo "$2 "| cut -d '\'':'\'' -f 2 >> target.out") ; \
system ("iscsiadm -m node -T "$2 " -l") ; \
system ("sleep 2") ; \
system ("iscsiadm -m session -P 3 | \
sed '\''1,/"$2 "/d'\'' | \
grep '\''Attached scsi disk'\'' | \
awk '\''{print $4}'\'' >> scsi.out ")}' > fout 2>&1
done

# Confirm successful discovery & login

if [ `cat target.out | wc -l` -eq 0 ]; then
echo -e "Discovery OR Login failed, check VSM connectivity OR LUN accessibility, exiting \n"
exit
else echo -e "LUN Discovery & Login completed \n"
fi

# Format devices, mount filesystems & append anchors to vdbench conf file

devices=`paste -d "," target.out scsi.out`

for i in $devices
do
  mount=`echo $i | cut -d "," -f 1`
  scsidevice=`echo $i | cut -d "," -f 2`
  mkdir -p /mnt/$mount 
  echo "Formatting $scsidevice"; mkfs.ext4 -F /dev/$scsidevice >> fout 2>&1
  if [ `echo $?` -ne 0 ]; then echo -e "Unable to format, check LUN access, exiting \n"
  exit
  else echo -e "Format completed \n" 
  fi
  mount -t ext4 -o discard /dev/$scsidevice /mnt/$mount
  echo "fsd=fsd$mount,anchor=/mnt/$mount,depth=1,width=1,files=1,size=2G" >> iSCSIVDConf
done

for i in `cat target.out`
do
  df -h -P | grep -q $i
  if [ `echo $?` -ne 0 ]; then echo -e "$i not mounted successfully, exiting \n"
  exit
  else echo "$i mounted successfully"
  fi
done

# Append workload definition & run definition to vdbench conf file

echo "fwd=fwd1,fsd=fsd*,xfersize=4k,rdpct=50,fileio=random,threads=1" >> iSCSIVDConf
echo "rd=rd1,fwd=fwd*,elapsed=36000,interval=1,fwdrate=max,format=yes" >> iSCSIVDConf
echo -e "Generated vdbench config file : iSCSIVDConf \n"

# Start vdbench I/O

timestamp=`date +%d%m%Y_%H%M%S`
echo -e "Running I/O \n"
./vdbench -f iSCSIVDConf -o output-$timestamp 	  
  

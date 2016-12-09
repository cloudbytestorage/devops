#!/bin/ksh

#
# Copyright (c) 2000, 2013, Oracle and/or its affiliates. All rights reserved.
#

#
# Author: Henk Vandenbergh.
#



# check for root
if [[ `/usr/ucb/whoami` == "root" ]] then
   echo "You have root!"
fi

echo ">>>>>uname -a"
uname -a

echo `date`
echo "mount"
mount

echo ">>>>>ifconfig -a"
ifconfig -a

echo ">>>>>id"
id

echo ">>>>>modinfo"
modinfo

echo ">>>>>cfgadm -al"
cfgadm -al

echo `date`
echo ">>>>>prtconf"
prtconf

echo `date`
echo ">>>>>prtdiag -v"

platform=`/usr/bin/uname -i 2> /dev/null`

if [ $? -ne 0 ]; then
  echo "prtdiag: could not determine platform" >& 2
else
  truepath=/usr/platform/$platform/sbin/prtdiag
  if [ -x $truepath ]; then
    exec $truepath -v
  else
    echo "prtdiag: not implemented on $platform" >& 2
  fi
fi


echo "cat /etc/system"
cat /etc/system

echo ">>>>>iostat -xdp"
iostat -xdp

echo ">>>>>iostat -xdnp"
iostat -xdnp

echo "cat /kernel/drv/scsi_vhci.conf"
cat /kernel/drv/scsi_vhci.conf

# Show if there are any other vdbench's or vdblite's running:
echo "ps -ef | grep vdb"
ps -ef | grep vdb


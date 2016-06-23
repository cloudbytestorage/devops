#!/bin/ksh

#
#
# Copyright 2010 Sun Microsystems, Inc. All rights reserved.
#
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
#
# The contents of this file are subject to the terms of the Common
# Development and Distribution License("CDDL") (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the License at http://www.sun.com/cddl/cddl.html
# or ../vdbench/license.txt. See the License for the
# specific language governing permissions and limitations under the License.
#
# When distributing the software, include this License Header Notice
# in each file and include the License file at ../vdbench/licensev1.0.txt.
#
# If applicable, add the following below the License Header, with the
# fields enclosed by brackets [] replaced by your own identifying information:
# "Portions Copyrighted [year] [name of copyright owner]"
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

echo ">>>>>ifconfig -a"
ifconfig -a

echo ">>>>>id"
id

echo ">>>>>modinfo"
modinfo

echo ">>>>>cfgadm -al"
cfgadm -al

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


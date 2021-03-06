#!/bin/bash

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

#
# This script was written specifically for running Vdbench on native VmWare .
# It turns out that VmWare does NOT have the Cshell.
# This also works for some brand-x version of Linux that did not have csh.
#
# Intructions:
# - cp /bin/bash /bin/csh   ===> This creates a clone of bash, naming it csh.
# - cp vdbench.bash vdbench ===> vdbench will now use THIS script instead of ./vdbench
#
#


# Directory where script was started from:
dir=`dirname $0`

# If the first parameter equals -SlaveJvm then this means that
# the script must start vdbench with more memory.
# Since all the real work is done in a slave, vdbench itself can be
# started with just a little bit of memory, while the slaves must
# have enough memory to handle large amount of threads and buffers.

# Set classpath.
# $dir                 - parent of $dir/solaris/solx86/linux/aix/hp/mac subdirectory
# $dir/../classes      - for development overrides
# $dir/vdbench.jar     - everything, including vdbench.class
cp=$dir/:$dir/classes:$dir/vdbench.jar

# Proper path for java:
java=java


# When out of memory, modify the first set of memory parameters. See above.
# '-client' is an option for Sun's Java. Remove if not needed.
if [ "$1" = "SlaveJvm" ]; then
  $java -client -Xmx1024m -Xms128m -cp $cp Vdb.SlaveJvm $*
  exit $status
else
  $java -client -Xmx512m  -Xms64m  -cp $cp Vdb.Vdbmain $*
  exit $status
fi

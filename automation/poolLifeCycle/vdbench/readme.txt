
/*
 * Copyright 2010 Sun Microsystems, Inc. All rights reserved.
 *
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
 *
 * The contents of this file are subject to the terms of the Common
 * Development and Distribution License("CDDL") (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the License at http://www.sun.com/cddl/cddl.html
 * or ../vdbench/license.txt. See the License for the
 * specific language governing permissions and limitations under the License.
 *
 * When distributing the software, include this License Header Notice
 * in each file and include the License file at ../vdbench/licensev1.0.txt.
 *
 * If applicable, add the following below the License Header, with the
 * fields enclosed by brackets [] replaced by your own identifying information:
 * "Portions Copyrighted [year] [name of copyright owner]"
 */


/*
 * Author: Henk Vandenbergh.
 */



Readme file for vdbench502: Wed Feb 10 10:17:15 MST 2010


Note to those who have installed Vdbench up until vdbench500rc8:
================================================================

Due to the fact that Vdbench is going open source the Vdbench installer
no longer is needed. All that is needed is an untar or unzip of the
downloaded file and you're ready to go.
It does mean however that if you used the installer to place the proper
java executable file name in the 'vdbench' or 'vdbench.bat' script, you'll have
to now do this manually.


Java requirements:
==================

You need at a minimum java 1.5.0
Follow the Java installation instructions.

If you don't have the proper Java installed download the JRE
(Java Runtime Environment) from www.sun.com, minimum 1.5.0


Note: You don't have to replace the current default Java version; Java can run
from your own private directories.


Documentation:
==============

You will find vdbench.pdf in your install directory, and there  are several
'example' parameter files also in the install directory.



How to start vdbench?
=====================


A very quick test can be done without ever having to create a Vdbench parameter file.
Just run:

./vdbench -t

And Vdbench will run the following very simple workload:

     *
     * This sample parameter file first creates a temporary file
     * if this is the first time the file is referenced.
     * It then does a five second 4k 50% read, 50% write test.
     *
     sd=sd1,lun=/var/tmp/quick_vdbench_test,size=10m
     wd=wd1,sd=sd1,xf=4k,rdpct=50
     rd=rd1,wd=wd1,iorate=100,elapsed=5,interval=1

After this point your favorite browser to ../vdbench/output/summary.html to
look at the reports that vdbench creates.


You'll find sample parameter files example1 - example7 in the installation directory.



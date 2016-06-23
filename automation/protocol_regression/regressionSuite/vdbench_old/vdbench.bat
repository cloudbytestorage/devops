
@echo off


rem
rem
rem Copyright 2010 Sun Microsystems, Inc. All rights reserved.
rem
rem DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
rem
rem The contents of this file are subject to the terms of the Common
rem Development and Distribution License("CDDL") (the "License").
rem You may not use this file except in compliance with the License.
rem
rem You can obtain a copy of the License at http://www.sun.com/cddl/cddl.html
rem or ../vdbench/license.txt. See the License for the
rem specific language governing permissions and limitations under the License.
rem
rem When distributing the software, include this License Header Notice
rem in each file and include the License file at ../vdbench/licensev1.0.txt.
rem
rem If applicable, add the following below the License Header, with the
rem fields enclosed by brackets [] replaced by your own identifying information:
rem "Portions Copyrighted [year] [name of copyright owner]"
rem

rem
rem Author: Henk Vandenbergh.
rem


rem If the first parameter equals -SlaveJvm then this means that
rem the script must start vdbench with more memory.
rem Since all the real work is done in a slave, vdbench itself can be
rem started with just a little bit of memory, while the slaves must
rem have enough memory to handle large amount of threads and buffers.

rem Directory where this is executed from:
set dir=%~dp0

rem Set classpath.
rem %dir%                 - parent of %dir%\windows subdirectory
rem %dir%\..\classes      - for development overrides
rem %dir%\vdbench.jar     - everything, including vdbench.class

set cp=%dir%;%dir%classes;%dir%vdbench.jar

rem Proper path for java:
set java=java

rem When out of memory, modify the first set of memory parameters. See above.
rem '-client' is an option for Sun's Java. Remove if not needed.
if "%1" EQU "SlaveJvm" (
 %java% -client -Xmx512m -Xms64m -cp "%cp% " Vdb.SlaveJvm %*
) else (
 %java% -client -Xmx256m -Xms64m -cp "%cp% " Vdb.Vdbmain %*
)

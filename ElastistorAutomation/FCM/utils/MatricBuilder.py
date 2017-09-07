#!/usr/bin/env python
#title           :NHCQA-.py
#description     :module to verified if java is instaled And matrixBuilder run for JMX
#author          :Alok
#date            :20160831
#version         :1
#usage           :
#notes           :
#python_version  :2.7
#==============================================================================

#!/usr/bin/env python2.7

import os
import sys, argparse
import subprocess


os.chdir( '/opt/emc/nhc/bin/' )
retval = os.getcwd()

f = open("/root/blah.txt", "w")
subprocess.call(['java', '-jar', '/opt/emc/nhc/bin/MetricsBuilder.jar'],stdout=f)
x="Jmx collector data xml file is created successfully"

ls = subprocess.Popen(['cat', "blah.txt"], stdout=subprocess.PIPE)

grep=subprocess.Popen(("grep", "%s"%x),stdin=ls.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output = grep.communicate()[0]
out=output.strip()
lenout=len(output)
lenstr = str(lenout)
f = open("/root/len.txt", "w")
f.write(lenstr)
f.close
if(lenout != 0):
   sys.exit(0)
else:  
   sys.exit(1)

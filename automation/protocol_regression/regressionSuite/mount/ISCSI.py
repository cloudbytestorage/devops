import os
#import json
import subprocess
import time

#Take ip
IP=raw_input("Ener valid ip")
#get uuid of host
uuid='xe host-list |grep uuid |cut -d ":" -f 2|cut -d " " -f 2'
link = subprocess.Popen(uuid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
ldata = link.stdout.readlines()
#ldata=ldatai.strip(' \n\t\r')
output, errors = link.communicate()
rco = link.returncode
#Get the name Sr to be created

SRname=raw_input("Ener the SR name to be created or deleted")
#Discover iscsi LUNs
iqnlist='iscsiadm -m discovery -t sendtargets -p'+IP+'| cut -d " " -f 2'
link1 = subprocess.Popen(iqnlist, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
ldata1 = link1.stdout.readlines()
if ldata1 :
  print ldata1
  for s in ldata1 :
#	print "first"
	login='iscsiadm --mode node --targetname '+s.strip(" \n\r\t")+' --portal '+IP+':3260 --login'
	iscsilogin = subprocess.Popen(login, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	time.sleep(5)
#greping the iqns of mounting ISCSI LUN

	lungrep='ls -l /dev/disk/by-path/ |grep '+IP+'| cut -d ":" -f 4|cut -d "/" -f 3'
	print lungrep

	lngrep = subprocess.Popen(lungrep, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	ldata2=lngrep.stdout.readlines()
        #print ldata2

	output, errors = lngrep.communicate()
	print str(errors)
	i=1
	for a in ldata2 :
		name1=str(SRname)+str(i)
		print a
#Grep scsid of the Disk

		ssid='ls -l /dev/disk/by-id/ |grep '+a.strip(" \n\t\r")+'| cut -d "-" -f 2'
		print ssid

		scsid= subprocess.Popen(ssid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		ld2=scsid.stdout.readlines()
		print ld2 
		
#Creating SR on Citrix


		if ldata :
                  print "ldata"+ldata[0]
                  value=str(ldata[0]).strip("\n\t\r")
                  print "value"+value
		  srcreate='xe sr-create host-uuid='+value+' content-type=user name-label='+name1+' shared=true device-config:target='+str(IP)+' device-config:targetIQN='+str(s).strip(" \n\t\r")+' device-config:SCSIid='+ld2[0].strip(" \n\t\r")+' type=lvmoiscsi'
		print srcreate	
		SR=subprocess.Popen(srcreate, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		output,errors=SR.communicate()
		print errors
		i += 1 
else:
  print "No ISCSI Lun exposed"  	
